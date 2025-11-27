"""
脚本生成进度屏幕
显示生成动画和结果
"""

import asyncio
from pathlib import Path
from typing import Dict, Any
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Static, LoadingIndicator
from textual.binding import Binding

from src.utils import generate_build_script


class GenerationScreen(Screen):
    """脚本生成进度屏幕"""

    CSS = """
    GenerationScreen {
        align: center middle;
        background: $surface;
    }
    
    #generation-container {
        width: 60;
        height: auto;
        padding: 2 4;
        background: $panel;
        border: solid $accent;
    }
    
    #generation-title {
        width: 100%;
        height: 1;
        color: $primary;
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    
    #generation-status {
        width: 100%;
        height: 1;
        color: $text;
        text-align: center;
        margin: 1 0;
    }
    
    #generation-result {
        width: 100%;
        height: auto;
        color: $success;
        text-align: center;
        margin-top: 1;
    }
    
    LoadingIndicator {
        height: 3;
        margin: 1 0;
    }
    """

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
            yield Static("生成构建脚本", id="generation-title")
            yield LoadingIndicator()
            yield Static("正在生成...", id="generation-status")
            yield Static("", id="generation-result")

    def on_mount(self) -> None:
        """挂载时开始生成"""
        # 使用 call_later 延迟执行，确保界面已渲染
        self.call_later(self._start_generation)

    def _start_generation(self) -> None:
        """开始生成脚本"""
        self.run_worker(self._generate_script(), exclusive=True)

    async def _generate_script(self) -> None:
        """异步生成脚本"""
        try:
            # 显示生成动画至少 1.5 秒
            await asyncio.sleep(1.5)

            # 生成脚本
            success, message = generate_build_script(self.config, self.project_dir)

            self.success = success
            self.message = message

            # 更新界面
            self._update_result()

            # 延迟关闭
            await asyncio.sleep(1.0)
            self.dismiss(success)

        except Exception as e:
            self.success = False
            self.message = f"生成失败: {e}"
            self._update_result()
            await asyncio.sleep(2.0)
            self.dismiss(False)

    def _update_result(self) -> None:
        """更新结果显示"""
        # 隐藏加载指示器
        loading = self.query_one(LoadingIndicator)
        loading.display = False

        # 更新状态文本
        status = self.query_one("#generation-status", Static)
        if self.success:
            status.update("生成成功！")
            status.styles.color = "green"
        else:
            status.update("生成失败")
            status.styles.color = "red"

        # 显示详细消息
        result = self.query_one("#generation-result", Static)
        result.update(self.message)
        if self.success:
            result.styles.color = "white"
        else:
            result.styles.color = "red"

    def action_close(self) -> None:
        """关闭屏幕"""
        self.dismiss(self.success)
