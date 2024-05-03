import os
import time
from stat import S_ISDIR, S_ISREG

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, DataTable


class FileCommander(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [
        # Binding(key="f1", action="help", key_display="F1", description="Help"),
        # Binding(key="f2", action="menu", key_display="F2", description="Menu"),
        # Binding(key="f3", action="view", key_display="F3", description="View"),
        # Binding(key="f4", action="edit", key_display="F4", description="Edit"),
        # Binding(key="f5", action="copy", key_display="F5", description="Copy"),
        # Binding(key="f6", action="renmov", key_display="F6", description="RenMov"),
        # Binding(key="f7", action="mkdir", key_display="F7", description="Mkdir"),
        # Binding(key="f8", action="delete", key_display="F8", description="Delete"),
        # Binding(key="f9", action="pulldn", key_display="F9", description="PullDn"),
        Binding(key="f10", action="quit", key_display="F10", description="Quit")
    ]

    header = Header(show_clock=True)
    dtLeftPanel = DataTable(id="app-panel-left", classes="box")
    dtLeftPanelFolder = os.getcwd()
    dtRightPanel = DataTable(id="app-panel-right", classes="box")
    dtRightPanelFolder = os.getcwd()
    footer = Footer()

    def compose(self) -> ComposeResult:
        yield self.header
        yield self.dtLeftPanel
        yield self.dtRightPanel
        yield self.footer

    def init_components(self):
        self.screen.styles.background = "darkblue"
        self.screen.styles.border = ("heavy", "white")

        self.dtLeftPanel.border_title = "Path: "
        self.dtLeftPanel.border_subtitle = self.dtLeftPanelFolder
        self.dtLeftPanel.cursor_type = "row"
        self.datatable_add_columns(self.dtLeftPanel)
        self.load_panel_items(self.dtLeftPanel, self.dtLeftPanelFolder)

        self.dtRightPanel.border_title = "Path: "
        self.dtRightPanel.border_subtitle = self.dtRightPanelFolder
        self.dtRightPanel.cursor_type = "row"
        self.datatable_add_columns(self.dtRightPanel)
        self.load_panel_items(self.dtRightPanel, self.dtRightPanelFolder)

    def datatable_add_columns(self, dt: DataTable):
        dt.add_column(
            label="Name",
            width=30
        )
        dt.add_column(
            label="Size"
        )
        dt.add_column(
            label="Perms"
        )
        dt.add_column(
            label="Modify"
        )

    def on_mount(self) -> None:
        self.title = "File Commander"
        self.init_components()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        row = event.data_table.get_row(event.row_key)

        if event.data_table.id == "app-panel-left":
            try:
                if row[0] != "..":
                    new_path = self.dtLeftPanelFolder + "/" + row[0]
                else:
                    new_path = os.path.dirname(self.dtLeftPanelFolder)
                if os.path.isdir(new_path):
                    self.dtLeftPanelFolder = new_path
                    self.dtLeftPanel.border_subtitle = self.dtLeftPanelFolder
                    self.dtLeftPanel.clear()
                    self.load_panel_items(self.dtLeftPanel, self.dtLeftPanelFolder)
            except Exception:
                self.dtLeftPanel.border_subtitle = "Can't load folder data"

        if event.data_table.id == "app-panel-right":
            try:
                if row[0] != "..":
                    new_path = self.dtRightPanelFolder + "/" + row[0]
                else:
                    new_path = os.path.dirname(self.dtRightPanelFolder)
                if os.path.isdir(new_path):
                    self.dtRightPanelFolder = new_path
                    self.dtRightPanel.border_subtitle = self.dtRightPanelFolder
                    self.dtRightPanel.clear()
                    self.load_panel_items(self.dtRightPanel, self.dtRightPanelFolder)
            except Exception:
                self.dtRightPanel.border_subtitle = "Can't load folder data"

    def load_panel_items(self, dt: DataTable, folder: str) -> list:
        for item in self.get_folder_items(folder):
            dt.add_row(*item)

    def get_folder_items(self, folder: str):
        folders = []
        files = []
        for item in [folder] + os.listdir(folder):
            try:
                pathname = os.path.join(folder, item)
                stat = os.stat(pathname)
                mode = stat.st_mode
                size = stat.st_size
                if item != "/":
                    if item == folder:
                        item = ".."
                    if S_ISDIR(mode):
                        folders.append([item, "DIR", oct(mode)[-3:], time.ctime(stat.st_mtime)])
                    elif S_ISREG(mode):
                        files.append([item, size, oct(mode)[-3:], time.ctime(stat.st_mtime)])
            except Exception:
                pass
        return sorted(folders) + sorted(files)


if __name__ == "__main__":
    app = FileCommander()
    app.run()
