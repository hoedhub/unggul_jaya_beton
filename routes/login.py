import flet as ft


class LoginForm(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.username = ft.TextField(
            label="Username",
            border_radius=ft.border_radius.only(top_right=20, bottom_left=20),
        )
        self.password = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            border_radius=ft.border_radius.only(top_right=20, bottom_left=20),
        )
        self.form = ft.Row(
            [
                ft.Container(
                    ft.Column(
                        [
                            self.username,
                            self.password,
                            ft.Icon(size=3),
                            ft.ElevatedButton(
                                "Masuk",
                                icon=ft.icons.LOGIN_OUTLINED,
                                height=50,
                                on_click=lambda e: self.logging(),
                            ),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        spacing=20,
                    ),
                    width=300,
                )
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def logging(self):
        pass

    def build(self):
        return self
