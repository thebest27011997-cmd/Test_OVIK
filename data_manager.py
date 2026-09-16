# data_manager.py
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def generate_pdf_report_flet(user_name, correct_count, total_questions, status, history):
    """Генерация PDF отчета на Android без использования pandas."""
    # Задаем имя файла отчета
    filename = f"Репорт_{user_name.replace(' ', '_')}.pdf"
    
    # Пытаемся подключить кириллический шрифт из ассетов
    try:
        font_path = os.path.join("assets", "fonts", "Helvetica.ttf")
        if not os.path.exists(font_path):
            font_path = "Helvetica.ttf"
        pdfmetrics.registerFont(TTFont('Helvetica', font_path))
        font_name = 'Helvetica'
    except Exception:
        font_name = 'Helvetica' # дефолтный откат
        
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1A365D"),
        alignment=1
    )
    
    text_style = ParagraphStyle(
        'TextStyle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2D3748")
    )
    
    # Шапка PDF
    story.append(Paragraph("Результаты тестирования ОВ", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(f"Сотрудник: {user_name}", text_style))
    story.append(Paragraph(f"Результат: {correct_count} из {total_questions}", text_style))
    story.append(Paragraph(f"Статус: {status.upper()}", text_style))
    story.append(Spacer(1, 20))
    
    # Таблица результатов
    table_data = [[
        Paragraph("<b>Вопрос</b>", text_style), 
        Paragraph("<b>Ваш ответ</b>", text_style), 
        Paragraph("<b>Верный ответ</b>", text_style), 
        Paragraph("<b>Вердикт</b>", text_style)
    ]]
    
    for item in history:
        # history состоит из кортежей: (q_text, u_ans, q_correct, verdict, source)
        q_text, u_ans, q_correct, verdict, _ = item
        table_data.append([
            Paragraph(str(q_text), text_style),
            Paragraph(str(u_ans), text_style),
            Paragraph(str(q_correct), text_style),
            Paragraph(str(verdict), text_style)
        ])
        
    # Стили таблицы
    t = Table(table_data, colWidths=[200, 110, 110, 70])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    
    story.append(t)
    
    try:
        doc.build(story)
        print(f"Отчет {filename} успешно сохранен.")
    except Exception as e:
        print(f"Ошибка сохранения PDF: {e}")
