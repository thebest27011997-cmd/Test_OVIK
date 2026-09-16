# main.py
import flet as ft
from screens import AppScreens

def main(page: ft.Page):
    page.title = "Тест_ОВ"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.assets_dir = "assets" 
    
    screens = AppScreens(page)
    screens.render_login_screen()

# Универсальная точка входа для мобильного контейнера
app = main

if __name__ == "__main__":
    ft.app(target=main)
