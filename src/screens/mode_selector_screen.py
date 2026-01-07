"""
模式选择屏幕
"""

from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, Select
from textual.binding import Binding


class ModeSelectorScreen(Screen):
    """模式选择屏幕"""

    CSS_PATH = Path(__file__).parent.parent / "style" / "mode_selector_screen.tcss"

    BINDINGS = [
        Binding("escape", "back", "返回"),
        Binding("enter", "confirm", "确认"),
    ]

    def __init__(self):
        super().__init__()
        self.selected_mode = "full"  # 默认选择完整模式
        self.mode_descriptions = {
            "full": "完整模式 - 创建编译脚本 + 安装包生成脚本 (推荐)\n- 生成完整的编译和打包流程\n- 适合需要发布的项目\n- 一站式解决方案",
            "compile": "编译模式 - 仅创建编译脚本\n- 使用 Nuitka/PyInstaller 编译Python项目\n- 生成独立可执行文件\n- 适合只需要编译的场景",
            "package": "打包模式 - 仅创建安装包生成脚本\n- Windows: Inno Setup (.iss)\n- Linux: nfpm (deb/rpm)\n- macOS: 开发中\n- 适合已有可执行文件的项目",
        }

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        with Container(id="mode-container"):
            yield Static("选择构建模式", id="screen-title")
            yield Static("请选择适合您项目的构建模式", id="screen-description")

            # 显示项目信息
            project_name = getattr(self.app, "project_dir", None)
            if project_name:
                yield Static(f"项目: {project_name.name}", id="project-info")

            # 模式选择
            yield Select(
                options=[
                    ("完整模式 (推荐)", "full"),
                    ("编译模式 - 将项目编译为可执行文件", "compile"),
                    ("打包模式 - 将可执行文件打包为安装包", "package"),
                ],
                prompt="选择构建模式",
                allow_blank=False,
                value="full",
                id="mode-select",
            )

            # 详细说明区域
            yield Static(
                self.mode_descriptions.get(self.selected_mode, ""),
                id="mode-description",
            )

            # 按钮
            with Horizontal(id="button-container"):
                yield Button("返回", variant="warning", id="back-btn", flat=True)
                yield Button("下一步", variant="success", id="next-btn", flat=True)

    def on_select_changed(self, event: Select.Changed) -> None:
        """下拉选择变化事件"""
        mode_value = event.value
        if mode_value in ("full", "compile", "package"):
            self.selected_mode = mode_value
            desc = self.mode_descriptions.get(self.selected_mode, "")
            desc_widget = self.query_one("#mode-description", Static)
            desc_widget.update(desc)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击事件"""
        button_id = event.button.id

        if button_id == "back-btn":
            self.action_back()
        elif button_id == "next-btn":
            self.action_confirm()

    def action_back(self) -> None:
        """返回上一屏"""
        self.app.pop_screen()

    def action_confirm(self) -> None:
        """确认选择并进入下一步"""
        self.app.build_mode = self.selected_mode  # type: ignore[assignment]

        mode_names = {
            "full": "完整模式",
            "compile": "编译模式",
            "package": "打包模式",
        }
        self.app.notify(
            f"已选择: {mode_names.get(self.selected_mode, '未知模式')}",
            severity="information",
        )

        if self.selected_mode == "compile":
            from src.screens.compile_config_screen import CompileConfigScreen

            self.app.push_screen(CompileConfigScreen())
        elif self.selected_mode == "full":
            self.app.notify("完整模式配置功能开发中...", severity="warning")
        elif self.selected_mode == "package":
            from src.screens.installer_config_screen import InstallerConfigScreen

            self.app.push_screen(InstallerConfigScreen())
