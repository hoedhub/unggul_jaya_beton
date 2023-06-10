import flet as ft


class AppBar(ft.UserControl):
    def __init__(self, title="AppBar Example", img_src="assets/logo.png", height=56):
        super().__init__()

        self.switcher = ft.Switch(on_change=lambda e: self.change_theme())
        theme_switch = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.SUNNY,
                    on_click=lambda e: self.change_theme(ft.ThemeMode.LIGHT),
                ),
                self.switcher,
                ft.IconButton(
                    ft.icons.NIGHTLIGHT,
                    on_click=lambda e: self.change_theme(ft.ThemeMode.DARK),
                ),
            ],
            spacing=1,
        )
        self.loggedout = False
        self.logout_btn = ft.Row(
            [
                ft.IconButton(
                    tooltip="Keluar",
                    icon=ft.icons.LOGOUT,
                    on_click=lambda e: self.loggedout(),
                ),
                ft.VerticalDivider(),
            ],
            visible=False,
        )

        self.actions = ft.Row(
            [
                self.logout_btn,
                theme_switch,
                ft.Text(""),
            ]
        )

        self.toolbar = ft.AppBar(
            leading=ft.Row(
                [
                    ft.Icon(),
                    ft.Image(
                        src=img_src,
                        # width=40,
                        height=40,
                        fit=ft.ImageFit.FIT_HEIGHT,
                    ),
                ],
                spacing=0,
            ),  # ft.Icon(ft.icons.PALETTE),
            leading_width=40,
            title=ft.Row(
                [
                    ft.Text(""),
                    ft.Text(title),
                ]
            ),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            elevation=112,
            toolbar_height=height,
            actions=[
                # ft.IconButton(
                #     ft.icons.WB_SUNNY_OUTLINED, on_click=lambda e: self.change_theme()
                # ),
                self.actions
                # ft.IconButton(ft.icons.FILTER_3),
                # ft.PopupMenuButton(
                #     items=[
                #         ft.PopupMenuItem(text="Item 1"),
                #         ft.PopupMenuItem(),  # divider
                #         ft.PopupMenuItem(
                #             text="Checked item", checked=False, on_click=check_item_clicked
                #         ),
                #     ]
                # ),
            ],
        )
        self.theme_mode = ft.ThemeMode.LIGHT

    def change_theme(self, theme=None):
        if not theme == None:
            if not self.theme_mode == theme:
                self.switcher.value = not self.switcher.value

        self.theme_mode = (
            theme
            if not theme == None
            else (
                ft.ThemeMode.LIGHT
                if self.theme_mode == ft.ThemeMode.DARK
                else ft.ThemeMode.DARK
            )
        )
        self.theme_changed()

    # should be handled from the parent
    def theme_changed(self):
        pass

    def login(self):
        self.logout_btn.visible = True
        self.logout_btn.update()

    def loggedout(self):
        pass

    def logout(self):
        self.logout_btn.visible = False
        self.logout_btn.update()

    def build(self):
        return self
