"""
脚本生成器模块
根据配置生成 Nuitka 或 PyInstaller 构建脚本
"""

import re
from pathlib import Path
from typing import Dict, Any, List


# 预编译正则表达式
_SPLIT_PATTERN = re.compile(r"[,\s，]+")


def _split_items(text: str) -> List[str]:
    """分割字符串，支持空格、英文逗号、中文逗号"""
    return [s.strip() for s in _SPLIT_PATTERN.split(text) if s.strip()]


# 颜色类定义（用于生成的脚本）
COLOR_CLASS_CODE = """# ANSI 颜色代码
class Color:
    RESET = '\\033[0m'
    BOLD = '\\033[1m'
    GREEN = '\\033[92m'
    YELLOW = '\\033[93m'
    RED = '\\033[91m'
    CYAN = '\\033[96m'
    GRAY = '\\033[90m'
"""


def _generate_script_header(config: Dict[str, Any], tool_name: str) -> List[str]:
    """生成脚本头部（公共部分）"""
    project_name = config.get("project_name", "MyApp")
    version = config.get("version", "1.0.0")

    lines = [
        "# -*- coding: utf-8 -*-",
        '"""',
        f"{project_name} - {tool_name} 构建脚本",
        f"版本: {version}",
        '"""',
        "",
        "import sys",
        "import os",
        "import subprocess",
        "import shutil",
        "import time",
        "import platform",
        "",
        "",
        COLOR_CLASS_CODE,
        "",
    ]
    return lines


def _generate_config_section(
    config: Dict[str, Any], extra_vars: List[str] | None = None
) -> List[str]:
    """生成配置常量部分"""
    lines = [
        "# 构建配置",
        f"PROJECT_NAME = '{config.get('project_name', 'MyApp')}'",
        f"VERSION = '{config.get('version', '1.0.0')}'",
        f"ENTRY_FILE = '{config.get('entry_file', 'main.py')}'",
    ]
    if config.get("company_name"):
        lines.append(f"COMPANY_NAME = '{config['company_name']}'")
    if config.get("icon_file"):
        lines.append(f"ICON_FILE = '{config['icon_file']}'")
    if extra_vars:
        lines.extend(extra_vars)
    lines.append(f"OUTPUT_DIR = '{config.get('output_dir', 'dist')}'")
    lines.append("")
    return lines


def _generate_build_function_header(tool_name: str) -> List[str]:
    """生成构建函数开头部分"""
    return [
        "def build():",
        f'    """执行 {tool_name} 构建"""',
        "    # 获取平台信息",
        "    os_type = platform.system()",
        "    is_windows = os_type == 'Windows'",
        "    is_macos = os_type == 'Darwin'",
        "    is_linux = os_type == 'Linux'",
        "    ",
        "    # 获取终端宽度",
        "    width = shutil.get_terminal_size().columns",
        "    separator = '-' * width",
        "    start_time = time.time()",
        "",
        "    print(f'{Color.CYAN}{Color.BOLD}Building {PROJECT_NAME} v{VERSION} on {os_type}{Color.RESET}')",
        "    print(separator)",
        "",
    ]


def _generate_build_execution() -> List[str]:
    """生成构建执行部分（命令打印）"""
    return [
        "    # 执行构建",
        "    print(f'{Color.GRAY}Command:{Color.RESET}')",
        "    print(f'{Color.GRAY}' + ' '.join(cmd) + f'{Color.RESET}')",
        "    print(separator)",
        "    print(f'{Color.YELLOW}Building, please wait...{Color.RESET}')",
        "    print()",
        "",
    ]


def _generate_build_result(cleanup_code: List[str] | None = None) -> List[str]:
    """生成构建结果处理部分"""
    lines = [
        "    try:",
        "        subprocess.run(cmd, check=True)",
        "        print(separator)",
        "        elapsed_time = time.time() - start_time",
        "        minutes = int(elapsed_time // 60)",
        "        seconds = int(elapsed_time % 60)",
        "        print(f'{Color.GREEN}{Color.BOLD}Build successful!{Color.RESET}')",
    ]
    if cleanup_code:
        lines.extend(cleanup_code)
    lines.extend(
        [
            "        abs_output = os.path.abspath(OUTPUT_DIR)",
            "        print(f'{Color.GREEN}Output: {abs_output}{Color.RESET}')",
            "        if minutes > 0:",
            "            print(f'{Color.CYAN}Build time: {minutes}m {seconds}s{Color.RESET}')",
            "        else:",
            "            print(f'{Color.CYAN}Build time: {seconds}s{Color.RESET}')",
            "        return 0",
            "    except subprocess.CalledProcessError as e:",
            "        print(separator)",
            "        print(f'{Color.RED}{Color.BOLD}Build failed: {Color.RESET}{Color.RED}{e}{Color.RESET}')",
            "        return 1",
            "    except Exception as e:",
            "        print(separator)",
            "        print(f'{Color.RED}{Color.BOLD}Error: {Color.RESET}{Color.RED}{e}{Color.RESET}')",
            "        return 1",
            "",
        ]
    )
    return lines


def _generate_main_block() -> List[str]:
    """生成主函数入口"""
    return [
        "",
        "if __name__ == '__main__':",
        "    sys.exit(build())",
        "",
    ]


def _generate_path_code(path_str: str) -> str:
    """生成 os.path.join 代码字符串"""
    parts = [p for p in path_str.replace("\\", "/").split("/") if p]
    return (
        f"os.path.join({', '.join(repr(p) for p in parts)})"
        if len(parts) > 1
        else repr(parts[0] if parts else path_str)
    )


def generate_nuitka_script(config: Dict[str, Any], project_dir: Path) -> str:
    """生成 Nuitka 构建脚本"""
    lines = []

    # 使用公共模板生成头部
    lines.extend(_generate_script_header(config, "Nuitka"))
    lines.extend(_generate_config_section(config))
    lines.extend(_generate_build_function_header("Nuitka"))

    # 构建命令
    lines.append("    # 构建 Nuitka 命令")
    lines.append("    cmd = [")
    lines.append("        sys.executable,")
    lines.append("        '-m', 'nuitka',")

    # 编译模式（使用 Nuitka 官方推荐的 --mode 参数）
    mode = config.get("mode", "").strip().lower()

    if not mode:
        # 向后兼容：从旧配置自动推导 mode
        standalone = config.get("standalone", True)
        onefile = config.get("onefile", True)

        if standalone and onefile:
            mode = "onefile"
        elif standalone:
            mode = "standalone"
        else:
            mode = "accelerated"

    # 添加 mode 参数
    lines.append(f"        '--mode={mode}',")

    # 输出选项
    lines.append("        f'--output-dir={OUTPUT_DIR}',")
    lines.append("        f'--output-filename={PROJECT_NAME}',")

    # 输出文件夹名称（仅非 onefile 模式）
    if mode == "standalone" or mode == "app-dist":
        lines.append("        f'--output-folder-name={PROJECT_NAME}.dist',")

    # LTO 链接时优化
    lto = config.get("lto", "no")
    # 兼容旧的布尔值
    if isinstance(lto, bool):
        lto = "yes" if lto else "no"
    # 只有设置了 lto 且不是 "no" 时才添加参数
    if lto and lto.lower() != "no":
        lines.append(f"        '--lto={lto.lower()}',")

    # 编译线程数（0或负数表示自动分配，不添加参数）
    jobs = config.get("jobs", 0)
    if jobs > 0:
        lines.append(f"        '--jobs={jobs}',")

    # Python 优化
    python_flag = config.get("python_flag", "")
    if python_flag:
        lines.append(f"        '--python-flag={python_flag}',")

    # 静默模式和进度显示
    quiet_mode = config.get("quiet_mode", False)
    if quiet_mode:
        # 静默模式：不显示详细进度，只显示关键信息
        lines.append("        '--quiet',")
    else:
        # 非静默模式：显示详细进度
        if config.get("show_progress", True):
            lines.append("        '--show-progress',")

    # 移除构建文件
    if config.get("remove_output", True):
        lines.append("        '--remove-output',")

    # 不生成 .pyi 文件（仅 module 和 package 模式有效）
    if config.get("no_pyi_file", False) and mode in ("module", "package"):
        lines.append("        '--no-pyi-file',")

    # 跟随导入（自动包含所有导入的模块）
    if config.get("follow_imports", True):
        lines.append("        '--follow-imports',")

    # 自动下载依赖工具（CI环境必需）
    if config.get("assume_yes_for_downloads", False):
        lines.append("        '--assume-yes-for-downloads',")

    # 包含包
    include_packages = config.get("include_packages", "")
    if include_packages:
        for package in _split_items(include_packages):
            lines.append(f"        '--include-package={package}',")

    # 包含模块
    include_modules = config.get("include_modules", "")
    if include_modules:
        for module in _split_items(include_modules):
            lines.append(f"        '--include-module={module}',")

    # 排除导入
    nofollow_imports = config.get("nofollow_imports", "")
    if nofollow_imports:
        for module in _split_items(nofollow_imports):
            lines.append(f"        '--nofollow-import-to={module}',")

    # 数据文件和数据目录（统一处理）
    data_params = [
        ("include_data_files", "--include-data-files"),
        ("include_data_dirs", "--include-data-dir"),
    ]

    for config_key, flag in data_params:
        data_value = config.get(config_key, "")
        if data_value:
            entries = [e.strip() for e in data_value.split() if e.strip()]
            for data_entry in entries:
                if ";" in data_entry:
                    src, dest = data_entry.split(";", 1)
                    src_code = _generate_path_code(src)
                    dest_code = _generate_path_code(dest)
                    lines.append(f"        f'{flag}={{{src_code}}}={{{dest_code}}}',")

    # 插件
    plugins = config.get("plugins", [])
    if isinstance(plugins, str):
        plugins = [p.strip() for p in plugins.split(",") if p.strip()]
    for plugin in plugins:
        lines.append(f"        '--enable-plugin={plugin}',")

    # 关闭初始命令列表
    lines.append("    ]")
    lines.append("")

    # 控制台选项（仅Windows平台）
    if not config.get("show_console", False):
        lines.append("    # 禁用控制台窗口（仅Windows平台）")
        lines.append("    if is_windows:")
        lines.append("        cmd.append('--windows-console-mode=disable')")
        lines.append("")

    # Windows特定参数（仅在Windows平台添加）
    if config.get("icon_file"):
        lines.append("    # Windows图标（仅Windows平台）")
        lines.append("    if is_windows:")
        lines.append("        cmd.append(f'--windows-icon-from-ico={ICON_FILE}')")
        lines.append("")

    if config.get("company_name"):
        lines.append("    # Windows公司名称（仅Windows平台）")
        lines.append("    if is_windows:")
        lines.append("        cmd.append(f'--windows-company-name={COMPANY_NAME}')")
        lines.append("")

    # 产品版本（仅Windows平台）
    lines.append("    # Windows版本信息（仅Windows平台）")
    lines.append("    if is_windows:")
    lines.append("        cmd.append(f'--windows-product-version={VERSION}')")
    lines.append("        cmd.append(f'--windows-file-version={VERSION}')")
    lines.append("")

    # 编译器（根据平台动态选择）
    compiler = config.get("compiler", "")
    if compiler:
        lines.append("    # 根据平台选择编译器")
        lines.append(f"    compiler = '{compiler}'")
        lines.append("    if is_windows:")
        lines.append("        # Windows平台编译器")
        lines.append("        if compiler == 'clang':")
        lines.append("            cmd.append('--clang')")
        lines.append("        elif compiler == 'mingw64':")
        lines.append("            cmd.append('--mingw64')")
        lines.append("        elif compiler == 'clang-cl':")
        lines.append("            cmd.append('--clang-cl')")
        lines.append("        # msvc是默认，不需要参数")
        lines.append("    elif is_linux:")
        lines.append("        # Linux平台编译器")
        lines.append("        if compiler == 'clang':")
        lines.append("            cmd.append('--clang')")
        lines.append("        # gcc是默认，不需要参数")
        lines.append("    elif is_macos:")
        lines.append("        # macOS平台编译器")
        lines.append("        if compiler != 'clang':")
        lines.append("            # clang是macOS默认，其他需要指定")
        lines.append("            if compiler == 'gcc':")
        lines.append(
            "                print(f'{Color.YELLOW}注意: macOS推荐使用Clang{Color.RESET}')"
        )
        lines.append("")

    # 入口文件（最后添加）
    lines.append("    # 添加入口文件")
    lines.append("    cmd.append(ENTRY_FILE)")
    lines.append("")

    # 使用公共模板生成执行和结果部分
    lines.extend(_generate_build_execution())
    lines.extend(_generate_build_result())
    lines.extend(_generate_main_block())

    return "\n".join(lines)


def generate_pyinstaller_script(config: Dict[str, Any], project_dir: Path) -> str:
    """生成 PyInstaller 构建脚本"""
    lines = []

    # 使用公共模板生成头部
    lines.extend(_generate_script_header(config, "PyInstaller"))

    # PyInstaller 特有的额外变量
    extra_vars: List[str] = []
    if config.get("splash_image"):
        extra_vars.append(f"SPLASH_IMAGE = '{config['splash_image']}'")
    lines.extend(_generate_config_section(config, extra_vars if extra_vars else None))
    lines.extend(_generate_build_function_header("PyInstaller"))

    # 添加数据文件分隔符检测（如果需要）
    add_data = config.get("add_data", "")
    if add_data:
        lines.append("    # 添加数据文件（根据操作系统使用不同分隔符）")
        lines.append("    data_separator = ';' if is_windows else ':'")
        lines.append("")

    # 构建命令
    lines.append("    # 构建 PyInstaller 命令")
    lines.append("    cmd = [")
    lines.append("        sys.executable,")
    lines.append("        '-m', 'PyInstaller',")

    # 基本选项
    onefile_mode = config.get("onefile", True)
    if onefile_mode:
        lines.append("        '--onefile',")

    # 输出选项
    lines.append("        f'--distpath={OUTPUT_DIR}',")
    # 非 onefile 模式且输出目录是 build 时，指定工作路径避免冲突
    if not onefile_mode and config.get("output_dir", "build") == "build":
        lines.append("        '--workpath=build/temp',")
    lines.append("        f'--name={PROJECT_NAME}',")

    # 内部目录名称（仅非 onefile 模式）
    if not onefile_mode:
        contents_dir = config.get("contents_directory", ".")
        if contents_dir and contents_dir != ".":
            lines.append(f"        '--contents-directory={contents_dir}',")

    # 控制台选项
    if not config.get("show_console", False):
        lines.append("        '--noconsole',")

    # 清理选项
    if config.get("clean", True):
        lines.append("        '--clean',")

    # 自动确认选项
    if config.get("noconfirm", False):
        lines.append("        '--noconfirm',")

    # 静默模式和日志级别
    quiet_mode = config.get("quiet_mode", False)
    if quiet_mode:
        lines.append("        '--log-level=WARN',")

    # 调试模式
    if config.get("debug", False):
        lines.append("        '--debug=all',")

    # 关闭初始命令列表
    lines.append("    ]")
    lines.append("")

    # 图标（仅 Windows 和 macOS，Linux 不支持）
    if config.get("icon_file"):
        lines.append("    # 图标文件（仅Windows和macOS平台）")
        lines.append("    if is_windows or is_macos:")
        lines.append("        cmd.append(f'--icon={ICON_FILE}')")
        lines.append("")

    # 启动画面（仅单文件模式）
    if config.get("splash_image") and onefile_mode:
        lines.append("    # 启动画面（仅单文件模式）")
        lines.append("    if onefile_mode:")
        lines.append("        cmd.append(f'--splash={SPLASH_IMAGE}')")
        lines.append("")

    # UAC 管理员权限（仅 Windows）
    if config.get("uac_admin", False):
        lines.append("    # UAC管理员权限（仅Windows平台）")
        lines.append("    if is_windows:")
        lines.append("        cmd.append('--uac-admin')")
        lines.append("")

    # 运行时临时目录（仅单文件模式）
    runtime_tmpdir = config.get("runtime_tmpdir", "")
    if runtime_tmpdir and onefile_mode:
        lines.append("    # 运行时临时目录（仅单文件模式）")
        lines.append("    if onefile_mode:")
        lines.append(f"        cmd.append('--runtime-tmpdir={runtime_tmpdir}')")
        lines.append("")

    # 平台特定参数（使用字典映射简化重复代码）
    platform_params = {
        "windows": [
            ("win_version_file", "--version-file", "Windows版本文件"),
            ("win_manifest", "--manifest", "Windows Manifest"),
        ],
        "macos": [
            ("target_architecture", "--target-architecture", "macOS架构"),
            ("osx_bundle_identifier", "--osx-bundle-identifier", "macOS Bundle标识"),
            ("osx_entitlements_file", "--osx-entitlements-file", "macOS权限文件"),
            ("codesign_identity", "--codesign-identity", "macOS代码签名"),
        ],
    }

    for platform_type, params in platform_params.items():
        condition = "is_windows" if platform_type == "windows" else "is_macos"
        for config_key, flag, comment in params:
            value = config.get(config_key, "")
            if value:
                lines.append(
                    f"    # {comment}（仅{'Windows' if platform_type == 'windows' else 'macOS'}平台）"
                )
                lines.append(f"    if {condition}:")
                lines.append(f"        cmd.append('{flag}={value}')")
                lines.append("")

    # 隐藏导入
    hidden_imports = config.get("hidden_imports", "")
    if hidden_imports:
        lines.append("    # 隐藏导入")
        for module in _split_items(hidden_imports):
            lines.append(f"    cmd.append('--hidden-import={module}')")
        lines.append("")

    # 排除模块
    exclude_modules = config.get("exclude_modules", "")
    if exclude_modules:
        lines.append("    # 排除模块")
        for module in _split_items(exclude_modules):
            lines.append(f"    cmd.append('--exclude-module={module}')")
        lines.append("")

    # 收集子模块
    collect_submodules = config.get("collect_submodules", "")
    if collect_submodules:
        lines.append("    # 收集子模块")
        for package in _split_items(collect_submodules):
            lines.append(f"    cmd.append('--collect-submodules={package}')")
        lines.append("")

    # 收集数据文件
    collect_data = config.get("collect_data", "")
    if collect_data:
        lines.append("    # 收集数据文件")
        for package in _split_items(collect_data):
            lines.append(f"    cmd.append('--collect-data={package}')")
        lines.append("")

    # 收集二进制文件
    collect_binaries = config.get("collect_binaries", "")
    if collect_binaries:
        lines.append("    # 收集二进制文件")
        for package in _split_items(collect_binaries):
            lines.append(f"    cmd.append('--collect-binaries={package}')")
        lines.append("")

    # 收集所有（子模块+数据+二进制）
    collect_all = config.get("collect_all", "")
    if collect_all:
        lines.append("    # 收集所有")
        for package in _split_items(collect_all):
            lines.append(f"    cmd.append('--collect-all={package}')")
        lines.append("")

    # 添加数据文件
    if add_data:
        lines.append("    # 添加数据文件")
        entries = [e.strip() for e in add_data.split() if e.strip()]
        for data_entry in entries:
            if ";" in data_entry:
                src, dest = data_entry.split(";", 1)
                src_code = _generate_path_code(src)
                dest_code = _generate_path_code(dest)
                lines.append(
                    f"    cmd.append(f'--add-data={{{src_code}}}{{data_separator}}{{{dest_code}}}')"
                )
            else:
                lines.append(f"    cmd.append('--add-data={data_entry}')")
        lines.append("")

    # 添加二进制文件
    add_binary = config.get("add_binary", "")
    if add_binary:
        lines.append("    # 添加二进制文件")
        entries = [e.strip() for e in add_binary.split() if e.strip()]
        for binary_entry in entries:
            if ";" in binary_entry:
                src, dest = binary_entry.split(";", 1)
                src_code = _generate_path_code(src)
                dest_code = _generate_path_code(dest)
                lines.append(
                    f"    cmd.append(f'--add-binary={{{src_code}}}{{data_separator}}{{{dest_code}}}')"
                )
            else:
                lines.append(f"    cmd.append('--add-binary={binary_entry}')")
        lines.append("")

    # 入口文件（最后添加）
    lines.append("    # 添加入口文件")
    lines.append("    cmd.append(ENTRY_FILE)")
    lines.append("")

    # PyInstaller 特有的清理代码
    cleanup_code = [
        "        # 清理 .spec 文件",
        "        spec_file = f'{PROJECT_NAME}.spec'",
        "        if os.path.exists(spec_file):",
        "            os.remove(spec_file)",
        "            print(f'{Color.GRAY}Cleaned: {spec_file}{Color.RESET}')",
    ]

    # 使用公共模板生成执行和结果部分
    lines.extend(_generate_build_execution())
    lines.extend(_generate_build_result(cleanup_code))
    lines.extend(_generate_main_block())

    return "\n".join(lines)


def generate_build_script(
    config: Dict[str, Any], project_dir: Path
) -> tuple[bool, str]:
    """
    生成构建脚本
    返回 (是否成功, 消息)
    """
    try:
        build_tool = config.get("build_tool", "nuitka")

        # 生成脚本内容
        if build_tool == "nuitka":
            script_content = generate_nuitka_script(config, project_dir)
            script_name = "build_nuitka.py"
        elif build_tool == "pyinstaller":
            script_content = generate_pyinstaller_script(config, project_dir)
            script_name = "build_pyinstaller.py"
        else:
            return False, f"不支持的构建工具: {build_tool}"

        # 保存脚本
        script_path = project_dir / script_name
        script_path.write_text(script_content, encoding="utf-8")

        # 设置可执行权限（Unix系统）
        import platform

        if platform.system() != "Windows":
            import stat

            script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)

        return True, f"脚本已生成: {script_name}"

    except Exception as e:
        return False, f"生成脚本失败: {e}"
