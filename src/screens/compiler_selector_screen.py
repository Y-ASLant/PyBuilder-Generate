"""
编译器选择屏幕
用于选择Nuitka编译器
"""

import platform
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, ListView, ListItem, Label
from textual.binding import Binding


class CompilerSelectorScreen(Screen):
    """编译器选择屏幕"""

    # 各平台编译器选项
    COMPILERS = {
        "Windows": [
            ("MSVC - Visual Studio (推荐)", "msvc"),
            ("MinGW64 - GCC for Windows", "mingw64"),
            ("Clang-cl - Clang (MSVC兼容)", "clang-cl"),
            ("Clang - LLVM (跨平台通用)", "clang"),
        ],
        "Linux": [
            ("GCC - 系统默认 (推荐)", "gcc"),
            ("Clang - LLVM编译器 (跨平台通用)", "clang"),
        ],
        "Darwin": [  # macOS
            ("Clang - Xcode默认 (推荐, 跨平台通用)", "clang"),
            ("GCC - GNU编译器", "gcc"),
        ],
    }

    # 默认编译器
    DEFAULT_COMPILER = {
        "Windows": "msvc",
        "Linux": "gcc",
        "Darwin": "clang",
    }

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

    def __init__(self, selected_compiler: str = None):
        super().__init__()
        self.os_type = platform.system()
        # 根据平台设置默认编译器
        if selected_compiler is None:
            selected_compiler = self.DEFAULT_COMPILER.get(self.os_type, "gcc")
        self.selected_compiler = selected_compiler

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        # 获取当前平台的编译器列表
        compilers = self.COMPILERS.get(self.os_type, self.COMPILERS["Linux"])
        
        # 平台名称映射
        platform_names = {
            "Windows": "Windows",
            "Linux": "Linux",
            "Darwin": "macOS",
        }
        platform_name = platform_names.get(self.os_type, "Unknown")
        
        with Container(id="compiler-container"):
            yield Static("选择 C 编译器", id="screen-title")
            yield Static(
                f"选择用于 Nuitka 编译的 C 编译器 ({platform_name})",
                id="compiler-description"
            )

            # 查找初始索引
            initial_index = next(
                (i for i, (_, value) in enumerate(compilers) if value == self.selected_compiler),
                0
            )

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
        # 从item id中提取编译器名称（移除"-item"后缀）
        if event.item.id and event.item.id.endswith("-item"):
            self.selected_compiler = event.item.id[:-5]

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
