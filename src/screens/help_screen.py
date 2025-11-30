"""
帮助文档屏幕
"""

from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import MarkdownViewer


class HelpScreen(Screen):
    """帮助文档屏幕"""

    CSS_PATH = Path(__file__).parent.parent / "style" / "help_screen.tcss"
    # 缓存文档路径，避免重复计算
    HELP_PATH = Path(__file__).parent.parent.parent / "docs" / "Tutorial.md"

    BINDINGS = [
        ("escape", "app.pop_screen", "返回"),
    ]

    def compose(self) -> ComposeResult:
        """创建帮助文档界面组件"""
        yield MarkdownViewer(
            id="help-viewer",
            show_table_of_contents=True,
        )

    async def on_mount(self) -> None:
        """挂载后加载文档"""
        viewer = self.query_one("#help-viewer", MarkdownViewer)
        try:
            await viewer.go(self.HELP_PATH)
        except Exception as e:
            viewer.document.update(
                f"# 错误\n\n无法加载文档: {e}\n\n路径: {self.HELP_PATH}"
            )
