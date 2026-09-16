# main.py
import flet as ft
from screens import AppScreens

def main(page: ft.Page):
    # Установка базовых мобильных параметров страницы
    page.title = "Тест_ОВ"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Указываем путь к папке с зашифрованными вопросами и шрифтами
    page.assets_dir = "assets" 
    
    # Инициализируем и отрисовываем стартовый экран авторизации сотрудников
    screens = AppScreens(page)
    screens.render_login_screen()

# ДЛЯ ИСКЛЮЧЕНИЯ ATTRIBUTEERROR: Новейший стандарт инициализации мобильного контейнера serious_python
app = main

if __name__ == "__main__":
    # Официальный запуск для Flet 1.0.0, работающий без вылетов
    ft.run_app(main)
