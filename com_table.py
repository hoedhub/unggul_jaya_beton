import flet as ft


class Table(ft.UserControl):
    def __init__(self, columns=None):
        super().__init__()

        def rowsperpage_change():
            pass

        self.rowsperpage_dd = ft.Dropdown(
            # hint_text="Jumlah baris yang ditampilkan per halaman",
            options=[
                ft.dropdown.Option(10),
                ft.dropdown.Option(20),
                ft.dropdown.Option(50),
                ft.dropdown.Option(100),
            ],
            value=20,
            width=96,
            on_change=lambda e: rowsperpage_change(),
            autofocus=True,
        )

        self.rowsperpage = ft.Row(
            [
                self.rowsperpage_dd,
                ft.Text("rowsperpage"),
            ]
        )

        def to_page(page):
            self.table_data.current_page = page
            # if int(self.page.value) == page:
            #   self.page.value = page
            self.page.value = page
            self.control.update()
            # update_rows()

        def prev_page(e):
            if self.table_data.current_page == 1:
                return
            to_page(self.page.value - 1)

        def next_page(e):
            if self.table_data.current_page >= len(self.page.options):
                return
            to_page(self.page.value + 1)

        self.page = ft.Dropdown(
            # options=update_hal(),
            value=1,
            width=56,
            on_change=lambda e: to_page(int(e.control.value)),
        )

        self.paging = ft.Row(
            [
                ft.IconButton(
                    tooltip="Previous page",
                    icon=ft.icons.SKIP_PREVIOUS_OUTLINED,
                    on_click=prev_page,
                ),
                ft.Text("Hal ke"),
                self.page,
                ft.Text("dari 1 halaman"),
                ft.IconButton(
                    tooltip="Next page",
                    icon=ft.icons.SKIP_NEXT_OUTLINED,
                    on_click=next_page,
                ),
            ]
        )

        self.info = ft.Text("0 rows")

        self.page_control = ft.Container(
            ft.Row(
                [self.rowsperpage, self.paging, self.info],
                spacing=2,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.all(4),
        )

        self.table = ft.DataTable(
            sort_column_index=0,
            sort_ascending=True,
            # heading_row_color=ft.colors.BLACK12,
            heading_row_height=70,
            data_row_color={"hovered": "0x30FF0000"},
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=100,
            # columns=[
            #     ft.DataColumn(ft.Text("First name")),
            #     ft.DataColumn(ft.Text("Last name")),
            #     ft.DataColumn(ft.Text("Age"), numeric=True),
            # ],
            # rows=[
            #     ft.DataRow(
            #         cells=[
            #             ft.DataCell(ft.Text("John")),
            #             ft.DataCell(ft.Text("Smith")),
            #             ft.DataCell(ft.Text("43")),
            #         ],
            #     ),
            #     ft.DataRow(
            #         cells=[
            #             ft.DataCell(ft.Text("Jack")),
            #             ft.DataCell(ft.Text("Brown")),
            #             ft.DataCell(ft.Text("19")),
            #         ],
            #     ),
            # ],
            expand=True,
        )

        def sort_column(e):
            self.table.sort_ascending = (
                not self.table.sort_ascending
                if self.table.sort_column_index == e.column_index
                else e.ascending
            )
            self.table.sort_column_index = e.column_index
            print(f"control: {e.column_index}, {e.ascending}")
            self.table.update()
            print(f"table: {self.table.sort_column_index}, {self.table.sort_ascending}")

        self.types = []
        if columns is not None:
            try:
                for id, column in enumerate(columns):
                    tooltip = column["tooltip"] if "tooltip" in column else None
                    numeric = column["numeric"] if "numeric" in column else False
                    self.table.columns.append(
                        ft.DataColumn(
                            ft.Text(column["label"], weight="bold"),
                            tooltip=tooltip,
                            numeric=numeric,
                            on_sort=lambda e: sort_column(e),
                        )
                    )
                    type = column["type"] if "type" in column else ft.Text()
                    self.types.append(type)
            except:
                print(f"columns elements not recognized: {columns}")

        self.empty = ft.Text(
            "NO DATA",
            italic=True,
            text_align=ft.TextAlign.CENTER,
            size=ft.TextThemeStyle.DISPLAY_LARGE,
            # top=60,
            expand=True,
        )

        self.view = ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Stack(
                                    [
                                        self.table,
                                    ],
                                ),
                                self.empty,
                            ],
                            scroll=ft.ScrollMode.AUTO,
                            # expand=True,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                self.page_control,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        )

    def append_rows(self, data):
        for row in data:
            cells = []
            for id, v in enumerate(row.values()):
                self.types[id].visible = False
                cells.append(
                    ft.Stack(
                        [
                            ft.TextButton(
                                v, on_click=lambda e: print(f"{e.control.text} clicked")
                            ),
                            self.types[id],
                        ]
                    )
                )
            self.table.rows.append(
                ft.DataRow(
                    cells=cells,
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                )
            )
        self.empty.visible = len(self.table.rows) <= 0

    def build(self):
        return self
