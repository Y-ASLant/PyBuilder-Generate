"""
安装包配置屏幕
配置通用的安装包信息（应用名、版本、发布者等）
"""

import asyncio
from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Input, Label, Select
from textual.binding import Binding

from src.utils import (
    load_build_config,
    async_load_build_config,
    async_save_build_config,
)


class InstallerConfigScreen(Screen):
    """安装包配置屏幕 - 通用信息"""

    CSS_PATH = Path(__file__).parent.parent / "style" / "compile_config_screen.tcss"

    BINDINGS = [
        Binding("escape", "back", "返回"),
        Binding("ctrl+s", "save", "保存"),
    ]

    def __init__(self):
        super().__init__()
        self.config = {}
        self.project_dir: Path | None = None

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        with Container(id="config-container"):
            yield Static("安装包配置", id="screen-title")

            # 显示项目信息
            project_dir = getattr(self.app, "project_dir", None)
            if project_dir:
                yield Static(f"项目: {project_dir}", id="project-info")

            # 目标平台选择（独占一行）
            with Vertical(classes="field-group full-width"):
                yield Label("目标平台:", classes="field-label")
                yield Select(
                    options=[
                        ("Windows (Inno Setup)", "windows"),
                        ("Linux (nfpm)", "linux"),
                        ("macOS - 开发中", "macos"),
                    ],
                    prompt="选择目标平台",
                    allow_blank=False,
                    value="windows",
                    id="platform-select",
                    classes="field-select",
                )

            # 两列布局
            with Horizontal(id="fields-container"):
                # 左列
                with Vertical(classes="column"):
                    with Vertical(classes="field-group"):
                        yield Label("应用名称:", classes="field-label")
                        yield Input(
                            placeholder="输入应用名称",
                            id="app-name-input",
                            classes="field-input",
                        )

                    with Vertical(classes="field-group"):
                        yield Label("版本号:", classes="field-label")
                        yield Input(
                            placeholder="例如: 1.0.0",
                            id="version-input",
                            classes="field-input",
                        )

                    with Vertical(classes="field-group"):
                        yield Label("发布者:", classes="field-label")
                        yield Input(
                            placeholder="例如: My Company",
                            id="publisher-input",
                            classes="field-input",
                        )

                # 右列
                with Vertical(classes="column"):
                    with Vertical(classes="field-group"):
                        yield Label("可执行文件名:", classes="field-label")
                        yield Input(
                            placeholder="例如: MyApp.exe",
                            id="exe-name-input",
                            classes="field-input",
                        )

                    with Vertical(classes="field-group"):
                        yield Label("源文件目录:", classes="field-label")
                        yield Input(
                            placeholder="编译输出目录，例如: build",
                            id="source-dir-input",
                            classes="field-input",
                        )

                    with Vertical(classes="field-group"):
                        yield Label("应用网址 (可选):", classes="field-label")
                        yield Input(
                            placeholder="例如: https://example.com",
                            id="url-input",
                            classes="field-input",
                        )

            # 按钮
            with Horizontal(id="button-container"):
                yield Button("返回", variant="warning", id="back-btn", flat=True)
                yield Button("保存配置", variant="primary", id="save-btn", flat=True)
                yield Button("下一步", variant="success", id="next-btn", flat=True)

    async def on_mount(self) -> None:
        """挂载时加载配置"""
        self.project_dir = self.app.project_dir  # type: ignore[assignment]
        if not self.project_dir:
            self.app.notify("未选择项目目录", severity="error")
            self.app.pop_screen()
            return

        self.config = await async_load_build_config(self.project_dir)
        self._load_config_to_ui()

    def _load_config_to_ui(self) -> None:
        """将配置加载到UI"""
        # 从已有配置或编译配置中获取默认值
        app_name = self.config.get("installer_app_name") or self.config.get(
            "project_name", ""
        )
        version = self.config.get("installer_version") or self.config.get(
            "version", "1.0.0"
        )
        publisher = self.config.get("installer_publisher") or self.config.get(
            "company_name", ""
        )
        exe_name = (
            self.config.get("installer_exe_name") or f"{app_name}.exe"
            if app_name
            else ""
        )
        source_dir = self.config.get("installer_source_dir") or self.config.get(
            "output_dir", "build"
        )

        self.query_one("#app-name-input", Input).value = app_name
        self.query_one("#version-input", Input).value = version
        self.query_one("#publisher-input", Input).value = publisher
        self.query_one("#exe-name-input", Input).value = exe_name
        self.query_one("#source-dir-input", Input).value = source_dir
        self.query_one("#url-input", Input).value = self.config.get("installer_url", "")

        # 平台选择
        platform = self.config.get("installer_platform", "windows")
        self.query_one("#platform-select", Select).value = platform

    def _save_config_from_ui(self) -> None:
        """从UI保存配置"""
        existing_config = load_build_config(self.project_dir)  # type: ignore[arg-type]

        existing_config["installer_platform"] = self.query_one(
            "#platform-select", Select
        ).value
        existing_config["installer_app_name"] = self.query_one(
            "#app-name-input", Input
        ).value.strip()
        existing_config["installer_version"] = self.query_one(
            "#version-input", Input
        ).value.strip()
        existing_config["installer_publisher"] = self.query_one(
            "#publisher-input", Input
        ).value.strip()
        existing_config["installer_exe_name"] = self.query_one(
            "#exe-name-input", Input
        ).value.strip()
        existing_config["installer_source_dir"] = self.query_one(
            "#source-dir-input", Input
        ).value.strip()
        existing_config["installer_url"] = self.query_one(
            "#url-input", Input
        ).value.strip()

        self.config = existing_config

    def _validate_config(self) -> tuple[bool, str]:
        """验证配置"""
        if not self.config.get("installer_app_name"):
            return False, "请输入应用名称"
        if not self.config.get("installer_version"):
            return False, "请输入版本号"
        if not self.config.get("installer_exe_name"):
            return False, "请输入可执行文件名"
        if not self.config.get("installer_source_dir"):
            return False, "请输入源文件目录"
        return True, ""

    def _validate_and_save(self) -> bool:
        """验证配置"""
        self._save_config_from_ui()

        is_valid, error_msg = self._validate_config()
        if not is_valid:
            self.app.notify(f"配置验证失败: {error_msg}", severity="error")
            return False

        return True

    async def _async_save_config(self) -> bool:
        """异步保存配置到文件"""
        success = await async_save_build_config(self.project_dir, self.config)  # type: ignore[arg-type]
        if not success:
            self.app.notify("配置保存失败", severity="error")
        return success

    def on_select_changed(self, event: Select.Changed) -> None:
        """处理平台选择变化"""
        if event.select.id == "platform-select":
            if event.value == "macos":
                self.app.notify("macOS 打包功能开发中...", severity="warning")
                # 重置为 windows（需要类型断言）
                select_widget = event.select
                select_widget.value = "windows"  # type: ignore[arg-type]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击"""
        button_id = event.button.id

        if button_id == "back-btn":
            self.action_back()
        elif button_id == "save-btn":
            asyncio.create_task(self.action_save())
        elif button_id == "next-btn":
            asyncio.create_task(self.action_next())

    def action_back(self) -> None:
        """返回上一屏"""
        self.app.pop_screen()

    async def action_save(self) -> None:
        """保存配置"""
        if self._validate_and_save():
            self._save_config_from_ui()
            success = await self._async_save_config()
            if success:
                self.app.notify("配置已保存", severity="information")

    async def action_next(self) -> None:
        """进入下一步：平台专有选项"""
        if not self._validate_and_save():
            return

        self._save_config_from_ui()
        # 异步保存配置
        await self._async_save_config()

        platform = self.config.get("installer_platform", "windows")

        if platform == "windows":
            from src.screens.installer_options_screen import InstallerOptionsScreen

            self.app.push_screen(InstallerOptionsScreen())
        elif platform == "linux":
            self.app.notify("Linux (nfpm) 打包功能开发中...", severity="warning")
        else:
            self.app.notify("macOS 打包功能开发中...", severity="warning")
