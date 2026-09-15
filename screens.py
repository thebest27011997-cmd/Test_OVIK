# screens.py — ЧАСТЬ 1
import os
import io
import random
import threading
import time
import hashlib
import pandas as pd
import flet as ft

# Официальный стандарт импорта для Flet 1.0.0: все элементы импортируются напрямую из flet
from flet import (
    Column, Row, Container, Text, TextField, ElevatedButton, 
    TextButton, RadioGroup, Radio, Checkbox, SnackBar, AlertDialog,
    MainAxisAlignment, CrossAxisAlignment
)

# Импорт криптографии напрямую в интерфейс (100% стабильность в APK)
from Crypto.Cipher import AES

import config
from data_manager import generate_pdf_report_flet

# screens.py — ЧАСТЬ 2

    def render_question_screen(self):
        self.page.clean()
        
        self.page.vertical_alignment = "start"
        self.page.horizontal_alignment = "stretch"
        
        idx = self.state["current_idx"]
        q = self.state["questions"][idx]
        
        info_text = Text(f"Сотрудник: {self.state['user_name']} | Режим: {config.settings['mode'].upper()}", size=12, italic=True)
        
        mins, secs = divmod(self.time_left_seconds, 60)
        timer_color = "red800" if self.time_left_seconds <= 60 else "bluegrey700"
        
        self.lbl_timer = Text(
            value=f"Осталось времени: {mins:02d}:{secs:02d}", 
            size=14, 
            weight="bold", 
            color=timer_color,
            visible=(config.settings["mode"] == "контрольные вопросы")
        )
        
        self.page.add(Row([info_text, self.lbl_timer], alignment=MainAxisAlignment.SPACE_BETWEEN))
        
        self.page.add(Text(f"Вопрос {idx + 1}:\n{q['text']}", size=16, weight="bold"))

        input_container = Column()
        checkboxes, radio_group = {}, RadioGroup(content=Column())
        text_field = TextField(label="Введите ваш ответ (без учета регистра)", width=450)

        if "один" in q["type"]:
            for opt in q["options"]: radio_group.content.controls.append(Radio(value=opt, label=opt))
            radio_group.value = self.state["saved_replies"].get(idx, "")
            input_container.controls.append(radio_group)
        elif "несколько" in q["type"]:
            self.page.add(Text("выберите несколько вариантов", size=12, color="orange800", italic=True))
            saved_arr = self.state["saved_replies"].get(idx, "").split("; ")
            for opt in q["options"]:
                cb = Checkbox(label=opt, value=(opt in saved_arr))
                checkboxes[opt] = cb
                input_container.controls.append(cb)
        elif "текст" in q["type"]:
            text_field.value = self.state["saved_replies"].get(idx, "")
            input_container.controls.append(text_field)

        self.page.add(input_container)

        source_ui = Text(f"Источник: {q['source'] if q['source'] else 'Не указан'}", size=12, italic=True, color="blue800", visible=False)
        self.page.add(source_ui)
        text_correct_lbl = Text("", color="green", weight="bold", visible=False)
        self.page.add(text_correct_lbl)
# screens.py — ЧАСТЬ 3

        def save_reply():
            if "один" in q["type"]: self.state["saved_replies"][idx] = radio_group.value if radio_group.value else ""
            elif "несколько" in q["type"]: self.state["saved_replies"][idx] = "; ".join([o for o, cb in checkboxes.items() if cb.value])
            elif "текст" in q["type"]: self.state["saved_replies"][idx] = text_field.value.strip()

        def next_click(e):
            save_reply()
            if not self.state["saved_replies"].get(idx, ""):
                self.show_snack("Пожалуйста, дайте ответ на вопрос!")
                return
            if idx < len(self.state["questions"]) - 1:
                self.state["current_idx"] += 1
                self.render_question_screen()
            else:
                self.finish_test()

        def prev_click(e):
            save_reply(); self.state["current_idx"] -= 1; self.render_question_screen()

        def show_hint_click(e):
            if q["source"]: source_ui.visible = True
            if "один" in q["type"] or "несколько" in q["type"]:
                correct_set = set([o.strip() for o in q["correct"].split(";") if o.strip()])
                if "один" in q["type"]:
                    for r in radio_group.content.controls:
                        if r.value in correct_set or r.value == q["correct"]: r.label = f"✓ {r.label} (ПРАВИЛЬНО)"
                else:
                    for opt, cb in checkboxes.items():
                        if opt in correct_set: cb.label = f"✓ {cb.label} (ПРАВИЛЬНО)"
            elif "текText" in q["type"] or "текст" in q["type"]:
                text_correct_lbl.value = f"Правильный ответ: {q['correct']}"; text_correct_lbl.visible = True
            e.control.disabled = True
            self.page.update()

        def open_confirm_dialog(e):
            def confirm_exit(ev):
                confirm_dialog.open = False
                self.page.update()
                self.finish_test()

            def close_dialog(ev):
                confirm_dialog.open = False
                self.page.update()

            confirm_dialog = AlertDialog(
                title=Text("Предупреждение"),
                content=Text("Вы уверены, что хотите принудительно завершить тестирование? Все оставшиеся вопросы будут засчитаны как неверные."),
                actions=[
                    TextButton("Да, завершить", on_click=confirm_exit, style=ft.ButtonStyle(color="red")),
                    TextButton("Отмена", on_click=close_dialog),
                ],
                actions_alignment=MainAxisAlignment.END,
            )
            
            if hasattr(self.page, "open"):
                self.page.open(confirm_dialog)
            else:
                self.page.dialog = confirm_dialog
                confirm_dialog.open = True
                self.page.update()

        buttons_row = Row(wrap=True, spacing=10, alignment=MainAxisAlignment.START)
        if idx > 0: buttons_row.controls.append(ElevatedButton("Назад", on_click=prev_click, bgcolor="grey400"))
        if config.settings["mode"] == "обучение":
            buttons_row.controls.append(ElevatedButton("Показать верный ответ", on_click=show_hint_click, bgcolor="orange"))
        
        buttons_row.controls.append(
            ElevatedButton("Завершить досрочно", on_click=open_confirm_dialog, bgcolor="red", color="white")
        )
        
        buttons_row.controls.append(ElevatedButton("Завершить" if (idx == len(self.state["questions"]) - 1) else "Далее", on_click=next_click, bgcolor="green", color="white"))
        
        self.page.add(buttons_row)
        self.page.update()

    def finish_test(self):
        self.timer_active = False
        
        self.state["correct_count"] = 0
        self.state["history"] = []
        for i, q in enumerate(self.state["questions"]):
            u_ans = self.state["saved_replies"].get(i, "[Нет ответа]")
            is_correct = False
            
            if u_ans != "[Нет ответа]":
                if "один" in q["type"]: is_correct = (u_ans == q["correct"])
                elif "несколько" in q["type"]: is_correct = (set([o.strip() for o in u_ans.split(";") if o.strip()]) == set([o.strip() for o in q["correct"].split(";") if o.strip()]))
                elif "текст" in q["type"]: is_correct = (u_ans.lower() == q["correct"].lower())
            
            if is_correct: self.state["correct_count"] += 1
            self.state["history"].append((q["text"], u_ans, q["correct"], "Верно" if is_correct else "Неверно", q["source"]))

        status = "Пройден"
        if config.settings["mode"] == "контрольные вопросы" and self.state["correct_count"] < config.settings["passing_score"]:
            status = "Не пройден"

        generate_pdf_report_flet(self.state["user_name"], self.state["correct_count"], len(self.state["questions"]), status, self.state["history"])
        self.page.clean()
        self.page.add(Column([
            Text("Тестирование завершено!", size=22, weight="bold", color="green"),
            Text(f"Сотрудник: {self.state['user_name']}"),
            Text(f"Результат: {self.state['correct_count']} из {len(self.state['questions'])}"),
            Text(f"Статус: {status.upper()}", size=16, weight="bold", color="green" if status == "Пройден" else "red"),
            ElevatedButton("В главное меню", on_click=lambda e: self.render_login_screen(), width=200)
        ], alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER))
        self.page.update()

    def render_admin_screen(self):
        self.page.clean()
        
        self.page.vertical_alignment = "start"
        self.page.horizontal_alignment = "start"
        
        self.page.add(Text("Панель администратора ОВиК", size=20, weight="bold", color="bluegrey800"))
        
        num_q_field = TextField(label="Количество вопросов в тесте", value=str(config.settings["num_questions"]), width=300)
        pass_score_field = TextField(label="Правильных ответов для зачета", value=str(config.settings["passing_score"]), width=300)
        time_limit_field = TextField(label="Время на тест (минуты)", value=str(config.settings["time_limit_minutes"]), width=300)
        
        self.page.add(Text("Настройки параметров теста:", weight="bold"))
        self.page.add(num_q_field, pass_score_field, time_limit_field)
        
        self.page.add(Container(height=10))
        self.page.add(Text("Выберите источники (базы нормативных документов):", weight="bold"))
        
        embedded_questions_dir = os.path.join("assets", "questions")
        if not os.path.exists(embedded_questions_dir):
            embedded_questions_dir = "questions"
            
        source_checkboxes = {}
        checkbox_container = Column(spacing=5)
        
        if os.path.exists(embedded_questions_dir):
            try:
                available_files = [
                    f for f in os.listdir(embedded_questions_dir) 
                    if f.lower().endswith((".dat", ".xlsx"))
                ]
            except Exception:
                available_files = []
            
            for file_name in sorted(available_files):
                display_name = os.path.splitext(file_name)[0]
                
                if not config.SELECTED_SOURCES:
                    is_checked = True
                else:
                    is_checked = (file_name in config.SELECTED_SOURCES)
                    
                cb = Checkbox(label=display_name, value=is_checked)
                source_checkboxes[file_name] = cb
                checkbox_container.controls.append(cb)
        
        if not checkbox_container.controls:
            checkbox_container.controls.append(Text("Доступные файлы источников не найдены!", color="red"))
            
        self.page.add(checkbox_container)
        self.page.add(Container(height=15))
        
        def save_admin_settings(e):
            try:
                config.settings["num_questions"] = int(num_q_field.value)
                config.settings["passing_score"] = int(pass_score_field.value)
                config.settings["time_limit_minutes"] = int(time_limit_field.value)
                
                selected = [file_name for file_name, cb in source_checkboxes.items() if cb.value]
                config.SELECTED_SOURCES = selected
                
                self.render_login_screen()
            except ValueError:
                self.show_snack("Параметры лимитов должны быть числами!")

        self.page.add(ElevatedButton("Сохранить конфигурацию и выйти", on_click=save_admin_settings, bgcolor="blue", color="white", width=350, height=45))
        self.page.update()
