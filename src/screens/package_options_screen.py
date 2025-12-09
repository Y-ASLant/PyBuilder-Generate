"""
打包选项配置屏幕
配置编译打包的详细选项
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
    TabbedContent,
    TabPane,
    Select,
)
from textual.binding import Binding

from src.utils import (
    load_build_config,
    save_build_config,
    validate_build_config,
)


class PackageOptionsScreen(Screen):
    """打包选项配置屏幕"""

    CSS_PATH = Path(__file__).parent.parent / "style" / "package_options_screen.tcss"

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
            # 添加加载指示器和提示文本
            with Container(id="options-fields"):
                from textual.widgets import LoadingIndicator
                yield LoadingIndicator(id="loading-indicator")
                yield Static("正在加载配置...", id="loading-text", classes="loading-hint")

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

        # 使用异步加载，避免阻塞渲染
        self.call_after_refresh(self._load_and_create_fields)
    
    def _load_and_create_fields(self) -> None:
        """异步加载配置并创建字段"""
        try:
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
            
            # 初始化界面状态
            if self.config.get("build_tool") == "nuitka":
                self._update_no_pyi_switch_state()
            elif self.config.get("build_tool") == "pyinstaller":
                self._update_pyinstaller_input_states()
                
        except Exception as e:
            # 错误处理：显示错误信息
            self._show_load_error(str(e))
    
    def _show_load_error(self, error_msg: str) -> None:
        """显示加载错误"""
        options_container = self.query_one("#options-fields", Container)
        
        # 移除加载器
        try:
            self.query_one("#loading-indicator").remove()
            self.query_one("#loading-text").remove()
        except Exception:
            pass
        
        # 显示错误信息
        from textual.widgets import Static
        options_container.mount(
            Static(
                f"加载配置失败\n\n{error_msg}\n\n请检查项目配置",
                id="error-message",
                classes="error-text"
            )
        )

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

    def _create_button_row(self, label1: str, id1: str, label2: str, id2: str):
        """创建按钮行"""
        return Horizontal(
            Vertical(
                Label(label1, classes="field-label"),
                Button(
                    id1.replace("-button", "..."), id=id1, variant="primary", flat=True
                ),
                classes="field-group",
            ),
            Vertical(
                Label(label2, classes="field-label"),
                Button(
                    id2.replace("-button", "..."), id=id2, variant="primary", flat=True
                ),
                classes="field-group",
            ),
            classes="inputs-row",
        )

    def _create_switch_row(self, *switches):
        """创建开关行"""
        return Horizontal(*switches, classes="switches-row")

    def _update_no_pyi_switch_state(self):
        """更新不生成 .pyi 文件开关的状态（仅 module/package 模式可用）"""
        try:
            no_pyi_switch = self.query_one("#no-pyi-switch", Switch)

            # 检查配置文件中是否明确设置了 mode
            mode = self.config.get("mode", "").strip().lower()

            # 只有在 module 或 package 模式下才启用该开关
            if mode in ("module", "package"):
                no_pyi_switch.disabled = False
            else:
                # 其他所有模式（standalone, onefile, app, accelerated 等）都禁用
                no_pyi_switch.disabled = True
                # 禁用时同时关闭开关（设为 False）
                no_pyi_switch.value = False
        except Exception:
            pass

    def _update_pyinstaller_input_states(self):
        """更新 PyInstaller 输入框状态（根据单文件模式）"""
        try:
            # 获取单文件模式开关的状态
            onefile_switch = self.query_one("#onefile-switch", Switch)
            is_onefile = onefile_switch.value

            # 内部目录名称（非单文件模式时启用）
            contents_dir_input = self.query_one("#contents-dir-input", Input)
            contents_dir_input.disabled = is_onefile

            # 启动画面图片（仅单文件模式）
            splash_image_input = self.query_one("#splash-image-input", Input)
            splash_image_input.disabled = not is_onefile

            # 运行时临时目录（仅单文件模式）
            runtime_tmpdir_input = self.query_one("#runtime-tmpdir-input", Input)
            runtime_tmpdir_input.disabled = not is_onefile

        except Exception:
            pass

    def _create_options_fields(self) -> None:
        """根据构建工具创建选项字段"""
        build_tool = self.config.get("build_tool", "nuitka")
        options_container = self.query_one("#options-fields", Container)
        
        # 移除加载指示器和提示文本
        try:
            self.query_one("#loading-indicator").remove()
            self.query_one("#loading-text").remove()
        except Exception:
            pass

        # Nuitka特有选项 - 使用标签页分组
        if build_tool == "nuitka":
            # 基本选项 - 按钮行
            buttons_row = self._create_button_row(
                "C 编译器:", "compiler-button", "启用插件:", "plugins-button"
            )

            # 基本选项 - 开关行1
            switches_row1 = self._create_switch_row(
                self._create_switch_widget(
                    "standalone-switch", "独立打包 (Standalone)", True, "standalone"
                ),
                self._create_switch_widget(
                    "onefile-switch", "单文件模式 (One File)", True, "onefile"
                ),
            )

            # 基本选项 - 开关行2
            switch3 = self._create_switch_widget(
                "console-switch", "显示终端窗口 (Windows)", False, "show_console"
            )
            python_flag_value = bool(self.config.get("python_flag", ""))
            switch4 = Vertical(
                Horizontal(
                    Switch(
                        value=python_flag_value,
                        id="python-flag-switch",
                        classes="field-switch",
                    ),
                    Label("Python优化 (移除断言和文档)", classes="field-switch-label"),
                    classes="field-switch-container",
                ),
                classes="field-group",
            )

            # 基本选项 - 开关行3：跟随导入 + 不生成 .pyi 文件
            follow_imports_switch = self._create_switch_widget(
                "follow-imports-switch",
                "跟随导入 (自动包含模块)",
                True,
                "follow_imports",
            )
            no_pyi_switch = self._create_switch_widget(
                "no-pyi-switch", "不生成 .pyi 文件 (仅module模式)", False, "no_pyi_file"
            )

            switches_row2 = self._create_switch_row(switch3, switch4)
            switches_row3_basic = self._create_switch_row(
                follow_imports_switch, no_pyi_switch
            )

            # 基本选项标签页内容（垂直布局：1行按钮 + 3行开关）
            basic_content = Vertical(
                buttons_row,
                switches_row1,
                switches_row2,
                switches_row3_basic,
                classes="basic-options-content",
            )

            # 高级选项 - 第1行：LTO 下拉选择 + 静默输出开关
            lto_value = self.config.get("lto", "no")
            # 兼容旧的布尔值
            if isinstance(lto_value, bool):
                lto_value = "yes" if lto_value else "no"

            # LTO 下拉选择
            lto_select = Select(
                [
                    ("关闭 LTO（链接时优化）", "no"),
                    ("启用 LTO（链接时优化）", "yes"),
                    ("自动 LTO（链接时优化）", "auto"),
                ],
                value=lto_value,
                id="lto-select",
                classes="field-select field-group",
                allow_blank=False,
            )

            # 静默输出开关
            quiet_switch = self._create_switch_widget(
                "quiet-switch", "静默输出 (仅进度条)", False, "quiet_mode"
            )

            switches_row3 = self._create_switch_row(lto_select, quiet_switch)

            # 高级选项 - 第2行
            switches_row4 = self._create_switch_row(
                self._create_switch_widget(
                    "remove-output-switch",
                    "移除构建文件 (节省空间)",
                    True,
                    "remove_output",
                ),
                Horizontal(
                    Label("编译线程:", classes="field-label-inline"),
                    Input(
                        placeholder="0",
                        value=str(self.config.get("jobs", 0)),
                        id="jobs-input",
                        classes="field-input",
                    ),
                    Button("-", id="jobs-decrease-btn", variant="default", flat=True),
                    Button("+", id="jobs-increase-btn", variant="default", flat=True),
                    classes="field-switch-container field-group",
                ),
            )

            # 高级选项 - 第3行：自动下载依赖工具
            switches_row5 = self._create_switch_row(
                self._create_switch_widget(
                    "assume-yes-switch",
                    "自动下载依赖 (CI环境必需)",
                    False,
                    "assume_yes_for_downloads",
                ),
                Vertical(classes="field-group"),  # 占位元素
            )

            # 高级选项标签页内容（垂直布局：3行）
            advanced_content = Vertical(
                switches_row3,
                switches_row4,
                switches_row5,
                classes="basic-options-content",
            )

            # 数据导入标签页 - 第1行输入框（2个）
            nuitka_import_input1 = self._create_input_widget(
                "nuitka-include-package-input",
                "包含包 (支持空格、中英文逗号分隔):",
                "include_packages",
                "例如: numpy pandas PIL",
            )
            nuitka_import_input2 = self._create_input_widget(
                "nuitka-include-module-input",
                "包含模块 (支持空格、中英文逗号分隔):",
                "include_modules",
                "例如: requests.adapters os.path",
            )
            nuitka_import_row1 = Horizontal(
                nuitka_import_input1, nuitka_import_input2, classes="inputs-row"
            )

            # 数据导入标签页 - 第2行输入框（2个）
            nuitka_import_input3 = self._create_input_widget(
                "nuitka-nofollow-import-input",
                "排除导入 (支持空格、中英文逗号分隔):",
                "nofollow_imports",
                "例如: tkinter test unittest",
            )
            nuitka_import_input4 = self._create_input_widget(
                "nuitka-include-data-files-input",
                "数据文件 (支持空格、中英文逗号分隔):",
                "include_data_files",
                "格式: src;dest 多个用空格",
            )
            nuitka_import_row2 = Horizontal(
                nuitka_import_input3, nuitka_import_input4, classes="inputs-row"
            )

            # 数据导入标签页 - 第3行输入框（2个）
            nuitka_import_input5 = self._create_input_widget(
                "nuitka-include-data-dir-input",
                "数据目录 (支持空格、中英文逗号分隔):",
                "include_data_dirs",
                "格式: src;dest 多个用空格",
            )
            nuitka_import_input6 = Vertical(
                Label("", classes="field-label"),  # 占位
                classes="field-group",
            )
            nuitka_import_row3 = Horizontal(
                nuitka_import_input5, nuitka_import_input6, classes="inputs-row"
            )

            # 数据导入标签页内容（垂直布局：3行输入框）
            nuitka_import_content = Vertical(
                nuitka_import_row1,
                nuitka_import_row2,
                nuitka_import_row3,
                classes="basic-options-content",
            )

            # 创建标签页容器并使用 compose 方法添加标签页
            tabs = TabbedContent(id="nuitka-tabs")
            tabs.compose_add_child(TabPane("基本选项", basic_content, id="basic-tab"))
            tabs.compose_add_child(
                TabPane("高级选项", advanced_content, id="advanced-tab")
            )
            tabs.compose_add_child(
                TabPane("数据导入", nuitka_import_content, id="nuitka-import-tab")
            )

            # 挂载标签页容器
            options_container.mount(tabs)

            return  # Nuitka 使用标签页，不需要下面的两列布局

        # PyInstaller特有选项 - 使用标签页分组
        if build_tool == "pyinstaller":
            # 基本选项 - 2个开关横向排列
            switch1 = self._create_switch_widget(
                "onefile-switch", "单文件模式", True, "onefile"
            )
            switch2 = self._create_switch_widget(
                "uac-admin-switch", "管理员权限 (Windows UAC)", False, "uac_admin"
            )
            switches_row = Horizontal(switch1, switch2, classes="switches-row")

            # 基本选项 - 第1行输入框（2个）
            input1 = self._create_input_widget(
                "contents-dir-input",
                "内部目录名称:",
                "contents_directory",
                "_internal (默认为 .)",
            )
            input2 = self._create_input_widget(
                "splash-image-input",
                "启动画面图片 (仅单文件模式):",
                "splash_image",
                "例如: splash.png",
            )
            inputs_row1 = Horizontal(input1, input2, classes="inputs-row")

            # 基本选项 - 第2行输入框（1个）
            input3 = self._create_input_widget(
                "runtime-tmpdir-input",
                "运行时临时目录 (仅单文件模式):",
                "runtime_tmpdir",
                "例如: /tmp/myapp",
            )
            input4 = Vertical(
                Label("", classes="field-label"),  # 占位
                classes="field-group",
            )
            inputs_row2 = Horizontal(input3, input4, classes="inputs-row")

            # 基本选项标签页内容（垂直布局：1行开关 + 2行输入框）
            basic_content = Vertical(
                switches_row, inputs_row1, inputs_row2, classes="basic-options-content"
            )

            # 高级选项 - 第1行开关（2个）
            switch3 = self._create_switch_widget(
                "clean-switch", "清理临时文件", True, "clean"
            )
            switch4 = self._create_switch_widget(
                "noconfirm-switch", "自动确认 (跳过删除提示)", False, "noconfirm"
            )
            switches_row1 = Horizontal(switch3, switch4, classes="switches-row")

            # 高级选项 - 第2行开关（2个）
            switch5 = self._create_switch_widget(
                "quiet-switch", "静默输出 (仅进度条)", False, "quiet_mode"
            )
            switch6 = self._create_switch_widget(
                "debug-switch", "调试模式 (输出详细信息)", False, "debug"
            )
            switches_row2 = Horizontal(switch5, switch6, classes="switches-row")

            # 高级选项标签页内容（垂直布局：2行开关）
            advanced_content = Vertical(
                switches_row1,
                switches_row2,
                classes="basic-options-content",
            )

            # 数据导入标签页 - 第1行输入框（2个）
            import_input1 = self._create_input_widget(
                "hidden-imports-input",
                "隐藏导入 (支持空格、中英文逗号分隔):",
                "hidden_imports",
                "例如: PIL numpy.core pandas",
            )
            import_input2 = self._create_input_widget(
                "exclude-modules-input",
                "排除模块 (支持空格、中英文逗号分隔):",
                "exclude_modules",
                "例如: tkinter test unittest",
            )
            import_row1 = Horizontal(import_input1, import_input2, classes="inputs-row")

            # 数据导入标签页 - 第2行输入框（2个）
            import_input3 = self._create_input_widget(
                "collect-submodules-input",
                "收集子模块 (支持空格、中英文逗号分隔):",
                "collect_submodules",
                "例如: textual pyfiglet",
            )
            import_input4 = self._create_input_widget(
                "collect-data-input",
                "收集数据文件 (支持空格、中英文逗号分隔):",
                "collect_data",
                "例如: textual pyfiglet",
            )
            import_row2 = Horizontal(import_input3, import_input4, classes="inputs-row")

            # 数据导入标签页 - 第3行输入框（2个）
            import_input5 = self._create_input_widget(
                "collect-binaries-input",
                "收集二进制文件 (支持空格、中英文逗号分隔):",
                "collect_binaries",
                "例如: numpy PIL",
            )
            import_input6 = self._create_input_widget(
                "collect-all-input",
                "收集所有 (支持空格、中英文逗号分隔):",
                "collect_all",
                "例如: cv2 scipy",
            )
            import_row3 = Horizontal(import_input5, import_input6, classes="inputs-row")

            # 数据导入标签页 - 第4行输入框（2个）
            import_input7 = self._create_input_widget(
                "add-data-input",
                "数据文件 (支持空格、中英文逗号分隔):",
                "add_data",
                "格式: src;dest 多个用空格",
            )
            import_input8 = self._create_input_widget(
                "add-binary-input",
                "二进制文件 (支持空格、中英文逗号分隔):",
                "add_binary",
                "格式: src;dest 多个用空格",
            )
            import_row4 = Horizontal(import_input7, import_input8, classes="inputs-row")

            # 数据导入标签页内容（垂直布局：4行输入框）
            import_content = Vertical(
                import_row1,
                import_row2,
                import_row3,
                import_row4,
                classes="basic-options-content",
            )

            # 系统特性标签页 - Windows 特性（第1行输入框）
            platform_input1 = self._create_input_widget(
                "win-version-file-input",
                "Windows 版本信息文件:",
                "win_version_file",
                "例如: version_info.txt",
            )
            platform_input2 = self._create_input_widget(
                "win-manifest-input",
                "Windows Manifest 文件:",
                "win_manifest",
                "例如: app.manifest",
            )
            platform_row1 = Horizontal(
                platform_input1, platform_input2, classes="inputs-row"
            )

            # 系统特性标签页 - macOS 特性（第2行输入框）
            platform_input3 = self._create_input_widget(
                "target-arch-input",
                "目标架构 (macOS):",
                "target_architecture",
                "例如: x86_64, arm64, universal2",
            )
            platform_input4 = self._create_input_widget(
                "osx-bundle-id-input",
                "macOS Bundle 标识符:",
                "osx_bundle_identifier",
                "例如: com.company.appname",
            )
            platform_row2 = Horizontal(
                platform_input3, platform_input4, classes="inputs-row"
            )

            # 系统特性标签页 - macOS 特性（第3行输入框）
            platform_input5 = self._create_input_widget(
                "osx-entitlements-input",
                "macOS 权限文件:",
                "osx_entitlements_file",
                "例如: entitlements.plist",
            )
            platform_input6 = self._create_input_widget(
                "codesign-identity-input",
                "代码签名身份 (macOS):",
                "codesign_identity",
                "例如: Developer ID Application",
            )
            platform_row3 = Horizontal(
                platform_input5, platform_input6, classes="inputs-row"
            )

            # 系统特性标签页内容（垂直布局：3行输入框）
            platform_content = Vertical(
                platform_row1,
                platform_row2,
                platform_row3,
                classes="basic-options-content",
            )

            # 创建标签页容器并使用 compose 方法添加标签页
            tabs = TabbedContent(id="pyinstaller-tabs")
            tabs.compose_add_child(TabPane("基本选项", basic_content, id="basic-tab"))
            tabs.compose_add_child(
                TabPane("高级选项", advanced_content, id="advanced-tab")
            )
            tabs.compose_add_child(TabPane("数据导入", import_content, id="import-tab"))
            tabs.compose_add_child(
                TabPane("系统特性", platform_content, id="platform-tab")
            )

            # 挂载标签页容器
            options_container.mount(tabs)

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
            # LTO 从下拉选择获取
            lto_select = self.query_one("#lto-select", Select)
            existing_config["lto"] = lto_select.value if lto_select.value else "no"
            existing_config["no_pyi_file"] = self.query_one(
                "#no-pyi-switch", Switch
            ).value
            existing_config["follow_imports"] = self.query_one(
                "#follow-imports-switch", Switch
            ).value
            # 并行编译任务数（0或负数表示自动分配）
            jobs_value = self.query_one("#jobs-input", Input).value
            try:
                existing_config["jobs"] = int(jobs_value) if jobs_value else 0
            except ValueError:
                existing_config["jobs"] = 0
            # Python优化标志（开关转换为字符串）
            python_opt = self.query_one("#python-flag-switch", Switch).value
            existing_config["python_flag"] = "-O" if python_opt else ""
            # 插件支持 - 使用存储的插件列表
            existing_config["plugins"] = (
                ",".join(self.selected_plugins) if self.selected_plugins else ""
            )
            # C编译器
            existing_config["compiler"] = self.selected_compiler
            # 自动下载依赖工具
            existing_config["assume_yes_for_downloads"] = self.query_one(
                "#assume-yes-switch", Switch
            ).value

            # 数据导入选项
            existing_config["include_packages"] = self.query_one(
                "#nuitka-include-package-input", Input
            ).value.strip()
            existing_config["include_modules"] = self.query_one(
                "#nuitka-include-module-input", Input
            ).value.strip()
            existing_config["nofollow_imports"] = self.query_one(
                "#nuitka-nofollow-import-input", Input
            ).value.strip()
            existing_config["include_data_files"] = self.query_one(
                "#nuitka-include-data-files-input", Input
            ).value.strip()
            existing_config["include_data_dirs"] = self.query_one(
                "#nuitka-include-data-dir-input", Input
            ).value.strip()

        # PyInstaller特有选项
        if build_tool == "pyinstaller":
            # 静默模式配置
            quiet_mode = self.query_one("#quiet-switch", Switch).value
            existing_config["quiet_mode"] = quiet_mode
            existing_config["show_progressbar"] = not quiet_mode

            # PyInstaller 特有选项
            existing_config["onefile"] = self.query_one("#onefile-switch", Switch).value
            existing_config["clean"] = self.query_one("#clean-switch", Switch).value
            existing_config["noconfirm"] = self.query_one(
                "#noconfirm-switch", Switch
            ).value
            existing_config["debug"] = self.query_one("#debug-switch", Switch).value

            # 内部目录名称（单文件模式下忽略）
            if not existing_config["onefile"]:
                contents_dir = self.query_one(
                    "#contents-dir-input", Input
                ).value.strip()
                existing_config["contents_directory"] = (
                    contents_dir if contents_dir else "."
                )
            else:
                existing_config["contents_directory"] = "."

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

            # 收集子模块
            existing_config["collect_submodules"] = self.query_one(
                "#collect-submodules-input", Input
            ).value.strip()

            # 收集数据文件
            existing_config["collect_data"] = self.query_one(
                "#collect-data-input", Input
            ).value.strip()

            # 收集二进制文件
            existing_config["collect_binaries"] = self.query_one(
                "#collect-binaries-input", Input
            ).value.strip()

            # 收集所有
            existing_config["collect_all"] = self.query_one(
                "#collect-all-input", Input
            ).value.strip()

            # 添加数据文件
            existing_config["add_data"] = self.query_one(
                "#add-data-input", Input
            ).value.strip()

            # 添加二进制文件
            existing_config["add_binary"] = self.query_one(
                "#add-binary-input", Input
            ).value.strip()

            # 运行时临时目录
            existing_config["runtime_tmpdir"] = self.query_one(
                "#runtime-tmpdir-input", Input
            ).value.strip()

            # 目标架构
            existing_config["target_architecture"] = self.query_one(
                "#target-arch-input", Input
            ).value.strip()

            # 系统特性 - Windows
            existing_config["win_version_file"] = self.query_one(
                "#win-version-file-input", Input
            ).value.strip()
            existing_config["win_manifest"] = self.query_one(
                "#win-manifest-input", Input
            ).value.strip()

            # 系统特性 - macOS
            existing_config["osx_bundle_identifier"] = self.query_one(
                "#osx-bundle-id-input", Input
            ).value.strip()
            existing_config["osx_entitlements_file"] = self.query_one(
                "#osx-entitlements-input", Input
            ).value.strip()
            existing_config["codesign_identity"] = self.query_one(
                "#codesign-identity-input", Input
            ).value.strip()

            # 启动画面图片（仅单文件模式时读取UI值）
            if existing_config["onefile"]:
                splash_image = self.query_one(
                    "#splash-image-input", Input
                ).value.strip()
                existing_config["splash_image"] = splash_image
            else:
                # 非单文件模式时，保留配置文件中的值（不从被禁用的UI读取）
                existing_config["splash_image"] = self.config.get("splash_image", "")

        # 保持列表字段
        if "exclude_packages" not in existing_config:
            existing_config["exclude_packages"] = []

        # 更新self.config为完整配置
        self.config = existing_config

    def on_switch_changed(self, event: Switch.Changed) -> None:
        """处理开关变化事件"""
        # Nuitka: 处理 standalone 和 onefile 开关变化
        if event.switch.id in ("standalone-switch", "onefile-switch"):
            if self.config.get("build_tool") == "nuitka":
                # 更新 config 中的值
                if event.switch.id == "standalone-switch":
                    self.config["standalone"] = event.value
                elif event.switch.id == "onefile-switch":
                    self.config["onefile"] = event.value
                # 更新 no-pyi-switch 状态
                self._update_no_pyi_switch_state()

        # PyInstaller: 处理 onefile 开关变化
        if event.switch.id == "onefile-switch":
            try:
                # 更新内部目录名称状态
                contents_dir_input = self.query_one("#contents-dir-input", Input)
                contents_dir_input.disabled = event.value
                if event.value:
                    contents_dir_input.value = ""

                # 更新启动画面图片状态（onefile时启用，非onefile时禁用）
                splash_image_input = self.query_one("#splash-image-input", Input)
                splash_image_input.disabled = not event.value
                # 注意：不清空值，保留用户输入，只是禁用输入框

                # 更新运行时临时目录状态（onefile时启用，非onefile时禁用）
                runtime_tmpdir_input = self.query_one("#runtime-tmpdir-input", Input)
                runtime_tmpdir_input.disabled = not event.value
                # 注意：不清空值，保留用户输入，只是禁用输入框
            except Exception:
                pass

    def on_input_changed(self, event: Input.Changed) -> None:
        """处理输入框变化事件"""
        # 检查 collect_all 与其他收集选项的冲突（仅 PyInstaller）
        if self.config.get("build_tool") == "pyinstaller":
            if event.input.id in [
                "collect-all-input",
                "collect-submodules-input",
                "collect-data-input",
                "collect-binaries-input",
            ]:
                self._check_collect_conflicts()

    def _check_collect_conflicts(self) -> None:
        """检查收集选项的冲突"""
        try:
            import re

            # 解析输入值的辅助函数
            def parse_input(input_id: str) -> set:
                return set(
                    filter(
                        None,
                        re.split(
                            r"[,\s，]+",
                            self.query_one(f"#{input_id}", Input).value.strip(),
                        ),
                    )
                )

            # 获取所有收集选项
            collect_all = parse_input("collect-all-input")
            if not collect_all:
                return

            # 检查与其他选项的重叠
            checks = [
                ("collect-submodules-input", "收集子模块"),
                ("collect-data-input", "收集数据文件"),
                ("collect-binaries-input", "收集二进制文件"),
            ]

            conflicts = [
                f"{label}: {', '.join(sorted(overlap))}"
                for input_id, label in checks
                if (overlap := collect_all & parse_input(input_id))
            ]

            if conflicts:
                self.notify(
                    "以下包在'收集所有'中已包含，无需重复配置:\n"
                    + "\n".join(conflicts),
                    severity="warning",
                    timeout=5,
                )
        except Exception as e:
            self.notify(f"检查冲突时出错: {str(e)}", severity="error")

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
        """调整编译线程数（0或负数表示自动分配）"""
        jobs_input = self.query_one("#jobs-input", Input)
        try:
            current_value = int(jobs_input.value) if jobs_input.value else 0
        except ValueError:
            current_value = 0

        # 计算新值，允许负数和0（表示自动分配）
        new_value = current_value + delta
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
        # 保存前检查冲突
        if self.config.get("build_tool") == "pyinstaller":
            self._check_collect_conflicts()

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
