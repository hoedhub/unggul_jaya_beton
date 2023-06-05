import flet as ft

from components.appbar import AppBar

# from components.modal import Modal
from components.rail import Rail
from components.alert import Dialog

from routes.login import LoginForm
from routes.pekerjaan import Pekerjaan


def main(page: ft.Page):
    page.padding = 0

    appbar = AppBar(title="UNGGUL JAYA BETON")

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

    #

    # setup snack bar untuk parent
    def open_snack(content):
        page.snack_bar = ft.SnackBar(content)
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
    session = False

    def logging():
        global session
        session = True
        app.content = logged_in
        appbar.login()
        page.update()

    def loggedout():
        global session
        session = False
        app.content = logged_out.form
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
    logged_out = LoginForm()
    logged_out.logging = logging
    app = ft.Container(expand=True)
    app.content = logged_out.form
    page.add(app)
    appbar.change_theme(ft.ThemeMode.DARK)


ft.app(target=main)
