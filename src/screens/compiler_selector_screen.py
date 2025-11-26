"""
编译器选择屏幕
用于选择Nuitka编译器
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, ListView, ListItem, Label
from textual.binding import Binding


class CompilerSelectorScreen(Screen):
    """编译器选择屏幕"""

    CSS = """
    CompilerSelectorScreen {
        align: center middle;
        overflow: hidden;
    }
    
    #compiler-container {
        width: 60;
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
    
    #compiler-description {
        width: 100%;
        height: auto;
        color: $text-muted;
        text-align: center;
        margin-bottom: 1;
    }
    
    #compiler-list {
        width: 100%;
        height: 16;
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

    def __init__(self, selected_compiler: str = "msvc"):
        super().__init__()
        self.selected_compiler = selected_compiler

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        with Container(id="compiler-container"):
            yield Static("选择 C 编译器", id="screen-title")
            yield Static(
                "选择用于 Nuitka 编译的 C 编译器",
                id="compiler-description"
            )

            # Windows平台编译器列表
            compilers = [
                ("MSVC - Visual Studio (推荐)", "msvc"),
                ("MinGW64 - GCC for Windows", "mingw64"),
                ("Clang-cl - Clang (MSVC兼容)", "clang-cl"),
                ("Clang - LLVM (MinGW)", "clang"),
            ]

            # 根据当前选择设置初始索引
            initial_index = 0
            for i, (_, value) in enumerate(compilers):
                if value == self.selected_compiler:
                    initial_index = i
                    break

            yield ListView(
                *[ListItem(Label(name), id=f"{value}-item") for name, value in compilers],
                id="compiler-list",
                initial_index=initial_index,
            )

            # 按钮
            with Horizontal(id="button-container"):
                yield Button("取消", variant="warning", id="cancel-btn", flat=True)
                yield Button("确认", variant="success", id="confirm-btn", flat=True)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """处理ListView选择事件"""
        item_id = event.item.id
        if item_id == "msvc-item":
            self.selected_compiler = "msvc"
        elif item_id == "mingw64-item":
            self.selected_compiler = "mingw64"
        elif item_id == "clang-cl-item":
            self.selected_compiler = "clang-cl"
        elif item_id == "clang-item":
            self.selected_compiler = "clang"

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
        self.dismiss(self.selected_compiler)
