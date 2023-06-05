import flet as ft


class Modal(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.modal = ft.Stack(expand=True)
        self.on_modal_close = None

    def close_modal(self, e):
        self.modal.visible = False
        self.update()
        self.on_modal_close()

    def build(self):
        backdrop = ft.ResponsiveRow(
            [
                ft.Container(
                    expand=True,
                    bgcolor="#000000",
                    ink=False,
                    # SET TRANSPARENT YOU BG DIALOG
                    opacity=0.6,
                    on_click=self.close_modal,
                )
            ]
        )
        window = ft.Container(
            bgcolor="white",
            border_radius=30,
            margin=ft.margin.only(top=80, left=180, right=180),
            height=200,
            alignment=ft.alignment.center,
            content=ft.Text("i am is dialog you", size=20, color="black"),
        )

        self.modal.visible = False
        self.modal.controls.append(backdrop)
        self.modal.controls.append(window)
        return self.modal
