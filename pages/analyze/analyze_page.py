from datetime import datetime

from PySide6.QtWidgets import QWidget, QLabel, QTreeWidgetItem, QHeaderView, QVBoxLayout
from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import QWidget, QHBoxLayout, QFileDialog, QMessageBox
from PySide6.QtGui import QPainter, QPen, QColor, QFont

from pages.analyze.ui_analyze import Ui_Form
from services.analyze_networks import analyze_network
from services.report_generator import generate_wifi_report


class AnalyzePage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.networks = []
        self.current_bssid = None

        # Cấu hình giao diện ban đầu cho TreeWidget
        self.setup_tree_style()

        # Hiển thị trang trống mặc định
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)

        self.score_layout = QVBoxLayout(self.ui.frScore)
        self.score_layout.setContentsMargins(0, 0, 0, 0)

        self.circular_score = CircularScoreWidget()
        self.score_layout.addWidget(self.circular_score)

        self.ui.btnTrusted.clicked.connect(self.trusted_network)
        self.ui.btnReport.clicked.connect(self.report_network)

        self.setStyleSheet("""
    QToolTip {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #dcdde1;
        border-radius: 4px;
        padding: 8px;
    }
""")

    def report_network(self):
        """Chức năng xuất báo cáo PDF cho mạng Wi-Fi hiện tại"""
        if not self.current_bssid:
            QMessageBox.warning(
                self, "Warning", "Please select a network to analyze first."
            )
            return

        # Lấy dữ liệu phân tích hiện tại
        data = analyze_network(self.current_bssid, self.networks)
        if not data:
            return

        # Mở hộp thoại lưu file
        default_name = (
            f"Wifi_Report_{data['SSID']}_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", default_name, "PDF Files (*.pdf)"
        )

        if file_path:
            try:
                # Gọi service tạo PDF
                success = generate_wifi_report(data, file_path)
                if success:
                    QMessageBox.information(
                        self, "Success", f"Report saved successfully to:\n{file_path}"
                    )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to generate report: {str(e)}"
                )

    def trusted_network(self):
        pass

    def update_analyze_results(self, bssid, networks):
        self.networks = networks
        self.current_bssid = bssid
        data = analyze_network(bssid, self.networks)
        print(data)

        # 1. Kiểm tra nếu không tìm thấy dữ liệu
        if data is None:
            self.ui.lblStatusText.setText(f"Error: BSSID {bssid} not found.")
            self.ui.stackedWidget.setCurrentWidget(self.ui.pageEmpty)
            return

        score_value = data.get("Score", "0/100")
        breakdown = data.get("ScoreBreakdown", [])
        self.circular_score.set_score_data(score_value, breakdown)

        # 2. Cập nhật thông tin cơ bản (Header labels)
        self.ui.lblSSID.setText(f"SSID: {data['SSID']}")
        self.ui.lblBSSID.setText(f"BSSID: {data['BSSID']}")
        self.ui.lblSecurity.setText(f"Security: {data['Security']}")
        self.ui.lblFreqChan.setText(f"Channel: {data['Channel']}")
        self.ui.lblBand.setText(f"Band: {data['Band']}")
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

        # --- 5. ĐỔ DANH SÁCH CONS (PHIÊN BẢN MỚI CÓ TOOLTIP) ---
        self.clear_layout(self.ui.verticalLayout_13)
        cons_data = data.get("Cons", [])

        for item in cons_data:
            # Tạo container cho mỗi hàng lỗi
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 2, 0, 2)
            row_layout.setSpacing(8)

            # 1. Nhãn hiển thị tên lỗi (Issue)
            lbl_issue = QLabel(f"✘ {item['issue']}")
            lbl_issue.setWordWrap(True)
            lbl_issue.setStyleSheet(
                "color: #d32f2f; font-weight: 500; font-size: 12px;"
            )

            # 2. Icon dấu chấm hỏi (Dùng QLabel để bắt sự kiện Tooltip)
            lbl_help = QLabel("?")
            lbl_help.setFixedSize(16, 16)
            lbl_help.setAlignment(Qt.AlignCenter)
            lbl_help.setCursor(Qt.PointingHandCursor)

            # Đặt nội dung giải pháp vào ToolTip của icon này
            lbl_help.setToolTip(f"<b>Solution:</b><br>{item['solution']}")

            # Style cho icon dấu chấm hỏi: Hình tròn, màu xanh dương, chữ trắng
            lbl_help.setStyleSheet("""
                QLabel {
                    background-color: #1976d2;
                    color: white;
                    border-radius: 8px;
                    font-size: 11px;
                    font-weight: bold;
                }
                QLabel:hover {
                    background-color: #0d47a1;
                }
            """)

            row_layout.addWidget(lbl_issue, 1)  # Chiếm phần lớn không gian
            row_layout.addWidget(lbl_help, 0)  # Đứng cạnh bên phải

            self.ui.verticalLayout_13.addWidget(row_widget)

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

    def clear_layout(self, layout):
        """Xóa tất cả các widget cũ trong một layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class CircularScoreWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.score = 0
        self.setMinimumSize(120, 120)
        # Kích hoạt ToolTip với thời gian hiển thị lâu hơn
        self.setToolTipDuration(180000)

    def set_score_data(self, score_value, breakdown_list):
        """Cập nhật điểm và tạo nội dung ToolTip với style Card hiện đại"""
        try:
            if isinstance(score_value, str):
                self.score = int(score_value.split("/")[0])
            else:
                self.score = score_value
        except:
            self.score = 0

        if breakdown_list:
            # Bắt đầu chuỗi HTML với định dạng container
            tooltip_html = """
            <div style='min-width: 250px; background-color: white;'>
                <h3 style='color: #2c3e50; margin-bottom: 5px; border-bottom: 2px solid #3498db; padding-bottom: 3px;'>
                    Score Calculation
                </h3>
                <table border='0' cellpadding='4' cellspacing='0' style='width: 100%;'>
            """

            for item in breakdown_list:
                # Tự động xác định màu sắc dựa trên biểu tượng
                color = "#333333"  # Mặc định
                bg_style = ""

                if "+" in item:
                    color = "#27ae60"  # Xanh lá cho điểm cộng
                elif "-" in item or "Penalty" in item:
                    color = "#e74c3c"  # Đỏ cho hình phạt
                    bg_style = "background-color: #fdf2f2;"  # Nền đỏ nhạt cho dòng phạt

                tooltip_html += f"""
                    <tr style='{bg_style}'>
                        <td style='color: {color}; font-family: Segoe UI; font-size: 12px;'>
                            {item}
                        </td>
                    </tr>
                """

            # Thêm phần tổng kết cuối bảng
            tooltip_html += f"""
                </table>
                <div style='margin-top: 8px; padding-top: 5px; border-top: 1px dashed #bdc3c7; text-align: right;'>
                    <span style='font-size: 14px; font-weight: bold; color: #2c3e50;'>
                        Final Score: <span style='font-size: 16px; color: #2980b9;'>{self.score}</span>/100
                    </span>
                </div>
            </div>
            """
            self.setToolTip(tooltip_html)

        self.update()

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
