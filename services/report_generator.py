import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.colors import HexColor 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

def add_nested_details_to_story(data, story, styles, level=0):
    """Hàm đệ quy để chuyển dictionary/list thành các dòng Paragraph có căn lề"""
    indent = level * 15
    detail_style = ParagraphStyle(
        f'DetailLevel{level}', 
        parent=styles['Normal'], 
        leftIndent=indent,
        fontSize=9,
        spaceAfter=2
    )

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                story.append(Paragraph(f"<b>{key}:</b>", detail_style))
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
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # 1. Header & Title
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'],
        fontSize=22, textColor=colors.HexColor("#2980b9"),
        alignment=1, spaceAfter=10
    )
    story.append(Paragraph("Wi-Fi Security Analysis Report", title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 15))

    # 2. Overview Table
    info_data = [
        ["Property", "Value"],
        ["SSID", data.get("SSID")],
        ["BSSID", data.get("BSSID")],
        ["Security Standard", data.get("Security")],
        ["Signal Strength", f"{data.get('Signal')} dBm"],
        ["Band / Channel", f"{data.get('Band')} / {data.get('Channel')}"],
        ["Security Score", f"{data.get('Score')}/100"]
    ]
    
    t = Table(info_data, colWidths=[140, 320])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495e")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # 3. Security Findings (Pros/Cons)
    # Pros
    story.append(Paragraph("Positive Security Findings", styles['Heading2']))
    for pro in data.get("Pros", []):
        story.append(Paragraph(f"<b>[+]</b> {pro}", styles['Normal']))
    story.append(Spacer(1, 10))

    # Cons & Solutions
    story.append(Paragraph("Risks & Recommendations", styles['Heading2']))
    for con in data.get("Cons", []):
        issue_p = Paragraph(f"<b>[!] RISK:</b> {con['issue']}", ParagraphStyle('R', parent=styles['Normal'], textColor=colors.red))
        sol_p = Paragraph(f"<i>Suggestion:</i> {con['solution']}", ParagraphStyle('S', parent=styles['Normal'], textColor=colors.darkgreen, leftIndent=15))
        story.append(issue_p)
        story.append(sol_p)
        story.append(Spacer(1, 5))

    # 4. Technical Details (Page Break to keep it organized)
    story.append(PageBreak())
    story.append(Paragraph("Full Technical Details (Raw Metadata)", styles['Heading2']))
    story.append(Paragraph("The following data is extracted directly from the Wi-Fi beacon/probe response frames:", styles['Italic']))
    story.append(Spacer(1, 10))
    
    # Gọi hàm đệ quy để đổ dữ liệu chi tiết
    details_dict = data.get("Details", {})
    add_nested_details_to_story(details_dict, story, styles)

    # Build PDF
    try:
        doc.build(story)
        return True
    except Exception as e:
        print(f"PDF Build Error: {e}")
        return False