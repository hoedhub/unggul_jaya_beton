import flet as ft


class Dialog(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.title = "Please Confirm"
        self.content = "Are you sure?"
        self.actions = [
            ft.TextButton("Yes", on_click=lambda e: self.close_dlg()),
            ft.TextButton("No", on_click=lambda e: self.close_dlg()),
        ]
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(self.title),
            content=ft.Text(self.content),
            actions=self.actions,
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self.update_page = None

    def update_dialog(self, props=None):
        if props is not None:
            self.dialog.title.value = props["title"]
            self.dialog.content.value = props["content"]
            self.dialog.actions = list(props["actions"])
            self.dialog.update()

    def open_dlg(self):
        self.dialog.open = True
        self.page.update()

    def close_dlg(self):
        self.dialog.open = False
        self.update_page()

    def build(self):
        return self
