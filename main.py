# main.py
import flet as ft
from screens import AppScreens

def main(page: ft.Page):
    # Конфигурация мобильного окна
    page.title = "Тест_ОВ"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.assets_dir = "assets" 
    
    # Инициализация интерфейса
    screens = AppScreens(page)
    screens.render_login_screen()

# Единственная точка входа, которую безошибочно подхватывает контейнер смартфона
app = main
