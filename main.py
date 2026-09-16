# main.py
import flet as ft
from screens import AppScreens

def main(page: ft.Page):
    # Жестко прописываем мобильные параметры страницы
    page.title = "Тест_ОВ"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Указываем правильный системный путь к ассетам внутри APK
    page.assets_dir = "assets" 
    
    # Запускаем экраны приложения
    screens = AppScreens(page)
    screens.render_login_screen()

if __name__ == "__main__":
    # ИСПРАВЛЕНИЕ: Новый стандарт запуска во Flet 1.0.0 для исключения AttributeError
    ft.run_app(main)
