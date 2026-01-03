"""
安装包选项屏幕
配置平台专有的安装包选项（Windows Inno Setup）
"""

from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import (
    Static,
    Button,
    Switch,
    Label,
    Input,
    Select,
    TabbedContent,
    TabPane,
)
from textual.binding import Binding

from src.utils import load_build_config, save_build_config


class InstallerOptionsScreen(Screen):
    """安装包选项屏幕 - Windows Inno Setup"""

    CSS_PATH = Path(__file__).parent.parent / "style" / "package_options_screen.tcss"

    BINDINGS = [
        Binding("escape", "back", "返回"),
        Binding("ctrl+s", "save", "保存"),
    ]

    def __init__(self):
        super().__init__()
        self.config = {}
        self.project_dir: Path = None

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        with Container(id="options-container"):
            yield Static("Windows 安装包选项", id="screen-title")

            # 显示项目信息
            project_dir = getattr(self.app, "project_dir", None)
            if project_dir:
                yield Static(f"项目: {project_dir}", id="project-info")

            with Container(id="options-fields"):
                from textual.widgets import LoadingIndicator
                yield LoadingIndicator(id="loading-indicator")
                yield Static("正在加载配置...", id="loading-text", classes="loading-hint")

            # 按钮
            with Horizontal(id="button-container"):
                yield Button("返回", variant="warning", id="back-btn", flat=True)
                yield Button("保存配置", variant="primary", id="save-btn", flat=True)
                yield Button("生成脚本", variant="success", id="generate-btn", flat=True)

    def on_mount(self) -> None:
        """挂载时加载配置"""
        self.project_dir = self.app.project_dir
        if not self.project_dir:
            self.app.notify("未选择项目目录", severity="error")
            self.app.pop_screen()
            return

        self.call_after_refresh(self._load_and_create_fields)

    def _load_and_create_fields(self) -> None:
        """加载配置并创建字段"""
        try:
            self.config = load_build_config(self.project_dir)
            self._create_options_fields()
        except Exception as e:
            self._show_load_error(str(e))

    def _show_load_error(self, error_msg: str) -> None:
        """显示加载错误"""
        options_container = self.query_one("#options-fields", Container)
        try:
            self.query_one("#loading-indicator").remove()
            self.query_one("#loading-text").remove()
        except Exception:
            pass
        options_container.mount(
            Static(f"加载配置失败\n\n{error_msg}", id="error-message", classes="error-text")
        )

    def _create_switch_widget(self, switch_id: str, label: str, default_value: bool, config_key: str):
        """创建开关组件"""
        return Vertical(
            Horizontal(
                Switch(
                    value=self.config.get(config_key, default_value),
                    id=switch_id,
                    classes="field-switch",
                ),
                Label(label, classes="field-switch-label"),
                classes="field-switch-container",
            ),
            classes="field-group",
        )

    def _create_input_widget(self, input_id: str, label: str, placeholder: str, value: str = ""):
        """创建输入框组件"""
        return Vertical(
            Label(label, classes="field-label"),
            Input(
                value=value,
                placeholder=placeholder,
                id=input_id,
                classes="field-input",
            ),
            classes="field-group",
        )

    def _create_options_fields(self) -> None:
        """创建 Windows Inno Setup 选项字段"""
        options_container = self.query_one("#options-fields", Container)

        # 移除加载指示器
        try:
            self.query_one("#loading-indicator").remove()
            self.query_one("#loading-text").remove()
        except Exception:
            pass

        # ===== 基本选项标签页 =====
        # 第1行：开关选项
        basic_row1 = Horizontal(
            self._create_switch_widget(
                "desktop-icon-switch", "创建桌面快捷方式", True, "installer_desktop_icon"
            ),
            self._create_switch_widget(
                "start-menu-switch", "创建开始菜单项", True, "installer_start_menu"
            ),
            classes="switches-row",
        )

        # 第2行：开关选项
        basic_row2 = Horizontal(
            self._create_switch_widget(
                "add-path-switch", "添加到 PATH 环境变量", False, "installer_add_path"
            ),
            self._create_switch_widget(
                "run-after-switch", "安装后运行程序", True, "installer_run_after"
            ),
            classes="switches-row",
        )

        # 第3行：下拉选择
        basic_row3 = Horizontal(
            Vertical(
                Label("安装权限:", classes="field-label"),
                Select(
                    options=[
                        ("普通用户", "lowest"),
                        ("管理员权限", "admin"),
                        ("用户自选", "dialog"),
                    ],
                    value=self.config.get("installer_privileges", "lowest"),
                    id="privileges-select",
                    classes="field-select",
                    allow_blank=False,
                ),
                classes="field-group",
            ),
            Vertical(
                Label("PATH 作用域:", classes="field-label"),
                Select(
                    options=[
                        ("用户级 (HKCU)", "user"),
                        ("系统级 (HKLM)", "system"),
                    ],
                    value=self.config.get("installer_path_scope", "user"),
                    id="path-scope-select",
                    classes="field-select",
                    allow_blank=False,
                ),
                classes="field-group",
            ),
            classes="inputs-row",
        )

        basic_content = Vertical(
            basic_row1, basic_row2, basic_row3,
            classes="basic-options-content",
        )

        # ===== 输出设置标签页 =====
        output_row1 = Horizontal(
            self._create_input_widget(
                "output-dir-input", "安装包输出目录:",
                "例如: dist/installer",
                self.config.get("installer_output_dir", "dist/installer")
            ),
            self._create_input_widget(
                "icon-input", "图标文件:",
                "例如: assets/app.ico",
                self.config.get("installer_icon", self.config.get("icon_file", ""))
            ),
            classes="inputs-row",
        )

        output_row2 = Horizontal(
            self._create_input_widget(
                "install-dir-input", "默认安装目录 (留空使用 Program Files):",
                "例如: C:\\MyApp",
                self.config.get("installer_install_dir", "")
            ),
            self._create_input_widget(
                "license-input", "许可协议文件 (可选):",
                "例如: LICENSE.txt",
                self.config.get("installer_license", "")
            ),
            classes="inputs-row",
        )

        output_row3 = Horizontal(
            self._create_input_widget(
                "readme-input", "自述文件 (可选):",
                "例如: README.txt",
                self.config.get("installer_readme", "")
            ),
            Vertical(
                Label("压缩方式:", classes="field-label"),
                Select(
                    options=[
                        ("LZMA2 (最高压缩)", "lzma2/ultra64"),
                        ("LZMA (高压缩)", "lzma"),
                        ("ZIP (快速)", "zip"),
                        ("无压缩", "none"),
                    ],
                    value=self.config.get("installer_compression", "lzma2/ultra64"),
                    id="compression-select",
                    classes="field-select",
                    allow_blank=False,
                ),
                classes="field-group",
            ),
            classes="inputs-row",
        )

        # AppId（留空则自动生成）- 显示时去掉花括号
        appid_display = self.config.get("installer_appid", "")
        if isinstance(appid_display, str):
            appid_display = appid_display.strip("{}")
        output_row4 = Horizontal(
            self._create_input_widget(
                "appid-input", "AppId (留空自动生成):",
                "升级时保持一致",
                appid_display
            ),
            Vertical(
                Label("", classes="field-label"),
                Static("", classes="field-input"),
                classes="field-group",
            ),
            classes="inputs-row",
        )

        output_content = Vertical(
            output_row1, output_row2, output_row3, output_row4,
            classes="basic-options-content",
        )

        # 创建标签页
        tabs = TabbedContent(id="installer-tabs")
        tabs.compose_add_child(TabPane("基本选项", basic_content, id="basic-tab"))
        tabs.compose_add_child(TabPane("输出设置", output_content, id="output-tab"))

        options_container.mount(tabs)

    def _save_config_from_ui(self) -> None:
        """从UI保存配置"""
        existing_config = load_build_config(self.project_dir)

        # 基本选项
        existing_config["installer_desktop_icon"] = self.query_one("#desktop-icon-switch", Switch).value
        existing_config["installer_start_menu"] = self.query_one("#start-menu-switch", Switch).value
        existing_config["installer_add_path"] = self.query_one("#add-path-switch", Switch).value
        existing_config["installer_run_after"] = self.query_one("#run-after-switch", Switch).value
        existing_config["installer_privileges"] = self.query_one("#privileges-select", Select).value
        existing_config["installer_path_scope"] = self.query_one("#path-scope-select", Select).value

        # 输出设置
        existing_config["installer_output_dir"] = self.query_one("#output-dir-input", Input).value.strip()
        existing_config["installer_icon"] = self.query_one("#icon-input", Input).value.strip()
        existing_config["installer_install_dir"] = self.query_one("#install-dir-input", Input).value.strip()
        existing_config["installer_compression"] = self.query_one("#compression-select", Select).value
        existing_config["installer_license"] = self.query_one("#license-input", Input).value.strip()
        existing_config["installer_readme"] = self.query_one("#readme-input", Input).value.strip()
        
        # AppId：保存时去掉花括号，只有用户输入了才更新
        appid_input = self.query_one("#appid-input", Input).value.strip().strip("{}")
        if appid_input:
            existing_config["installer_appid"] = appid_input
        # 如果用户没输入，保留 existing_config 中已有的 installer_appid

        self.config = existing_config

    def _validate_and_save(self) -> bool:
        """验证并保存配置"""
        self._save_config_from_ui()

        success = save_build_config(self.project_dir, self.config)
        if not success:
            self.app.notify("配置保存失败", severity="error")
            return False

        return True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击"""
        button_id = event.button.id

        if button_id == "back-btn":
            self.action_back()
        elif button_id == "save-btn":
            self.action_save()
        elif button_id == "generate-btn":
            self.run_worker(self.action_generate())

    def action_back(self) -> None:
        """返回上一屏"""
        try:
            self._save_config_from_ui()
            save_build_config(self.project_dir, self.config)
        except Exception:
            pass
        self.app.pop_screen()

    def action_save(self) -> None:
        """保存配置"""
        if self._validate_and_save():
            self.app.notify("配置已保存", severity="information")

    async def action_generate(self) -> None:
        """生成安装包脚本"""
        if not self._validate_and_save():
            return

        from src.screens.installer_generation_screen import InstallerGenerationScreen

        result = await self.app.push_screen_wait(
            InstallerGenerationScreen(self.config, self.project_dir)
        )

        if result and result[0]:
            # 生成成功，更新 config（包含自动生成的 AppId）
            self.config = result[1]
            save_build_config(self.project_dir, self.config)
            # 更新 UI 中的 AppId 显示
            try:
                appid_input = self.query_one("#appid-input", Input)
                appid_input.value = self.config.get("installer_appid", "").strip("{}")
            except Exception:
                pass
            self.app.notify("脚本生成成功！", severity="information")
        else:
            self.app.notify("脚本生成失败", severity="error")
