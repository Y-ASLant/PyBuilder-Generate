"""
插件选择屏幕
用于选择Nuitka编译插件
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, SelectionList
from textual.binding import Binding


class PluginSelectorScreen(Screen):
    """插件选择屏幕"""

    CSS = """
    PluginSelectorScreen {
        align: center middle;
        overflow: hidden;
    }
    
    #plugin-container {
        width: 80;
        height: auto;
        padding: 1 2;
    }
    
    #screen-title {
        width: 100%;
        height: 1;
        color: $primary;
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    
    #plugin-description {
        width: 100%;
        height: auto;
        color: $text-muted;
        text-align: center;
        margin-bottom: 1;
    }
    
    #plugins-list {
        width: 100%;
        height: 20;
        border: solid $accent;
        margin-bottom: 1;
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
        Binding("escape", "cancel", "取消"),
        Binding("enter", "confirm", "确认"),
    ]

    def __init__(self, selected_plugins: list[str] = None):
        super().__init__()
        self.selected_plugins = selected_plugins or []

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        with Container(id="plugin-container"):
            yield Static("选择 Nuitka 插件", id="screen-title")
            yield Static(
                "选择需要启用的插件以确保第三方库的兼容性", id="plugin-description"
            )

            # 常用插件列表
            common_plugins = [
                ("NumPy - 数值计算库", "numpy"),
                ("PyTorch - 深度学习框架", "torch"),
                ("TensorFlow - 深度学习框架", "tensorflow"),
                ("Matplotlib - 数据可视化", "matplotlib"),
                ("Tkinter - GUI工具包", "tk-inter"),
                ("PySide6 - Qt6 GUI框架", "pyside6"),
                ("PyQt5 - Qt5 GUI框架", "pyqt5"),
                ("Multiprocessing - 多进程支持", "multiprocessing"),
                ("Anti-bloat - 移除不必要依赖", "anti-bloat"),
                ("Pandas - 数据分析库", "pandas"),
                ("Pillow - 图像处理库", "pillow"),
                ("SciPy - 科学计算库", "scipy"),
            ]

            yield SelectionList[str](
                *[
                    (name, value, value in self.selected_plugins)
                    for name, value in common_plugins
                ],
                id="plugins-list",
            )

            # 按钮
            with Horizontal(id="button-container"):
                yield Button("取消", variant="warning", id="cancel-btn", flat=True)
                yield Button("确认", variant="success", id="confirm-btn", flat=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击事件"""
        button_id = event.button.id

        if button_id == "cancel-btn":
            self.action_cancel()
        elif button_id == "confirm-btn":
            self.action_confirm()

    def action_cancel(self) -> None:
        """取消并返回"""
        self.dismiss(None)

    def action_confirm(self) -> None:
        """确认选择并返回"""
        plugins_list = self.query_one("#plugins-list", SelectionList)
        selected = list(plugins_list.selected)
        self.dismiss(selected)
