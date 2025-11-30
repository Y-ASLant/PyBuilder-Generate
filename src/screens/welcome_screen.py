"""
欢迎屏幕
"""

import pyfiglet
from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Link


def generate_logo(text="PyBuilder", font="big"):
    """使用 pyfiglet 生成 ASCII Logo"""
    try:
        return pyfiglet.figlet_format(text, font=font)
    except Exception:
        # PyInstaller 打包后 pyfiglet.fonts 模块缺失时的降级方案
        return f"\n  {text}  \n"


# 动态生成 ASCII Logo - 延迟生成避免打包时导入错误
# 可选字体（从小到大）：
# "small" - 最小字体
# "standard" - 标准字体
# "big" - 大字体
# "banner" - 横幅样式
# "block" - 块状字体（较大）
# "3-d" - 3D效果（最大）


class WelcomeScreen(Screen):
    """欢迎屏幕"""

    CSS_PATH = Path(__file__).parent.parent / "style" / "welcome_screen.tcss"

    def compose(self) -> ComposeResult:
        """创建欢迎界面组件"""
        # 运行时生成 LOGO，避免模块导入阶段错误
        logo = generate_logo("PyBuilder", "big")

        with Container(id="welcome-container"):
            yield Static(logo, id="logo")
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
