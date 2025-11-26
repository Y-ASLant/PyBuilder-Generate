"""
打包选项配置屏幕
配置编译打包的详细选项
"""

from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Switch, Label
from textual.binding import Binding

from src.utils import (
    load_build_config,
    save_build_config,
    validate_build_config,
)


class PackageOptionsScreen(Screen):
    """打包选项配置屏幕"""

    CSS = """
    PackageOptionsScreen {
        align: center middle;
        overflow: hidden;
    }
    
    #options-container {
        width: 100;
        height: auto;
        padding: 1 2;
    }
    
    #screen-title {
        width: 100%;
        height: 1;
        color: $primary;
        text-align: center;
        text-style: bold;
        margin-bottom: 0;
    }
    
    
    #project-info {
        width: 100%;
        height: 1;
        color: $accent;
        text-align: center;
        margin-bottom: 1;
    }
    
    #options-fields {
        width: 100%;
        height: auto;
    }
    
    .options-columns {
        width: 100%;
        height: auto;
        layout: horizontal;
    }
    
    .option-column {
        width: 50%;
        height: auto;
        padding: 0 1;
    }
    
    .field-group {
        width: 100%;
        height: auto;
        margin: 0 0 1 0;
    }
    
    .field-switch-container {
        width: 100%;
        height: auto;
        layout: horizontal;
        align-vertical: middle;
    }
    
    .field-switch {
        margin: 0 1 0 0;
    }
    
    .field-switch-label {
        color: $text;
        padding-top: 1;
    }
    
    #button-container {
        width: 100%;
        height: auto;
        layout: horizontal;
        align: center middle;
        margin-top: 1;
    }
    
    Button {
        margin: 0 2;
        min-width: 16;
        height: 3;
    }
    """

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
            yield Static("打包选项", id="screen-title")

            # 显示项目信息
            project_dir = getattr(self.app, "project_dir", None)
            if project_dir:
                yield Static(f"项目: {project_dir}", id="project-info")

            # 选项容器（将在on_mount中动态填充）
            yield Container(id="options-fields")

            # 按钮
            with Horizontal(id="button-container"):
                yield Button("返回", variant="warning", id="back-btn", flat=True)
                yield Button("保存配置", variant="primary", id="save-btn", flat=True)
                yield Button(
                    "生成脚本", variant="success", id="generate-btn", flat=True
                )

    def on_mount(self) -> None:
        """挂载时加载配置"""
        self.project_dir = self.app.project_dir
        if not self.project_dir:
            self.app.notify("未选择项目目录", severity="error")
            self.app.pop_screen()
            return

        # 加载现有配置或使用默认配置
        self.config = load_build_config(self.project_dir)

        # 根据构建工具动态生成选项（开关值已在创建时设置）
        self._create_options_fields()

    def _create_switch_widget(self, switch_id: str, label: str, default_value: bool, config_key: str):
        """创建开关组件的辅助方法"""
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

    def _create_options_fields(self) -> None:
        """根据构建工具创建选项字段"""
        build_tool = self.config.get("build_tool", "nuitka")
        options_container = self.query_one("#options-fields", Container)

        # 创建左列和右列的组件列表
        left_widgets = []
        right_widgets = []

        # Nuitka特有选项：独立打包
        if build_tool == "nuitka":
            left_widgets.append(
                self._create_switch_widget(
                    "standalone-switch", "独立打包 (Standalone)", True, "standalone"
                )
            )

        # 通用选项：单文件模式
        onefile_widget = self._create_switch_widget(
            "onefile-switch", "单文件模式 (One File)", True, "onefile"
        )
        (left_widgets if build_tool == "nuitka" else right_widgets).append(onefile_widget)

        # 通用选项：显示控制台
        right_widgets.append(
            self._create_switch_widget(
                "console-switch", "显示控制台窗口", False, "show_console"
            )
        )

        # 通用选项：静默模式
        left_widgets.append(
            self._create_switch_widget(
                "quiet-switch", "静默模式 (减少输出)", False, "quiet_mode"
            )
        )

        # Nuitka特有选项
        if build_tool == "nuitka":
            right_widgets.append(
                self._create_switch_widget(
                    "remove-output-switch", "移除构建文件 (节省空间)", True, "remove_output"
                )
            )
            left_widgets.append(
                self._create_switch_widget(
                    "progressbar-switch", "显示进度条", True, "show_progressbar"
                )
            )

        # PyInstaller特有选项
        if build_tool == "pyinstaller":
            left_widgets.append(
                self._create_switch_widget(
                    "clean-switch", "清理临时文件", True, "clean"
                )
            )
            right_widgets.append(
                self._create_switch_widget(
                    "debug-switch", "调试模式 (输出详细信息)", False, "debug"
                )
            )

        # 创建两列容器并一次性挂载所有组件
        left_column = Vertical(*left_widgets, classes="option-column")
        right_column = Vertical(*right_widgets, classes="option-column")
        two_columns = Horizontal(left_column, right_column, classes="options-columns")

        options_container.mount(two_columns)

    def _save_config_from_ui(self) -> None:
        """从UI保存配置（只更新打包选项字段，保留编译配置）"""
        # 先加载现有配置，保留编译配置字段
        existing_config = load_build_config(self.project_dir)
        build_tool = existing_config.get("build_tool", "nuitka")

        # 只更新打包选项相关的字段
        # Nuitka特有：独立打包
        if build_tool == "nuitka":
            existing_config["standalone"] = self.query_one(
                "#standalone-switch", Switch
            ).value

        # 通用选项
        existing_config["onefile"] = self.query_one("#onefile-switch", Switch).value
        existing_config["show_console"] = self.query_one(
            "#console-switch", Switch
        ).value
        existing_config["quiet_mode"] = self.query_one("#quiet-switch", Switch).value

        # Nuitka特有选项
        if build_tool == "nuitka":
            existing_config["remove_output"] = self.query_one(
                "#remove-output-switch", Switch
            ).value
            existing_config["show_progressbar"] = self.query_one(
                "#progressbar-switch", Switch
            ).value

        # PyInstaller特有选项
        if build_tool == "pyinstaller":
            existing_config["clean"] = self.query_one("#clean-switch", Switch).value
            existing_config["debug"] = self.query_one("#debug-switch", Switch).value

        # 保持列表字段
        if "plugins" not in existing_config:
            existing_config["plugins"] = []
        if "exclude_packages" not in existing_config:
            existing_config["exclude_packages"] = []

        # 更新self.config为完整配置
        self.config = existing_config

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击事件"""
        button_id = event.button.id

        if button_id == "back-btn":
            self.action_back()
        elif button_id == "save-btn":
            self.action_save()
        elif button_id == "generate-btn":
            self.action_generate()

    def action_back(self) -> None:
        """返回上一屏"""
        self.app.pop_screen()

    def _validate_and_save(self) -> bool:
        """验证并保存配置，返回是否成功"""
        self._save_config_from_ui()

        # 验证配置
        is_valid, error_msg = validate_build_config(self.config, self.project_dir)
        if not is_valid:
            self.app.notify(f"配置验证失败: {error_msg}", severity="error")
            return False

        # 保存到文件
        success = save_build_config(self.project_dir, self.config)
        if not success:
            self.app.notify("配置保存失败", severity="error")
            return False

        return True

    def action_save(self) -> None:
        """保存配置"""
        if self._validate_and_save():
            self.app.notify("配置已保存", severity="information")

    def action_generate(self) -> None:
        """生成编译脚本"""
        if not self._validate_and_save():
            return

        # TODO: 生成编译脚本
        self.app.notify("生成编译脚本功能开发中...", severity="warning")
