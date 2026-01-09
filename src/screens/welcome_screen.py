"""
欢迎屏幕
"""

from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Link, Static
from src.widgets.figlet_widget import FigletWidget


class WelcomeScreen(Screen):
    """欢迎屏幕"""

    CSS_PATH = Path(__file__).parent.parent / "style" / "welcome_screen.tcss"

    def compose(self) -> ComposeResult:
        """创建欢迎界面组件"""
        with Container(id="welcome-container"):
            yield FigletWidget("PyBuilder", id="logo", font="big")
            with Container(id="title"):
                yield Link(
                    "Github Star.", url="https://github.com/Y-ASLant/PyBuilder-Generate"
                )
            yield Static(
                "Cross-Platform Python Build Script Generator Tools", id="subtitle"
            )
            yield Static("智能化 | 现代化 | 高效 | 跨平台", id="description")

            with Vertical(classes="button-container"):
                with Horizontal(classes="button-row"):
                    yield Button("开始使用", variant="success", id="start", flat=True)
                    yield Button(
                        "帮助文档",
                        variant="primary",
                        id="help",
                        flat=True,
                    )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击事件"""
        button_id = event.button.id

        if button_id == "start":
            # 跳转到项目选择屏幕
            from src.screens.project_selector_screen import (
                ProjectSelectorScreen,
            )

            self.app.push_screen(ProjectSelectorScreen())

        elif button_id == "help":
            # 跳转到帮助文档屏幕
            from src.screens.help_screen import HelpScreen

            self.app.push_screen(HelpScreen())
