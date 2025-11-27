"""
打包选项配置屏幕
配置编译打包的详细选项
"""

from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Switch, Label, Input
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
    
    .field-label {
        color: $text;
        height: 1;
        margin-bottom: 0;
    }
    
    .field-input {
        width: 100%;
        height: 3;
    }
    
    #jobs-input {
        width: 30;
        height: 3;
    }
    
    #jobs-decrease-btn, #jobs-increase-btn {
        min-width: 5;
        width: 5;
        height: 3;
        margin: 0 0 0 1;
        padding: 0;
    }
    
    #plugins-button, #compiler-button {
        width: 100%;
        margin: 0;
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
        self.selected_plugins: list[str] = []  # 存储选中的插件
        # 根据平台设置默认编译器
        import platform

        os_type = platform.system()
        if os_type == "Windows":
            self.selected_compiler = "msvc"
        elif os_type == "Linux":
            self.selected_compiler = "gcc"
        else:  # macOS
            self.selected_compiler = "clang"

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

        # 加载插件配置
        plugins_value = self.config.get("plugins", "")
        if isinstance(plugins_value, str):
            self.selected_plugins = [
                p.strip() for p in plugins_value.split(",") if p.strip()
            ]
        else:
            self.selected_plugins = (
                plugins_value if isinstance(plugins_value, list) else []
            )

        # 加载编译器配置
        self.selected_compiler = self.config.get("compiler", "msvc")

        # 根据构庻工具动态生成选项（开关值已在创庻时设置）
        self._create_options_fields()

    def _create_switch_widget(
        self, switch_id: str, label: str, default_value: bool, config_key: str
    ):
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

    def _create_input_widget(
        self, input_id: str, label: str, config_key: str, placeholder: str
    ):
        """创建输入框组件的辅助方法"""
        return Vertical(
            Label(label, classes="field-label"),
            Input(
                value=self.config.get(config_key, ""),
                placeholder=placeholder,
                id=input_id,
                classes="field-input",
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

        # Nuitka特有选项
        if build_tool == "nuitka":
            # 左列第1行：C编译器选择
            left_widgets.append(
                Vertical(
                    Label("C 编译器:", classes="field-label"),
                    Button(
                        "选择编译器...",
                        id="compiler-button",
                        variant="primary",
                        flat=True,
                    ),
                    classes="field-group",
                )
            )
            # 右列第1行：插件支持
            right_widgets.append(
                Vertical(
                    Label("启用插件:", classes="field-label"),
                    Button(
                        "选择插件...",
                        id="plugins-button",
                        variant="primary",
                        flat=True,
                    ),
                    classes="field-group",
                )
            )
            # 左列第2行：独立打包
            left_widgets.append(
                self._create_switch_widget(
                    "standalone-switch", "独立打包 (Standalone)", True, "standalone"
                )
            )
            # 右列第2行：Python优化（从字符串转换为布尔值）
            python_flag_value = bool(self.config.get("python_flag", ""))
            right_widgets.append(
                Vertical(
                    Horizontal(
                        Switch(
                            value=python_flag_value,
                            id="python-flag-switch",
                            classes="field-switch",
                        ),
                        Label(
                            "Python优化 (移除断言和文档)", classes="field-switch-label"
                        ),
                        classes="field-switch-container",
                    ),
                    classes="field-group",
                )
            )
            # 左列第3行：LTO优化
            left_widgets.append(
                self._create_switch_widget(
                    "lto-switch", "链接时优化 (LTO)", False, "lto"
                )
            )
            # 左列第4行：单文件模式
            left_widgets.append(
                self._create_switch_widget(
                    "onefile-switch", "单文件模式 (One File)", True, "onefile"
                )
            )
            # 左列第5行：静默输出（合并静默模式和显示进度条）
            left_widgets.append(
                self._create_switch_widget(
                    "quiet-switch", "静默输出 (仅进度条)", False, "quiet_mode"
                )
            )
            # 右列第3行：显示控制台窗口
            right_widgets.append(
                self._create_switch_widget(
                    "console-switch", "显示终端窗口 (Windows)", False, "show_console"
                )
            )
            # 右列第4行：移除构建文件
            right_widgets.append(
                self._create_switch_widget(
                    "remove-output-switch",
                    "移除构建文件 (节省空间)",
                    True,
                    "remove_output",
                )
            )
            # 右列第5行：编译线程
            right_widgets.append(
                Vertical(
                    Horizontal(
                        Input(
                            placeholder="编译线程 (默认: 4)",
                            value=str(self.config.get("jobs", 4)),
                            id="jobs-input",
                            classes="field-input",
                        ),
                        Button(
                            "-", id="jobs-decrease-btn", variant="default", flat=True
                        ),
                        Button(
                            "+", id="jobs-increase-btn", variant="default", flat=True
                        ),
                        classes="field-switch-container",
                    ),
                    classes="field-group",
                )
            )

        # PyInstaller特有选项
        if build_tool == "pyinstaller":
            # 左列：清理临时文件
            left_widgets.append(
                self._create_switch_widget(
                    "clean-switch", "清理临时文件", True, "clean"
                )
            )
            # 左列：静默输出
            left_widgets.append(
                self._create_switch_widget(
                    "quiet-switch", "静默输出 (仅进度条)", False, "quiet_mode"
                )
            )
            # 左列：_internal 目录名称
            left_widgets.append(
                self._create_input_widget(
                    "contents-dir-input",
                    "内部目录名称:",
                    "contents_directory",
                    "_internal (默认为 .)",
                )
            )
            # 右列：调试模式
            right_widgets.append(
                self._create_switch_widget(
                    "debug-switch", "调试模式 (输出详细信息)", False, "debug"
                )
            )
            # 右列：UAC 管理员权限
            right_widgets.append(
                self._create_switch_widget(
                    "uac-admin-switch", "管理员权限 (Windows UAC)", False, "uac_admin"
                )
            )

            # 左列：隐藏导入
            left_widgets.append(
                self._create_input_widget(
                    "hidden-imports-input",
                    "隐藏导入 (支持空格、中英文逗号分隔):",
                    "hidden_imports",
                    "例如: PIL numpy.core pandas",
                )
            )

            # 右列：排除模块
            right_widgets.append(
                self._create_input_widget(
                    "exclude-modules-input",
                    "排除模块 (支持空格、中英文逗号分隔):",
                    "exclude_modules",
                    "例如: tkinter test unittest",
                )
            )

            # 左列：添加数据文件
            left_widgets.append(
                self._create_input_widget(
                    "add-data-input",
                    "数据文件 (支持空格、中英文逗号分隔):",
                    "add_data",
                    "格式: src;dest 多个用空格",
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

        # Nuitka特有选项
        if build_tool == "nuitka":
            # Nuitka 通用选项
            existing_config["onefile"] = self.query_one("#onefile-switch", Switch).value
            existing_config["show_console"] = self.query_one(
                "#console-switch", Switch
            ).value
            # 静默模式配置
            quiet_mode = self.query_one("#quiet-switch", Switch).value
            existing_config["quiet_mode"] = quiet_mode
            existing_config["show_progress"] = not quiet_mode

            # Nuitka 特有选项
            existing_config["standalone"] = self.query_one(
                "#standalone-switch", Switch
            ).value
            existing_config["remove_output"] = self.query_one(
                "#remove-output-switch", Switch
            ).value
            existing_config["lto"] = self.query_one("#lto-switch", Switch).value
            # 并行编译任务数
            jobs_value = self.query_one("#jobs-input", Input).value
            try:
                existing_config["jobs"] = int(jobs_value) if jobs_value else 4
            except ValueError:
                existing_config["jobs"] = 4
            # Python优化标志（开关转换为字符串）
            python_opt = self.query_one("#python-flag-switch", Switch).value
            existing_config["python_flag"] = "-O" if python_opt else ""
            # 插件支持 - 使用存储的插件列表
            existing_config["plugins"] = (
                ",".join(self.selected_plugins) if self.selected_plugins else ""
            )
            # C编译器
            existing_config["compiler"] = self.selected_compiler

        # PyInstaller特有选项
        if build_tool == "pyinstaller":
            # 静默模式配置
            quiet_mode = self.query_one("#quiet-switch", Switch).value
            existing_config["quiet_mode"] = quiet_mode
            existing_config["show_progressbar"] = not quiet_mode

            # PyInstaller 特有选项
            existing_config["clean"] = self.query_one("#clean-switch", Switch).value
            existing_config["debug"] = self.query_one("#debug-switch", Switch).value

            # 内部目录名称
            contents_dir = self.query_one("#contents-dir-input", Input).value.strip()
            existing_config["contents_directory"] = (
                contents_dir if contents_dir else "."
            )

            # UAC 管理员权限
            existing_config["uac_admin"] = self.query_one(
                "#uac-admin-switch", Switch
            ).value

            # 隐藏导入
            existing_config["hidden_imports"] = self.query_one(
                "#hidden-imports-input", Input
            ).value.strip()

            # 排除模块
            existing_config["exclude_modules"] = self.query_one(
                "#exclude-modules-input", Input
            ).value.strip()

            # 添加数据文件
            existing_config["add_data"] = self.query_one(
                "#add-data-input", Input
            ).value.strip()

        # 保持列表字段
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
            self.run_worker(self.action_generate())
        elif button_id == "plugins-button":
            self.run_worker(self.action_select_plugins())
        elif button_id == "compiler-button":
            self.run_worker(self.action_select_compiler())
        elif button_id == "jobs-decrease-btn":
            self._adjust_jobs(-1)
        elif button_id == "jobs-increase-btn":
            self._adjust_jobs(1)

    def _adjust_jobs(self, delta: int) -> None:
        """调整编译线程数"""
        jobs_input = self.query_one("#jobs-input", Input)
        try:
            current_value = int(jobs_input.value) if jobs_input.value else 4
        except ValueError:
            current_value = 4

        # 计算新值，最小为1
        new_value = max(1, current_value + delta)
        jobs_input.value = str(new_value)

    def action_back(self) -> None:
        """返回上一屏"""
        # 返回前自动保存配置
        try:
            self._save_config_from_ui()
            save_build_config(self.project_dir, self.config)
        except Exception as e:
            # 显示保存失败的错误信息
            self.app.notify(f"保存配置失败: {str(e)}", severity="error")
        self.app.pop_screen()

    async def action_select_plugins(self) -> None:
        """打开插件选择界面"""
        from src.screens.plugin_selector_screen import PluginSelectorScreen

        # 打开插件选择界面并等待结果
        result = await self.app.push_screen_wait(
            PluginSelectorScreen(self.selected_plugins)
        )

        # 如果用户确认选择（不是取消），更新插件列表
        if result is not None:
            self.selected_plugins = result
            plugin_count = len(result)
            self.app.notify(f"已选择 {plugin_count} 个插件", severity="information")

    async def action_select_compiler(self) -> None:
        """打开编译器选择界面"""
        from src.screens.compiler_selector_screen import CompilerSelectorScreen

        # 打开编译器选择界面并等待结果
        result = await self.app.push_screen_wait(
            CompilerSelectorScreen(self.selected_compiler)
        )

        # 如果用户确认选择（不是取消），更新编译器
        if result is not None:
            self.selected_compiler = result
            compiler_names = {
                "msvc": "MSVC (Visual Studio)",
                "mingw64": "MinGW64",
                "clang-cl": "Clang-cl",
                "clang": "Clang",
                "gcc": "GCC",
            }
            compiler_name = compiler_names.get(result, result)
            self.app.notify(f"已选择编译器: {compiler_name}", severity="information")

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

    async def action_generate(self) -> None:
        """生成编译脚本"""
        if not self._validate_and_save():
            return

        # 打开生成进度界面
        from src.screens.generation_screen import GenerationScreen

        result = await self.app.push_screen_wait(
            GenerationScreen(self.config, self.project_dir)
        )

        if result:
            self.app.notify("脚本生成成功！", severity="information")
        else:
            self.app.notify("脚本生成失败", severity="error")
