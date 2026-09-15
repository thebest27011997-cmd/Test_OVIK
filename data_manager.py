# data_manager.py
import os
from datetime import datetime
import config

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def generate_pdf_report_flet(user_name, correct_count, total_count, status, answers_history):
    """Экспорт результатов тестирования в кроссплатформенный формат PDF с поддержкой кириллицы."""
    try:
        output_dir = "Результаты"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        current_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        percent = round((correct_count / total_count) * 100) if total_count > 0 else 0

        db_path = os.path.join(output_dir, "база_результатов.txt")
        with open(db_path, "a", encoding="utf-8") as db_file:
            db_file.write(f"{user_name}, {percent}%, {current_time}\n")

        font_path = os.path.join("assets", "fonts", "Arial.ttf")
        if not os.path.exists(font_path): font_path = os.path.join("fonts", "Arial.ttf") 
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('RussianFont', font_path))
        else:
            print("Ошибка: Шрифт Arial.ttf не найден!")
            return

        clean_name = "".join(c for c in user_name if c.isalnum() or c in (" ", "_", "-")).strip()
        pdf_filename = os.path.join(output_dir, f"{clean_name}_{datetime.now().strftime('%d.%m.%y')}.pdf")

        doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        story, styles = [], getSampleStyleSheet()
        
        title_style = ParagraphStyle('PDFTitle', parent=styles['Heading1'], fontName='RussianFont', fontSize=22, textColor=colors.HexColor("#1A237E"), spaceAfter=15)
        info_style = ParagraphStyle('PDFInfo', parent=styles['Normal'], fontName='RussianFont', fontSize=11, leading=16, spaceAfter=5)
        q_style = ParagraphStyle('PDFQuestion', parent=styles['Normal'], fontName='RussianFont', fontSize=12, leading=16, spaceAfter=8)
        ans_style = ParagraphStyle('PDFAnswer', parent=styles['Normal'], fontName='RussianFont', fontSize=10, leading=14, leftIndent=15, spaceAfter=4)

        story.append(Paragraph("Результаты тестирования ОВиК", title_style))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1A237E"), spaceAfter=15))
        story.append(Paragraph(f"<b>Сотрудник:</b> {user_name}", info_style))
        story.append(Paragraph(f"<b>Дата прохождения:</b> {current_time}", info_style))
        story.append(Paragraph(f"<b>Итоговый результат:</b> {correct_count} из {total_count} ({percent}%)", info_style))
        
        if config.settings["mode"] == "контрольные вопросы":
            res_color = "#2E7D32" if status == "Пройден" else "#C62828"
            story.append(Paragraph(f"<b>Вердикт: <font color='{res_color}'>{status.upper()}</font></b>", info_style))
        
        story.append(Spacer(1, 15))
        story.append(Paragraph("Детализация по ответам:", ParagraphStyle('Sub', parent=title_style, fontSize=16, spaceAfter=10)))

        for idx, (q_text, u_ans, c_ans, verdict, source_text) in enumerate(answers_history, start=1):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=10, spaceBefore=5))
            story.append(Paragraph(f"<b>Вопрос {idx}:</b> {q_text.replace('\n', '<br/>')}", q_style))

            if verdict == "Верно":
                story.append(Paragraph(f"<b>Ваш ответ:</b> <font color='green'>{u_ans}</font>", ans_style))
            else:
                story.append(Paragraph(f"<b>Ваш ответ:</b> <font color='red'>{u_ans}</font>", ans_style))
                story.append(Paragraph(f"<i>Правильный ответ:</i> <font color='green'><b>{c_ans}</b></font>", ans_style))

            if config.settings["mode"] != "контрольные вопросы" and source_text:
                story.append(Paragraph(f"<i>Источник: <font color='blue'>{source_text}</font></i>", ans_style))

        doc.build(story)
    except Exception as e:
        print(f"Ошибка сохранения PDF: {e}")
