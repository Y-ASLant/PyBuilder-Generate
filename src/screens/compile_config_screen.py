"""
编译配置屏幕
用于配置 PyInstaller 和 Nuitka 的编译选项
"""

from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Input, Select, Label

from src.screens.base_config_screen import BaseConfigScreen
from src.utils import load_build_config


class CompileConfigScreen(BaseConfigScreen):
    """编译配置屏幕"""

    CSS_PATH = Path(__file__).parent.parent / "style" / "compile_config_screen.tcss"

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        with Container(id="config-container"):
            yield Static("编译配置", id="screen-title")

            # 显示项目信息（compose 时 project_dir 尚未初始化，使用 getattr）
            project_dir = getattr(self.app, "project_dir", None)
            if project_dir:
                yield Static(f"项目: {project_dir}", id="project-info")

            # 构建工具（独占一行）
            with Vertical(classes="field-group full-width"):
                yield Label("构建工具:", classes="field-label")
                yield Select(
                    options=[
                        ("PyInstaller", "pyinstaller"),
                        ("Nuitka", "nuitka"),
                    ],
                    prompt="选择构建工具",
                    allow_blank=False,
                    value="pyinstaller",
                    id="build-tool-select",
                    classes="field-select",
                )

            # 两列布局
            with Horizontal(id="fields-container"):
                # 左列
                with Vertical(classes="column"):
                    with Vertical(classes="field-group"):
                        yield Label("项目名称:", classes="field-label")
                        yield Input(
                            placeholder="输入项目名称",
                            id="project-name-input",
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
                        yield Label("公司名称 (可选):", classes="field-label")
                        yield Input(
                            placeholder="例如: My Company",
                            id="company-name-input",
                            classes="field-input",
                        )

                # 右列
                with Vertical(classes="column"):
                    with Vertical(classes="field-group"):
                        yield Label("输出目录:", classes="field-label")
                        yield Input(
                            placeholder="相对路径，如: dist 或 build",
                            id="output-dir-input",
                            classes="field-input",
                        )

                    with Vertical(classes="field-group"):
                        yield Label("入口文件:", classes="field-label")
                        yield Input(
                            placeholder="相对于项目根目录，如: main.py",
                            id="entry-file-input",
                            classes="field-input",
                        )

                    with Vertical(classes="field-group"):
                        yield Label("图标文件 (可选):", classes="field-label")
                        yield Input(
                            placeholder=".ico/.icns (Windows/macOS)，如: assets/icon.ico",
                            id="icon-file-input",
                            classes="field-input",
                        )

            # 按钮
            with Horizontal(id="button-container"):
                yield Button("返回", variant="warning", id="back-btn", flat=True)
                yield Button("保存配置", variant="primary", id="save-btn", flat=True)
                yield Button("下一步", variant="success", id="next-btn", flat=True)

    def _load_config_to_ui(self) -> None:
        """将配置加载到UI"""
        # 基本信息
        self.query_one("#project-name-input", Input).value = self.config.get(
            "project_name", ""
        )
        self.query_one("#version-input", Input).value = self.config.get("version", "")
        self.query_one("#company-name-input", Input).value = self.config.get(
            "company_name", ""
        )
        self.query_one("#entry-file-input", Input).value = self.config.get(
            "entry_file", ""
        )
        self.query_one("#icon-file-input", Input).value = self.config.get(
            "icon_file", ""
        )

        # 构建工具
        build_tool = self.config.get("build_tool", "pyinstaller")
        self.query_one("#build-tool-select", Select).value = build_tool

        # 输出目录
        self.query_one("#output-dir-input", Input).value = self.config.get(
            "output_dir", ""
        )

    def _save_config_from_ui(self) -> None:
        """从UI保存配置（只更新编译配置字段，保留打包选项）"""
        # 先加载现有配置，保留打包选项字段
        existing_config = load_build_config(self.project_dir)  # type: ignore[arg-type]

        # 只更新编译配置相关的字段
        existing_config["project_name"] = self.query_one(
            "#project-name-input", Input
        ).value
        existing_config["version"] = self.query_one("#version-input", Input).value
        existing_config["company_name"] = self.query_one(
            "#company-name-input", Input
        ).value
        existing_config["entry_file"] = self.query_one("#entry-file-input", Input).value
        existing_config["icon_file"] = self.query_one("#icon-file-input", Input).value
        existing_config["build_tool"] = self.query_one(
            "#build-tool-select", Select
        ).value
        existing_config["output_dir"] = self.query_one("#output-dir-input", Input).value

        # 保持列表字段
        if "plugins" not in existing_config:
            existing_config["plugins"] = []
        if "exclude_packages" not in existing_config:
            existing_config["exclude_packages"] = []

        # 更新self.config为完整配置
        self.config = existing_config

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击事件"""
        button_id = event.button.id

        if button_id == "back-btn":
            self.action_back()
        elif button_id == "save-btn":
            self.action_save()
        elif button_id == "next-btn":
            await self._action_next()

    async def _action_next(self) -> None:
        """进入下一步：打包选项配置"""
        if not self._validate_and_save():
            return

        # 异步保存配置
        await self._async_save_config()

        # 跳转到打包选项配置
        from src.screens.package_options_screen import PackageOptionsScreen

        self.app.push_screen(PackageOptionsScreen())
