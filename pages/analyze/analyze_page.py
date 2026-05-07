from PySide6.QtWidgets import QWidget, QLabel, QTreeWidgetItem, QHeaderView, QVBoxLayout
from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont

from pages.analyze.ui_analyze import Ui_Form
from services.analyze_networks import analyze_network


class AnalyzePage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.networks = []

        # Cấu hình giao diện ban đầu cho TreeWidget
        self.setup_tree_style()

        # Hiển thị trang trống mặc định
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)

        self.score_layout = QVBoxLayout(self.ui.frScore)
        self.score_layout.setContentsMargins(0, 0, 0, 0)

        self.circular_score = CircularScoreWidget()
        self.score_layout.addWidget(self.circular_score)

    def setup_tree_style(self):
        """Cấu hình giao diện cho TreeWidget có sẵn trong UI"""
        self.ui.treeWidget.setColumnCount(2)
        self.ui.treeWidget.setHeaderLabels(["Property", "Value"])

        # Cho phép cột Property tự co giãn theo nội dung
        self.ui.treeWidget.header().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.ui.treeWidget.setAlternatingRowColors(True)
        self.ui.treeWidget.setAnimated(True)

        self.ui.treeWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.treeWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.ui.treeWidget.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #ecf0f1;
                background-color: #ffffff;
                font-size: 14px;
                outline: 0;
            }
            QTreeWidget::item {
                padding: 4px;
                border-bottom: 1px solid #f9f9f9;
            }
            QTreeWidget::item:selected {
                background-color: #e3f2fd;
                color: #000;
            }
        """)

    def clear_layout(self, layout):
        """Xóa tất cả các widget cũ trong một layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def fill_tree(self, data, parent_item):
        """Hàm đệ quy để đổ dữ liệu dictionary vào TreeWidget"""
        if isinstance(data, dict):
            for key, value in data.items():
                # Tạo node mới với tên key ở cột 0
                child = QTreeWidgetItem([str(key)])
                parent_item.addChild(child)
                # Tiếp tục đệ quy xuống sâu hơn
                self.fill_tree(value, child)
        elif isinstance(data, list):
            for index, value in enumerate(data):
                # Hiển thị index của list
                child = QTreeWidgetItem([f"[{index}]"])
                parent_item.addChild(child)
                self.fill_tree(value, child)
        else:
            # Nếu là giá trị cuối (string, int...), hiển thị ở cột 1 của node hiện tại
            parent_item.setText(1, str(data))
            # Đổi màu giá trị cuối để dễ phân biệt
            parent_item.setForeground(1, Qt.darkBlue)

    def update_analyze_results(self, bssid, networks):
        self.networks = networks
        data = analyze_network(bssid, self.networks)

        # 1. Kiểm tra nếu không tìm thấy dữ liệu
        if data is None:
            self.ui.lblStatusText.setText(f"Error: BSSID {bssid} not found.")
            self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)
            return

        score_value = data.get("Score", "0/100")
        self.circular_score.set_score(score_value)

        # 2. Cập nhật thông tin cơ bản (Header labels)
        self.ui.lblSSID.setText(f"SSID: {data['SSID']}")
        self.ui.lblBSSID.setText(f"BSSID: {data['BSSID']}")
        self.ui.lblSecurity.setText(f"Security: {data['Security']}")
        self.ui.lblFreqChan.setText(f"Channel: {data['Channel']}")
        self.ui.lblInterface.setText(f"Interface: {data['Interface']}")
        self.ui.lblScore.setText(f"Overall Score: {data['Score']}")

        # 3. Làm sạch dữ liệu cũ
        self.clear_layout(self.ui.verticalLayout_12)  # Pros
        self.clear_layout(self.ui.verticalLayout_13)  # Cons
        self.ui.treeWidget.clear()  # Xóa các node cũ trong Tree

        # 4. Đổ danh sách Pros
        for pro in data.get("Pros", []):
            lbl = QLabel(f"✔ {pro}")
            lbl.setWordWrap(True)
            lbl.setStyleSheet("color: #2e7d32; font-weight: 500; font-size: 12px;")
            self.ui.verticalLayout_12.addWidget(lbl)
        self.ui.verticalLayout_12.addStretch()

        # 5. Đổ danh sách Cons
        self.clear_layout(self.ui.verticalLayout_13)
        for con in data.get("Cons", []):
            lbl = QLabel(con)
            lbl.setWordWrap(True)

            # Nếu là cảnh báo bảo mật từ hàm detect_suspicious_networks
            if "SECURITY ALERT" in con or "CRITICAL" in con:
                lbl.setStyleSheet("""
                    color: white; 
                    background-color: #d32f2f; 
                    font-weight: bold; 
                    padding: 4px; 
                    border-radius: 2px;
                """)
            elif "Suspicious" in con:
                lbl.setStyleSheet("color: #b71c1c; font-weight: bold;")
            else:
                lbl.setStyleSheet("color: #d32f2f; font-weight: 500;")

            self.ui.verticalLayout_13.addWidget(lbl)
        self.ui.verticalLayout_13.addStretch()

        # 6. Đổ dữ liệu vào TreeWidget (Phần Details)
        details_dict = data.get("Details", {})
        for key, value in details_dict.items():
            # Tạo node gốc (Top Level)
            root_node = QTreeWidgetItem([str(key)])
            self.ui.treeWidget.addTopLevelItem(root_node)
            # Gọi đệ quy để tạo các nhánh con
            self.fill_tree(value, root_node)

        # 7. Tùy chỉnh hiển thị: Chỉ mở sẵn các node gốc
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            self.ui.treeWidget.topLevelItem(i).setExpanded(False)

        self.ui.stackedWidget.setCurrentWidget(self.ui.pageData)


class CircularScoreWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.score = 0
        self.setMinimumSize(120, 120)

    def set_score(self, value):
        # Chuyển đổi chuỗi "85/100" thành số 85
        try:
            if isinstance(value, str):
                self.score = int(value.split("/")[0])
            else:
                self.score = value
        except:
            self.score = 0
        self.update()  # Vẽ lại widget

    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        size = min(width, height) - 20
        rect = QRectF((width - size) / 2, (height - size) / 2, size, size)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. Vẽ vòng tròn nền (Xám nhạt)
        pen = QPen()
        pen.setWidth(10)
        pen.setColor(QColor("#e6e6e6"))
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawEllipse(rect)

        # 2. Xác định màu sắc dựa trên điểm số
        if self.score >= 75:
            color = QColor("#2ecc71")  # Xanh lá
        elif self.score >= 45:
            color = QColor("#f1c40f")  # Vàng
        else:
            color = QColor("#e74c3c")  # Đỏ

        # 3. Vẽ cung tròn tiến độ (Progress Arc)
        pen.setColor(color)
        painter.setPen(pen)
        # Tính toán góc (Score 100 = 360 độ). Qt dùng đơn vị 1/16 độ.
        start_angle = 90 * 16
        span_angle = -self.score * 3.6 * 16
        painter.drawArc(rect, start_angle, span_angle)

        # 4. Vẽ chữ số điểm ở giữa
        painter.setPen(QColor("#333333"))
        painter.setFont(QFont("Segoe UI", 18, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, f"{self.score}")
