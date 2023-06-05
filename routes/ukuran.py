import flet as ft
import sys, os

# setting path
if getattr(sys, "frozen", False):
    app_path = os.path.dirname(sys.executable)
    sys.path.append(app_path)
else:
    app_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append("../components")
from components.table import Table


class Ukuran(ft.UserControl):
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

        self.tambah_btn = ft.ElevatedButton("Tambah", icon=ft.icons.ADD_OUTLINED)
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
                {"label": "Nama", "type": ft.TextField()},
                {
                    "label": "JK",
                    "tooltip": "Jenis Kelamin",
                    "type": ft.Dropdown(options=["Pria", "Wanita"], value="Pria"),
                },
                {"label": "Jurusan", "type": ft.TextField()},
                {"label": "Panjang Baju", "numeric": True, "type": ft.TextField()},
                {"label": "Bahu", "numeric": True, "type": ft.TextField()},
                {"label": "Tangan", "numeric": True, "type": ft.TextField()},
                {"label": "94", "numeric": True, "type": ft.TextField()},
                {
                    "label": "L Tangan",
                    "tooltip": "Lingkar Tangan",
                    "numeric": True,
                    "type": ft.TextField(),
                },
                {
                    "label": "L Dada",
                    "tooltip": "Lingkar Dada",
                    "numeric": True,
                    "type": ft.TextField(),
                },
                {
                    "label": "L Pinggang",
                    "tooltip": "Lingkar Pinggang",
                    "numeric": True,
                    "type": ft.TextField(),
                },
                {
                    "label": "L Pinggul",
                    "tooltip": "Lingkar Pinggul",
                    "numeric": True,
                    "type": ft.TextField(),
                },
                {"label": "Leher", "numeric": True, "type": ft.TextField()},
                {"label": "Catatan Baju", "type": ft.TextField()},
                {"label": "JLH Baju", "tooltip": "Jumlah Baju", "type": ft.TextField()},
                {"label": "Panjang Celana", "numeric": True, "type": ft.TextField()},
                {"label": "Pinggang", "numeric": True, "type": ft.TextField()},
                {"label": "Pesak", "numeric": True, "type": ft.TextField()},
                {"label": "Paha", "numeric": True, "type": ft.TextField()},
                {"label": "Lutut", "numeric": True, "type": ft.TextField()},
                {
                    "label": "L Bawah",
                    "tooltip": "L Bawah",
                    "numeric": True,
                    "type": ft.TextField(),
                },
                {"label": "Pinggul", "numeric": True, "type": ft.TextField()},
                {"label": "Catatan Celana", "type": ft.TextField()},
                {
                    "label": "JLH Celana",
                    "tooltip": "Jumlah Celana",
                    "type": ft.TextField(),
                },
            ]
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
        self.content = ft.Column(
            [self.toolbar, table.view],
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
