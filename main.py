import flet as ft
import os

# database imports
from db_ujb import CurrentUser

from com_appbar import AppBar

# from components.modal import Modal
from com_rail import Rail
from com_alert import Dialog

from route_login import LoginForm
from route_pekerjaan import Pekerjaan


def main(page: ft.Page):
    page.padding = 0

    appbar = AppBar(title="", img_src="assets/unggul-jaya-beton-logo-white.png")

    def change_theme():
        page.theme_mode = appbar.theme_mode
        page.update()

    appbar.theme_changed = change_theme
    page.appbar = appbar.toolbar
    #

    # setup alert untuk parent
    # modal = Modal()

    # def modal_closed():
    #     page.update()

    # modal.on_modal_close = modal_closed

    alert = Dialog()
    alert.update_page = lambda: page.update()

    def open_dlg(
        props=None,  # ={"title": alert.title, "content": alert.content, "actions": alert.actions}
    ):
        page.dialog = alert.dialog
        alert.dialog.open = True
        page.update()

        alert.update_dialog(props)
        page.update()

    #

    # setup snack bar untuk parent
    def open_snack(text, action=None):
        if action is None:
            page.snack_bar = ft.SnackBar(ft.Text(text))
        else:
            page.snack_bar = ft.SnackBar(ft.Text(text), action=action)

        page.snack_bar.open = True
        page.update()

    #

    # routing
    rail = Rail()

    def destination_changed(e):
        print("Selected destination:", e.control.selected_index)
        match e.control.selected_index:
            case 1:
                # setup alert untuk halaman pekerjaan
                pekerjaan.alert_dismiss = lambda: alert.close_dlg()
                pekerjaan.alert = lambda: open_dlg(props=pekerjaan.alert_props)

                pekerjaan.open_snack_bar = lambda: open_snack(
                    pekerjaan.snack_bar_content
                )

                body.content = pekerjaan.content
            case 2:
                # modal.modal.visible = True
                # modal.update()
                open_dlg()
            case _:
                body.content = ft.Text("Home!")

        body.update()
        # page.update()

    rail.rail.on_change = destination_changed

    # routes
    pekerjaan = Pekerjaan()
    #

    # app container
    body = ft.Container(
        ft.Text("Body!"),
        alignment=ft.alignment.top_left,
        expand=True,
        margin=ft.margin.all(10),
        # bgcolor=ft.colors.AMBER_100,
    )

    # Create an instance of DBlite
    ujb = CurrentUser()

    def logging():
        ujb.login_user(login.username.value, login.password.value)
        if ujb.username is None:
            # Failed login
            open_dlg(
                props={
                    "title": "ERROR",
                    "content": "Invalid username or password!",
                    "actions": [
                        ft.TextButton("Try again", on_click=lambda e: alert.close_dlg())
                    ],
                }
            )
            print(f"Invalid creds!")
            return
        else:
            # Successful login
            login.username.value = ""
            login.password.value = ""
            app.content = logged_in
            appbar.login()
            # app.update()
            open_snack("Login successful")

    def loggedout():
        ujb.logout_user()
        app.content = login.form
        appbar.logout()
        page.update()

    appbar.loggedout = loggedout

    logged_in = ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            body,
        ],
        expand=True,
    )

    login = LoginForm()
    login.logging = logging
    app = ft.Container(expand=True)
    app.content = login.form
    page.add(app)
    appbar.change_theme(ft.ThemeMode.DARK)


ft.app(target=main)
