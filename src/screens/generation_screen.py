"""
脚本生成进度屏幕
显示生成动画和结果
"""

import asyncio
from pathlib import Path
from typing import Dict, Any
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, LoadingIndicator, Button
from textual.binding import Binding

from src.utils import generate_build_script


class GenerationScreen(Screen):
    """脚本生成进度屏幕"""

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
            yield Static("生成构建脚本", id="generation-title")
            yield LoadingIndicator()
            yield Static("正在生成...", id="generation-status")
            yield Static("", id="generation-result")
            with Horizontal(id="button-container"):
                yield Button("返回", variant="primary", id="back-btn", flat=True)
                yield Button("退出", variant="error", id="exit-btn", flat=True)

    def on_mount(self) -> None:
        """挂载时开始生成"""
        # 初始隐藏按钮
        button_container = self.query_one("#button-container")
        button_container.display = False
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

            # 不自动关闭，等待用户点击按钮

        except Exception as e:
            self.success = False
            self.message = f"生成失败: {e}"
            self._update_result()
            # 不自动关闭，等待用户点击按钮

    def _update_result(self) -> None:
        """更新结果显示"""
        # 隐藏加载指示器
        loading = self.query_one(LoadingIndicator)
        loading.display = False

        # 显示按钮
        button_container = self.query_one("#button-container")
        button_container.display = True

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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击"""
        if event.button.id == "back-btn":
            # 返回到模式选择界面
            self.app.pop_screen()  # 关闭生成进度界面
            self.app.pop_screen()  # 关闭打包选项界面
            self.app.pop_screen()  # 关闭编译配置界面，回到模式选择
        elif event.button.id == "exit-btn":
            # 退出应用
            self.app.exit()

    def action_close(self) -> None:
        """关闭屏幕"""
        self.dismiss(self.success)
