"""
安装包脚本生成进度屏幕
"""

import asyncio
from pathlib import Path
from typing import Dict, Any
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, LoadingIndicator, Button
from textual.binding import Binding

from src.utils.installer_generator import generate_installer_script


class InstallerGenerationScreen(Screen):
    """安装包脚本生成进度屏幕"""

    CSS_PATH = Path(__file__).parent.parent / "style" / "generation_screen.tcss"

    BINDINGS = [
        Binding("escape", "close", "关闭", show=False),
    ]

    def __init__(self, config: Dict[str, Any], project_dir: Path):
        super().__init__()
        self.config = config
        self.project_dir = project_dir
        self.success = False
        self.message = ""

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        with Container(id="generation-container"):
            yield Static("生成安装包脚本", id="generation-title")
            yield LoadingIndicator()
            yield Static("正在生成...", id="generation-status")
            yield Static("", id="generation-result")
            with Horizontal(id="button-container"):
                yield Button("返回", variant="primary", id="back-btn", flat=True)
                yield Button("退出", variant="error", id="exit-btn", flat=True)

    def on_mount(self) -> None:
        """挂载时开始生成"""
        button_container = self.query_one("#button-container")
        button_container.display = False
        self.call_later(self._start_generation)

    def _start_generation(self) -> None:
        """开始生成脚本"""
        self.run_worker(self._generate_script(), exclusive=True)

    async def _generate_script(self) -> None:
        """异步生成脚本"""
        try:
            await asyncio.sleep(1.5)

            success, message = generate_installer_script(self.config, self.project_dir)

            self.success = success
            self.message = message

            self._update_result()

        except Exception as e:
            self.success = False
            self.message = f"生成失败: {e}"
            self._update_result()

    def _update_result(self) -> None:
        """更新结果显示"""
        loading = self.query_one(LoadingIndicator)
        loading.display = False

        button_container = self.query_one("#button-container")
        button_container.display = True

        status = self.query_one("#generation-status", Static)
        if self.success:
            status.update("生成成功！")
            status.styles.color = "green"
        else:
            status.update("生成失败")
            status.styles.color = "red"

        result = self.query_one("#generation-result", Static)
        result.update(self.message)
        if self.success:
            result.styles.color = "white"
        else:
            result.styles.color = "red"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击"""
        if event.button.id == "back-btn":
            # 返回时传递更新后的 config（包含自动生成的 AppId）
            self.dismiss((self.success, self.config))
        elif event.button.id == "exit-btn":
            self.app.exit()

    def action_close(self) -> None:
        """关闭屏幕"""
        self.dismiss((self.success, self.config))
