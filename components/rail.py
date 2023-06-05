import flet as ft


class Rail(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.selected_index = 0

        self.rail = ft.NavigationRail(
            expand=True,
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            # extended=True,
            min_width=100,
            min_extended_width=400,
            # leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.FAVORITE_BORDER,
                    selected_icon=ft.icons.FAVORITE,
                    label="First",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label="Second",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("Settings"),
                ),
            ],
            on_change=self.destination_changed,
        )

    def destination_changed(self, e):
        self.selected_index = e.control.selected_index

    def build(self):
        return self.rail
