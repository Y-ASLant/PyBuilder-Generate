"""
帮助文档屏幕
"""

from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import MarkdownViewer, LoadingIndicator, Static
from textual.containers import Container


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
        # 添加容器，先显示加载动画
        with Container(id="help-container"):
            # 加载状态
            yield LoadingIndicator(id="help-loading")
            yield Static("正在加载帮助文档...", id="help-loading-text")
            # 文档查看器（初始隐藏）
            yield MarkdownViewer(
                id="help-viewer",
                show_table_of_contents=True,
                classes="hidden",
            )

    async def on_mount(self) -> None:
        """挂载后加载文档"""
        # 异步加载文档
        self.call_after_refresh(self._load_document)
    
    async def _load_document(self) -> None:
        """异步加载文档内容"""
        viewer = self.query_one("#help-viewer", MarkdownViewer)
        try:
            # 加载文档
            await viewer.go(self.HELP_PATH)
        except Exception as e:
            # 显示错误信息
            viewer.document.update(
                f"# 加载失败\n\n无法加载文档: {e}\n\n路径: {self.HELP_PATH}"
            )
        finally:
            # 移除加载指示器（无论成功或失败都执行）
            try:
                self.query_one("#help-loading").remove()
                self.query_one("#help-loading-text").remove()
            except Exception:
                pass
            # 显示文档
            viewer.remove_class("hidden")
