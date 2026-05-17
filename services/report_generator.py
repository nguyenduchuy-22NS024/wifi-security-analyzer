import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable

# Cấu hình màu sắc hiện đại
COLOR_PRIMARY = colors.HexColor("#1A5276")    # Xanh đậm chuyên nghiệp
COLOR_SECONDARY = colors.HexColor("#D5DBDB")  # Xám nhạt cho line
COLOR_SUCCESS = colors.HexColor("#27AE60")    # Xanh lá
COLOR_DANGER = colors.HexColor("#C0392B")     # Đỏ
COLOR_WARNING = colors.HexColor("#F39C12")    # Cam
COLOR_TEXT = colors.HexColor("#2C3E50")       # Đen xám

def get_score_color(score):
    if score >= 80: return COLOR_SUCCESS
    if score >= 50: return COLOR_WARNING
    return COLOR_DANGER

def add_nested_details_to_story(data, story, styles, level=0):
    indent = level * 12
    # Style cho technical data (giống code block)
    detail_style = ParagraphStyle(
        f'DetailLevel{level}', 
        parent=styles['Normal'], 
        leftIndent=indent,
        fontSize=8,
        fontName='Courier', # Font máy tính
        textColor=colors.HexColor("#34495E"),
        spaceAfter=1
    )

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                story.append(Paragraph(f"<b>{key}</b>", detail_style))
                add_nested_details_to_story(value, story, styles, level + 1)
            else:
                story.append(Paragraph(f"<b>{key}:</b> {value}", detail_style))
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                add_nested_details_to_story(item, story, styles, level + 1)
            else:
                story.append(Paragraph(f"• {item}", detail_style))

def generate_wifi_report(data, filepath):
    doc = SimpleDocTemplate(
        filepath, 
        pagesize=letter,
        rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50
    )
    styles = getSampleStyleSheet()
    story = []

    # --- 1. HEADER SECTION ---
    title_style = ParagraphStyle(
        'MainTitle', parent=styles['Heading1'],
        fontSize=24, textColor=colors.white,
        alignment=1, spaceAfter=20, fontName='Helvetica-Bold'
    )
    
    # Tạo Header background dùng Table
    header_table = Table([[Paragraph("Wi-Fi SECURITY ANALYSIS REPORT", title_style)]], colWidths=[510])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_PRIMARY),
        ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 15),
    ]))
    story.append(header_table)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"Report ID: {os.urandom(4).hex().upper()} | Date: {datetime.now().strftime('%d %M %Y, %H:%M')}", 
                           ParagraphStyle('Sub', parent=styles['Italic'], alignment=2, fontSize=8)))
    story.append(Spacer(1, 20))

        # --- 2. SUMMARY DASHBOARD ---
    score = data.get("Score", 0)
    score_color = get_score_color(score)

    # Định nghĩa style riêng cho các thành phần trong Score để tránh lỗi đè chữ
    style_score_label = ParagraphStyle('ScoreLabel', alignment=1, fontSize=10, fontName='Helvetica-Bold', leading=12)
    style_score_val = ParagraphStyle('ScoreVal', alignment=1, fontSize=48, textColor=score_color, fontName='Helvetica-Bold', leading=50) # leading >= fontSize
    style_score_footer = ParagraphStyle('ScoreTotal', alignment=1, fontSize=9, leading=10, textColor=colors.grey)

    # Tạo một bảng nhỏ chỉ dành riêng cho ô điểm số (để căn giữa chính xác)
    score_content = [
        [Paragraph("SECURITY SCORE", style_score_label)],
        [Paragraph(f"{score}", style_score_val)],
        [Paragraph("out of 100", style_score_footer)]
    ]
    score_sub_table = Table(score_content, colWidths=[140])
    score_sub_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))

    # Cột bên trái: Thông tin chi tiết
    info_content = [
        [Paragraph(f"<b>SSID:</b> {data.get('SSID')}", styles['Normal'])],
        [Paragraph(f"<b>BSSID:</b> {data.get('BSSID')}", styles['Normal'])],
        [Paragraph(f"<b>Security:</b> {data.get('Security')}", styles['Normal'])],
        [Paragraph(f"<b>Signal:</b> {data.get('Signal')} dBm", styles['Normal'])],
        [Paragraph(f"<b>Channel:</b> {data.get('Channel')} ({data.get('Band')})", styles['Normal'])]
    ]
    info_sub_table = Table(info_content, colWidths=[340])
    info_sub_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))

    # Kết hợp vào bảng chính
    main_summary_data = [[info_sub_table, score_sub_table]]
    summary_table = Table(main_summary_data, colWidths=[350, 150])
    
    summary_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECONDARY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#F8F9F9")), # Màu nền nhẹ cho ô điểm số
        ('BOX', (0, 0), (-1, -1), 1, COLOR_PRIMARY), # Viền ngoài đậm hơn
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 25))

    # --- 3. ANALYSIS DETAILS (PROS & CONS) ---
    # Pros
    story.append(Paragraph("✔ Positive Security Features", ParagraphStyle('H2', parent=styles['Heading2'], textColor=COLOR_SUCCESS)))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_SUCCESS, spaceAfter=10))
    
    for pro in data.get("Pros", []):
        story.append(Paragraph(f"<font color='#27AE60'>●</font> {pro}", styles['Normal']))
    
    story.append(Spacer(1, 20))

    # Cons
    story.append(Paragraph("⚠ Identified Risks & Mitigations", ParagraphStyle('H2', parent=styles['Heading2'], textColor=COLOR_DANGER)))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_DANGER, spaceAfter=10))
    
    for con in data.get("Cons", []):
        # Create a small "Card" for each risk
        issue_table = Table([
            [Paragraph(f"<b>RISK:</b> {con['issue']}", ParagraphStyle('R', parent=styles['Normal'], textColor=COLOR_DANGER))],
            [Paragraph(f"<b>Action:</b> {con['solution']}", ParagraphStyle('S', parent=styles['Normal'], textColor=colors.black, leftIndent=10))]
        ], colWidths=[490])
        issue_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor("#FDEDEC")),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(issue_table)
        story.append(Spacer(1, 8))

    # --- 4. TECHNICAL RAW DATA ---
    story.append(PageBreak())
    story.append(Paragraph("Technical Metadata Extraction", ParagraphStyle('H2', parent=styles['Heading2'], textColor=COLOR_PRIMARY)))
    story.append(Paragraph("Below is the raw frame information captured during the scan:", styles['Italic']))
    story.append(Spacer(1, 10))
    
    # Tạo một khung màu xám nhạt cho technical data
    details_dict = data.get("Details", {})
    add_nested_details_to_story(details_dict, story, styles)

    # Build PDF
    try:
        doc.build(story)
        return True
    except Exception as e:
        print(f"PDF Build Error: {e}")
        return False