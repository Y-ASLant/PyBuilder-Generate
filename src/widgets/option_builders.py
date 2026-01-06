"""
打包选项 UI 组件构建器
提取自 package_options_screen.py 的可复用组件工厂函数
"""

from typing import Dict, Any
from textual.containers import Vertical, Horizontal
from textual.widgets import (
    Button,
    Switch,
    Label,
    Input,
    TabbedContent,
    TabPane,
    Select,
)


def create_switch_widget(
    switch_id: str,
    label: str,
    default_value: bool,
    config: Dict[str, Any],
    config_key: str,
) -> Vertical:
    """创建开关组件"""
    return Vertical(
        Horizontal(
            Switch(
                value=config.get(config_key, default_value),
                id=switch_id,
                classes="field-switch",
            ),
            Label(label, classes="field-switch-label"),
            classes="field-switch-container",
        ),
        classes="field-group",
    )


def create_input_widget(
    input_id: str,
    label: str,
    config: Dict[str, Any],
    config_key: str,
    placeholder: str,
) -> Vertical:
    """创建输入框组件"""
    return Vertical(
        Label(label, classes="field-label"),
        Input(
            value=config.get(config_key, ""),
            placeholder=placeholder,
            id=input_id,
            classes="field-input",
        ),
        classes="field-group",
    )


def create_button_row(label1: str, id1: str, label2: str, id2: str) -> Horizontal:
    """创建按钮行"""
    return Horizontal(
        Vertical(
            Label(label1, classes="field-label"),
            Button(id1.replace("-button", "..."), id=id1, variant="primary", flat=True),
            classes="field-group",
        ),
        Vertical(
            Label(label2, classes="field-label"),
            Button(id2.replace("-button", "..."), id=id2, variant="primary", flat=True),
            classes="field-group",
        ),
        classes="inputs-row",
    )


def create_switch_row(*switches) -> Horizontal:
    """创建开关行"""
    return Horizontal(*switches, classes="switches-row")


def create_inputs_row(*inputs) -> Horizontal:
    """创建输入框行"""
    return Horizontal(*inputs, classes="inputs-row")


def build_nuitka_options(config: Dict[str, Any]) -> TabbedContent:
    """
    构建 Nuitka 打包选项的标签页组件

    Args:
        config: 构建配置字典

    Returns:
        TabbedContent: 包含基本选项、高级选项、数据导入三个标签页
    """
    # 基本选项 - 按钮行
    buttons_row = create_button_row(
        "C 编译器:", "compiler-button", "启用插件:", "plugins-button"
    )

    # 基本选项 - 开关行1
    switches_row1 = create_switch_row(
        create_switch_widget(
            "standalone-switch", "独立打包 (Standalone)", True, config, "standalone"
        ),
        create_switch_widget(
            "onefile-switch", "单文件模式 (One File)", True, config, "onefile"
        ),
    )

    # 基本选项 - 开关行2
    switch3 = create_switch_widget(
        "console-switch", "显示终端窗口 (Windows)", False, config, "show_console"
    )
    python_flag_value = bool(config.get("python_flag", ""))
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
    follow_imports_switch = create_switch_widget(
        "follow-imports-switch",
        "跟随导入 (自动包含模块)",
        True,
        config,
        "follow_imports",
    )
    no_pyi_switch = create_switch_widget(
        "no-pyi-switch", "不生成 .pyi 文件 (仅module模式)", False, config, "no_pyi_file"
    )

    switches_row2 = create_switch_row(switch3, switch4)
    switches_row3_basic = create_switch_row(follow_imports_switch, no_pyi_switch)

    # 基本选项标签页内容
    basic_content = Vertical(
        buttons_row,
        switches_row1,
        switches_row2,
        switches_row3_basic,
        classes="basic-options-content",
    )

    # 高级选项 - 第1行：LTO 下拉选择 + 静默输出开关
    lto_value = config.get("lto", "no")
    if isinstance(lto_value, bool):
        lto_value = "yes" if lto_value else "no"

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

    quiet_switch = create_switch_widget(
        "quiet-switch", "静默输出 (仅进度条)", False, config, "quiet_mode"
    )

    switches_row3 = create_switch_row(lto_select, quiet_switch)

    # 高级选项 - 第2行
    switches_row4 = create_switch_row(
        create_switch_widget(
            "remove-output-switch",
            "移除构建文件 (节省空间)",
            True,
            config,
            "remove_output",
        ),
        Horizontal(
            Label("编译线程:", classes="field-label-inline"),
            Input(
                placeholder="0",
                value=str(config.get("jobs", 0)),
                id="jobs-input",
                classes="field-input",
            ),
            Button("-", id="jobs-decrease-btn", variant="default", flat=True),
            Button("+", id="jobs-increase-btn", variant="default", flat=True),
            classes="field-switch-container field-group",
        ),
    )

    # 高级选项 - 第3行：自动下载依赖工具
    switches_row5 = create_switch_row(
        create_switch_widget(
            "assume-yes-switch",
            "自动下载依赖 (CI环境必需)",
            False,
            config,
            "assume_yes_for_downloads",
        ),
        Vertical(classes="field-group"),  # 占位元素
    )

    # 高级选项标签页内容
    advanced_content = Vertical(
        switches_row3,
        switches_row4,
        switches_row5,
        classes="basic-options-content",
    )

    # 数据导入标签页
    nuitka_import_row1 = create_inputs_row(
        create_input_widget(
            "nuitka-include-package-input",
            "包含包 (支持空格、中英文逗号分隔):",
            config,
            "include_packages",
            "例如: numpy pandas PIL",
        ),
        create_input_widget(
            "nuitka-include-module-input",
            "包含模块 (支持空格、中英文逗号分隔):",
            config,
            "include_modules",
            "例如: requests.adapters os.path",
        ),
    )

    nuitka_import_row2 = create_inputs_row(
        create_input_widget(
            "nuitka-nofollow-import-input",
            "排除导入 (支持空格、中英文逗号分隔):",
            config,
            "nofollow_imports",
            "例如: tkinter test unittest",
        ),
        create_input_widget(
            "nuitka-include-data-files-input",
            "数据文件 (支持空格、中英文逗号分隔):",
            config,
            "include_data_files",
            "格式: src;dest 多个用空格",
        ),
    )

    nuitka_import_row3 = create_inputs_row(
        create_input_widget(
            "nuitka-include-data-dir-input",
            "数据目录 (支持空格、中英文逗号分隔):",
            config,
            "include_data_dirs",
            "格式: src;dest 多个用空格",
        ),
        Vertical(
            Label("", classes="field-label"),  # 占位
            classes="field-group",
        ),
    )

    nuitka_import_content = Vertical(
        nuitka_import_row1,
        nuitka_import_row2,
        nuitka_import_row3,
        classes="basic-options-content",
    )

    # 创建标签页容器
    tabs = TabbedContent(id="nuitka-tabs")
    tabs.compose_add_child(TabPane("基本选项", basic_content, id="basic-tab"))
    tabs.compose_add_child(TabPane("高级选项", advanced_content, id="advanced-tab"))
    tabs.compose_add_child(
        TabPane("数据导入", nuitka_import_content, id="nuitka-import-tab")
    )

    return tabs


def build_pyinstaller_options(config: Dict[str, Any]) -> TabbedContent:
    """
    构建 PyInstaller 打包选项的标签页组件

    Args:
        config: 构建配置字典

    Returns:
        TabbedContent: 包含基本选项、高级选项、数据导入、系统特性四个标签页
    """
    # 基本选项 - 2个开关横向排列
    switches_row = create_switch_row(
        create_switch_widget("onefile-switch", "单文件模式", True, config, "onefile"),
        create_switch_widget(
            "uac-admin-switch", "管理员权限 (Windows UAC)", False, config, "uac_admin"
        ),
    )

    # 基本选项 - 第1行输入框
    inputs_row1 = create_inputs_row(
        create_input_widget(
            "contents-dir-input",
            "内部目录名称:",
            config,
            "contents_directory",
            "_internal (默认为 .)",
        ),
        create_input_widget(
            "splash-image-input",
            "启动画面图片 (仅单文件模式):",
            config,
            "splash_image",
            "例如: splash.png",
        ),
    )

    # 基本选项 - 第2行输入框
    inputs_row2 = create_inputs_row(
        create_input_widget(
            "runtime-tmpdir-input",
            "运行时临时目录 (仅单文件模式):",
            config,
            "runtime_tmpdir",
            "例如: /tmp/myapp",
        ),
        Vertical(
            Label("", classes="field-label"),  # 占位
            classes="field-group",
        ),
    )

    basic_content = Vertical(
        switches_row, inputs_row1, inputs_row2, classes="basic-options-content"
    )

    # 高级选项 - 第1行开关
    switches_row1 = create_switch_row(
        create_switch_widget("clean-switch", "清理临时文件", True, config, "clean"),
        create_switch_widget(
            "noconfirm-switch", "自动确认 (跳过删除提示)", False, config, "noconfirm"
        ),
    )

    # 高级选项 - 第2行开关
    switches_row2 = create_switch_row(
        create_switch_widget(
            "quiet-switch", "静默输出 (仅进度条)", False, config, "quiet_mode"
        ),
        create_switch_widget(
            "debug-switch", "调试模式 (输出详细信息)", False, config, "debug"
        ),
    )

    advanced_content = Vertical(
        switches_row1,
        switches_row2,
        classes="basic-options-content",
    )

    # 数据导入标签页
    import_row1 = create_inputs_row(
        create_input_widget(
            "hidden-imports-input",
            "隐藏导入 (支持空格、中英文逗号分隔):",
            config,
            "hidden_imports",
            "例如: PIL numpy.core pandas",
        ),
        create_input_widget(
            "exclude-modules-input",
            "排除模块 (支持空格、中英文逗号分隔):",
            config,
            "exclude_modules",
            "例如: tkinter test unittest",
        ),
    )

    import_row2 = create_inputs_row(
        create_input_widget(
            "collect-submodules-input",
            "收集子模块 (支持空格、中英文逗号分隔):",
            config,
            "collect_submodules",
            "例如: textual pyfiglet",
        ),
        create_input_widget(
            "collect-data-input",
            "收集数据文件 (支持空格、中英文逗号分隔):",
            config,
            "collect_data",
            "例如: textual pyfiglet",
        ),
    )

    import_row3 = create_inputs_row(
        create_input_widget(
            "collect-binaries-input",
            "收集二进制文件 (支持空格、中英文逗号分隔):",
            config,
            "collect_binaries",
            "例如: numpy PIL",
        ),
        create_input_widget(
            "collect-all-input",
            "收集所有 (支持空格、中英文逗号分隔):",
            config,
            "collect_all",
            "例如: cv2 scipy",
        ),
    )

    import_row4 = create_inputs_row(
        create_input_widget(
            "add-data-input",
            "数据文件 (支持空格、中英文逗号分隔):",
            config,
            "add_data",
            "格式: src;dest 多个用空格",
        ),
        create_input_widget(
            "add-binary-input",
            "二进制文件 (支持空格、中英文逗号分隔):",
            config,
            "add_binary",
            "格式: src;dest 多个用空格",
        ),
    )

    import_content = Vertical(
        import_row1,
        import_row2,
        import_row3,
        import_row4,
        classes="basic-options-content",
    )

    # 系统特性标签页 - Windows 特性
    platform_row1 = create_inputs_row(
        create_input_widget(
            "win-version-file-input",
            "Windows 版本信息文件:",
            config,
            "win_version_file",
            "例如: version_info.txt",
        ),
        create_input_widget(
            "win-manifest-input",
            "Windows Manifest 文件:",
            config,
            "win_manifest",
            "例如: app.manifest",
        ),
    )

    # 系统特性标签页 - macOS 特性
    platform_row2 = create_inputs_row(
        create_input_widget(
            "target-arch-input",
            "目标架构 (macOS):",
            config,
            "target_architecture",
            "例如: x86_64, arm64, universal2",
        ),
        create_input_widget(
            "osx-bundle-id-input",
            "macOS Bundle 标识符:",
            config,
            "osx_bundle_identifier",
            "例如: com.company.appname",
        ),
    )

    platform_row3 = create_inputs_row(
        create_input_widget(
            "osx-entitlements-input",
            "macOS 权限文件:",
            config,
            "osx_entitlements_file",
            "例如: entitlements.plist",
        ),
        create_input_widget(
            "codesign-identity-input",
            "代码签名身份 (macOS):",
            config,
            "codesign_identity",
            "例如: Developer ID Application",
        ),
    )

    platform_content = Vertical(
        platform_row1,
        platform_row2,
        platform_row3,
        classes="basic-options-content",
    )

    # 创建标签页容器
    tabs = TabbedContent(id="pyinstaller-tabs")
    tabs.compose_add_child(TabPane("基本选项", basic_content, id="basic-tab"))
    tabs.compose_add_child(TabPane("高级选项", advanced_content, id="advanced-tab"))
    tabs.compose_add_child(TabPane("数据导入", import_content, id="import-tab"))
    tabs.compose_add_child(TabPane("系统特性", platform_content, id="platform-tab"))

    return tabs
