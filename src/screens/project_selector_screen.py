"""
项目目录选择屏幕
"""

from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Input, Label, ListItem, ListView
from textual.binding import Binding


class ProjectSelectorScreen(Screen):
    """项目目录选择屏幕"""

    CSS = """
    ProjectSelectorScreen {
        align: center middle;
        overflow: hidden;
    }
    
    #selector-container {
        width: 96;
        height: auto;
        max-height: 30;
        padding: 1 2;
    }
    
    #screen-title {
        width: 100%;
        height: 1;
        color: $primary;
        text-align: center;
        text-style: bold;
        margin-bottom: 0;
    }
    
    #screen-description {
        width: 100%;
        height: 1;
        color: $text-muted;
        text-align: center;
        margin-bottom: 1;
    }
    
    #path-input-container {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }
    
    #path-label {
        color: $text;
        height: 1;
        margin-bottom: 0;
    }
    
    #path-input {
        width: 100%;
        height: 3;
    }
    
    #tree-container {
        width: 100%;
        height: 12;
        border: solid $accent;
        margin: 1 0;
        overflow-y: auto;
    }
    
    ListView {
        width: 100%;
        height: 100%;
        padding: 0;
        scrollbar-size: 1 1;
        scrollbar-size-vertical: 1;
    }
    
    ListItem {
        height: 1;
        padding: 0 1;
    }
    
    .parent-dir {
        color: $warning;
    }
    
    .directory {
        color: $accent;
    }
    
    .file {
        color: $text-muted;
    }
    
    #selected-path {
        width: 100%;
        height: 1;
        color: $success;
        text-align: center;
        margin: 1 0;
    }
    
    #button-container {
        width: 100%;
        height: auto;
        layout: horizontal;
        align: center middle;
        margin-top: 1;
    }
    
    Button {
        margin: 0 2;
        min-width: 16;
        height: 3;
    }
    """

    BINDINGS = [
        Binding("escape", "back", "返回"),
        Binding("enter", "confirm", "确认"),
    ]

    def __init__(self):
        super().__init__()
        self.selected_path: Path = Path.cwd()  # 默认当前目录
        self.current_page = 0  # 当前页面
        self.items_per_page = 12  # 每页显示12条

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        with Container(id="selector-container"):
            yield Static("选择项目目录", id="screen-title")
            yield Static("请选择需要打包的 Python 项目目录", id="screen-description")

            # 路径输入框
            with Vertical(id="path-input-container"):
                yield Label("项目路径:", id="path-label")
                yield Input(
                    placeholder="输入项目路径或从下方选择...",
                    value=str(self.selected_path),
                    id="path-input",
                )

            # 目录列表
            with Container(id="tree-container"):
                yield ListView(id="directory-list")

            # 显示选中的路径
            yield Static(f"选中路径: {self.selected_path}", id="selected-path")

            # 按钮
            with Horizontal(id="button-container"):
                yield Button("返回", variant="warning", id="back-btn", flat=True)
                yield Button("确认", variant="success", id="confirm-btn", flat=True)

    def on_mount(self) -> None:
        """挂载时刷新目录列表"""
        self.refresh_directory_list()

    def refresh_directory_list(self) -> None:
        """刷新目录列表（固定显示12条）"""
        list_view = self.query_one("#directory-list", ListView)
        list_view.clear()

        try:
            # 获取当前目录下的所有项目
            all_items = []

            # 添加 ".." 返回上一级（如果不是根目录）
            parent = self.selected_path.parent
            if parent != self.selected_path:
                parent_item = ListItem(Label("📁 .."), classes="parent-dir")
                parent_item.is_parent = True
                all_items.append(parent_item)

            # 获取目录内容
            try:
                dir_items = []
                for item in self.selected_path.iterdir():
                    dir_items.append(item)
            except PermissionError:
                self.app.notify(f"无权限访问: {self.selected_path}", severity="error")
                return

            # 排序：文件夹在前，文件在后
            dir_items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

            # 添加到列表（只显示前12条，如果有..则显示11条）
            max_items = self.items_per_page - len(all_items)  # 减去..后的剩余数量
            for item in dir_items[:max_items]:
                if item.is_dir():
                    icon = "📁"
                    label = Label(f"{icon} {item.name}")
                    list_item = ListItem(label, classes="directory")
                    list_item.item_path = item
                    all_items.append(list_item)
                else:
                    icon = "📄"
                    label = Label(f"{icon} {item.name}")
                    list_item = ListItem(label, classes="file")
                    list_item.item_path = item
                    all_items.append(list_item)

            # 添加所有项目到ListView
            for item in all_items:
                list_view.append(item)

        except Exception as e:
            self.app.notify(f"读取目录失败: {e}", severity="error")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """列表项选择事件"""
        # 检查是否是父目录项
        if hasattr(event.item, "is_parent") and event.item.is_parent:
            # 点击 ".." 返回上一级
            parent_path = self.selected_path.parent
            if parent_path != self.selected_path:
                self.selected_path = parent_path
                self.update_selected_path()
                self.refresh_directory_list()
        elif hasattr(event.item, "item_path"):
            item_path = event.item.item_path
            if item_path.is_dir():
                # 点击文件夹，进入该目录
                self.selected_path = item_path
                self.update_selected_path()
                self.refresh_directory_list()
            # 文件不做处理

    def on_input_changed(self, event: Input.Changed) -> None:
        """输入框变化事件"""
        if event.input.id == "path-input":
            try:
                path = Path(event.value)
                if path.exists() and path.is_dir():
                    self.selected_path = path
                    self.update_selected_path()
                    self.refresh_directory_list()
            except Exception:
                pass  # 忽略无效路径

    def update_selected_path(self) -> None:
        """更新选中路径显示"""
        selected_label = self.query_one("#selected-path", Static)
        selected_label.update(f"选中路径: {self.selected_path}")

        # 同步到输入框
        path_input = self.query_one("#path-input", Input)
        if path_input.value != str(self.selected_path):
            path_input.value = str(self.selected_path)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击事件"""
        button_id = event.button.id

        if button_id == "back-btn":
            self.action_back()
        elif button_id == "confirm-btn":
            self.action_confirm()

    def action_back(self) -> None:
        """返回上一屏"""
        self.app.pop_screen()

    def action_confirm(self) -> None:
        """确认选择"""
        if not self.selected_path.exists():
            self.app.notify("所选路径不存在，请重新选择", severity="error")
            return

        if not self.selected_path.is_dir():
            self.app.notify("请选择一个目录", severity="error")
            return

        # 保存选中的项目路径到 app
        self.app.project_dir = self.selected_path

        # 跳转到模式选择屏幕
        from src.screens.mode_selector_screen import ModeSelectorScreen

        self.app.notify(
            f"已选择项目: {self.selected_path.name}", severity="information"
        )
        self.app.push_screen(ModeSelectorScreen())
