import flet as ft
import sys, os

from com_table import Table


class Pekerjaan(ft.UserControl):
    def __init__(self):
        super().__init__()

        # setup alert dari halaman pekerjaan
        self.alert_props = {
            "title": "Mohon Konfirmasi",
            "content": "Anda yakin?",
            "actions": [
                ft.TextButton("Ya", on_click=lambda e: self.yes_alert()),
                ft.TextButton("Tidak", on_click=lambda e: self.no_alert()),
            ],
        }
        self.alert_dismiss = None

        # setup snackbar dari halaman pekerjaan
        self.snack_bar_content = ft.Text(
            "Berhasil dihapus", weight="bold", color=ft.colors.GREEN_400
        )

        def toggle_form():
            pekerjaan_view.visible = not pekerjaan_view.visible
            form.visible = not form.visible
            pekerjaan_view.update()
            form.update()
            pass

        self.tambah_btn = ft.ElevatedButton(
            "Tambah", icon=ft.icons.ADD_OUTLINED, on_click=lambda e: toggle_form()
        )
        self.hapus_btn = ft.ElevatedButton("Hapus", icon=ft.icons.REMOVE_OUTLINED)

        def filter_tf_change():
            self.clearer.visible = len(self.filter_tf.value) > 0
            self.clearer.update()

        self.filter_tf = ft.TextField(
            label="Cari", on_change=lambda e: filter_tf_change()
        )
        self.filter_dd = ft.Dropdown(label="Di kolom")

        def clear_filter_tf():
            self.filter_tf.value = ""
            self.filter_tf.update()
            filter_tf_change()

        self.clearer = ft.Container(
            content=ft.IconButton(ft.icons.CLEAR, on_click=lambda e: clear_filter_tf()),
            width=38,
            height=38,
            right=4,
            top=8,
            visible=False,
        )

        table = Table(
            columns=[
                {"label": "Nama Pekerjaan", "type": ft.TextField()},
                {"label": "Alokasi Dana", "numeric": True, "type": ft.TextField()},
                {
                    "label": "Ditambahkan",
                    "tooltip": "Kapan pekerjaan ditambahkan",
                    "numeric": True,
                    "type": ft.Text(),
                },
            ]
        )
        form = ft.Container(visible=False)
        pekerjaan_baru = ft.TextField(label="Nama Pekerjaan")
        pengalokasian_dana = ft.TextField(label="Dana yang dialokasikan")
        form_fields = ft.Column([pekerjaan_baru, pengalokasian_dana])
        form_actions = ft.Row(
            [
                ft.TextButton("Simpan dan Tambah Baru"),
                ft.TextButton("Simpan dan Tututp"),
                ft.TextButton("Batal", on_click=lambda e: toggle_form()),
            ],
            alignment=ft.MainAxisAlignment.END,
        )
        form.content = ft.Column(
            [
                ft.Text("Tambah Pekerjaan Baru", size=ft.TextThemeStyle.DISPLAY_LARGE),
                form_fields,
                form_actions,
            ],
            spacing=20,
        )

        self.toolbar = ft.Row(
            [
                # CRUD tool
                ft.Row([self.tambah_btn, self.hapus_btn]),
                # display tool
                ft.Row(
                    [
                        ft.Stack(
                            [
                                self.filter_tf,
                                self.clearer,
                            ]
                        ),
                        self.filter_dd,
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        # ft.ElevatedButton("Alert", on_click=lambda e: self.alert())
        pekerjaan_view = ft.Column(
            [
                self.toolbar,
                table.view,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        )
        self.content = ft.Column(
            [
                pekerjaan_view,
                form,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        )

    # methods untuk alert
    def alert(self):
        pass

    def yes_alert(self):
        print("Ya")
        self.alert_dismiss()
        self.open_snack_bar()

    def no_alert(self):
        print("Tidak")
        self.alert_dismiss()

    def open_snack_bar(self):
        pass

    def build(self):
        return self
