import flet as ft
from screens import AppScreens

def main(page: ft.Page):
    app = AppScreens(page)
    
    def on_disconnect(e):
        # Если пользователь закрыл приложение или свернул, глушим фоновые потоки
        app.timer_active = False

    page.on_disconnect = on_disconnect
    app.render_login_screen()

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
