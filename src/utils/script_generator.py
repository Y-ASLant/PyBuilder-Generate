"""
脚本生成器模块
根据配置生成 Nuitka 或 PyInstaller 构建脚本
"""

import re
from pathlib import Path
from typing import Dict, Any


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


def generate_nuitka_script(config: Dict[str, Any], project_dir: Path) -> str:
    """生成 Nuitka 构建脚本"""
    lines = []

    # 脚本头部
    lines.append("# -*- coding: utf-8 -*-")
    lines.append('"""')
    lines.append(f"{config['project_name']} - Nuitka 构建脚本")
    lines.append(f"版本: {config['version']}")
    lines.append('"""')
    lines.append("")
    lines.append("import sys")
    lines.append("import os")
    lines.append("import subprocess")
    lines.append("import shutil")
    lines.append("import time")
    lines.append("")
    lines.append("")
    lines.append(COLOR_CLASS_CODE)
    lines.append("")

    # 配置部分
    lines.append("# 构建配置")
    lines.append(f"PROJECT_NAME = '{config['project_name']}'")
    lines.append(f"VERSION = '{config['version']}'")
    lines.append(f"ENTRY_FILE = '{config['entry_file']}'")
    if config.get("company_name"):
        lines.append(f"COMPANY_NAME = '{config['company_name']}'")
    if config.get("icon_file"):
        lines.append(f"ICON_FILE = '{config['icon_file']}'")
    lines.append(f"OUTPUT_DIR = '{config['output_dir']}'")
    lines.append("")

    # 构建函数
    lines.append("def build():")
    lines.append('    """执行 Nuitka 构建"""')
    lines.append("    # 获取终端宽度")
    lines.append("    width = shutil.get_terminal_size().columns")
    lines.append("    separator = '-' * width")
    lines.append("    start_time = time.time()")
    lines.append("")
    lines.append(
        "    print(f'{Color.CYAN}{Color.BOLD}Building {PROJECT_NAME} v{VERSION}{Color.RESET}')"
    )
    lines.append("    print(separator)")
    lines.append("")

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

    # 控制台选项
    if not config.get("show_console", False):
        lines.append("        '--disable-console',")

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

    # 编译器
    compiler = config.get("compiler", "msvc")
    if compiler == "clang":
        lines.append("        '--clang',")
    elif compiler == "mingw64":
        lines.append("        '--mingw64',")
    elif compiler == "clang-cl":
        lines.append("        '--clang-cl',")

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
        packages = [
            p.strip() for p in re.split(r"[,\s，]+", include_packages) if p.strip()
        ]
        for package in packages:
            lines.append(f"        '--include-package={package}',")

    # 包含模块
    include_modules = config.get("include_modules", "")
    if include_modules:
        modules = [
            m.strip() for m in re.split(r"[,\s，]+", include_modules) if m.strip()
        ]
        for module in modules:
            lines.append(f"        '--include-module={module}',")

    # 排除导入
    nofollow_imports = config.get("nofollow_imports", "")
    if nofollow_imports:
        modules = [
            m.strip() for m in re.split(r"[,\s，]+", nofollow_imports) if m.strip()
        ]
        for module in modules:
            lines.append(f"        '--nofollow-import-to={module}',")

    # 数据文件（支持 ; 分隔符，转换为 Nuitka 的 = 格式）
    include_data_files = config.get("include_data_files", "")
    if include_data_files:
        entries = [e.strip() for e in include_data_files.split() if e.strip()]
        for data_entry in entries:
            if ";" in data_entry:
                src, dest = data_entry.split(";", 1)
                # 将路径分割为部分，用于 os.path.join
                src_parts = [p for p in src.replace("\\", "/").split("/") if p]
                dest_parts = [p for p in dest.replace("\\", "/").split("/") if p]

                # 生成 os.path.join 调用
                src_code = (
                    f"os.path.join({', '.join(repr(p) for p in src_parts)})"
                    if len(src_parts) > 1
                    else repr(src_parts[0] if src_parts else src)
                )
                dest_code = (
                    f"os.path.join({', '.join(repr(p) for p in dest_parts)})"
                    if len(dest_parts) > 1
                    else repr(dest_parts[0] if dest_parts else dest)
                )

                lines.append(
                    f"        f'--include-data-files={{{src_code}}}={{{dest_code}}}',"
                )

    # 数据目录（支持 ; 分隔符，转换为 Nuitka 的 = 格式）
    include_data_dirs = config.get("include_data_dirs", "")
    if include_data_dirs:
        entries = [e.strip() for e in include_data_dirs.split() if e.strip()]
        for data_entry in entries:
            if ";" in data_entry:
                src, dest = data_entry.split(";", 1)
                # 将路径分割为部分，用于 os.path.join
                src_parts = [p for p in src.replace("\\", "/").split("/") if p]
                dest_parts = [p for p in dest.replace("\\", "/").split("/") if p]

                # 生成 os.path.join 调用
                src_code = (
                    f"os.path.join({', '.join(repr(p) for p in src_parts)})"
                    if len(src_parts) > 1
                    else repr(src_parts[0] if src_parts else src)
                )
                dest_code = (
                    f"os.path.join({', '.join(repr(p) for p in dest_parts)})"
                    if len(dest_parts) > 1
                    else repr(dest_parts[0] if dest_parts else dest)
                )

                lines.append(
                    f"        f'--include-data-dir={{{src_code}}}={{{dest_code}}}',"
                )

    # 插件
    plugins = config.get("plugins", [])
    if isinstance(plugins, str):
        plugins = [p.strip() for p in plugins.split(",") if p.strip()]
    for plugin in plugins:
        lines.append(f"        '--enable-plugin={plugin}',")

    # 图标
    if config.get("icon_file"):
        lines.append("        f'--windows-icon-from-ico={ICON_FILE}',")

    # 公司名称
    if config.get("company_name"):
        lines.append("        f'--windows-company-name={COMPANY_NAME}',")

    # 产品版本
    lines.append("        f'--windows-product-version={VERSION}',")
    lines.append("        f'--windows-file-version={VERSION}',")

    # 入口文件
    lines.append("        ENTRY_FILE,")
    lines.append("    ]")
    lines.append("")

    # 执行构建
    lines.append("    # 执行构建")
    lines.append("    print(f'{Color.GRAY}Command:{Color.RESET}')")
    lines.append("    print(f'{Color.GRAY}' + ' '.join(cmd) + f'{Color.RESET}')")
    lines.append("    print(separator)")
    lines.append("    print(f'{Color.YELLOW}Building, please wait...{Color.RESET}')")
    lines.append("    print()")
    lines.append("")
    lines.append("    try:")
    lines.append("        subprocess.run(cmd, check=True)")
    lines.append("        print(separator)")
    lines.append("        elapsed_time = time.time() - start_time")
    lines.append("        minutes = int(elapsed_time // 60)")
    lines.append("        seconds = int(elapsed_time % 60)")
    lines.append(
        "        print(f'{Color.GREEN}{Color.BOLD}Build successful!{Color.RESET}')"
    )
    lines.append("        abs_output = os.path.abspath(OUTPUT_DIR)")
    lines.append("        print(f'{Color.GREEN}Output: {abs_output}{Color.RESET}')")
    lines.append("        if minutes > 0:")
    lines.append(
        "            print(f'{Color.CYAN}Build time: {minutes}m {seconds}s{Color.RESET}')"
    )
    lines.append("        else:")
    lines.append(
        "            print(f'{Color.CYAN}Build time: {seconds}s{Color.RESET}')"
    )
    lines.append("        return 0")
    lines.append("    except subprocess.CalledProcessError as e:")
    lines.append("        print(separator)")
    lines.append(
        "        print(f'{Color.RED}{Color.BOLD}Build failed: {Color.RESET}{Color.RED}{e}{Color.RESET}')"
    )
    lines.append("        return 1")
    lines.append("    except Exception as e:")
    lines.append("        print(separator)")
    lines.append(
        "        print(f'{Color.RED}{Color.BOLD}Error: {Color.RESET}{Color.RED}{e}{Color.RESET}')"
    )
    lines.append("        return 1")
    lines.append("")

    # 主函数
    lines.append("")
    lines.append("if __name__ == '__main__':")
    lines.append("    sys.exit(build())")
    lines.append("")

    return "\n".join(lines)


def generate_pyinstaller_script(config: Dict[str, Any], project_dir: Path) -> str:
    """生成 PyInstaller 构建脚本"""
    lines = []

    # 脚本头部
    lines.append("# -*- coding: utf-8 -*-")
    lines.append('"""')
    lines.append(f"{config['project_name']} - PyInstaller 构建脚本")
    lines.append(f"版本: {config['version']}")
    lines.append('"""')
    lines.append("")
    lines.append("import sys")
    lines.append("import subprocess")
    lines.append("import shutil")
    lines.append("import time")
    lines.append("import os")
    lines.append("")
    lines.append("")
    lines.append(COLOR_CLASS_CODE)
    lines.append("")

    # 配置部分
    lines.append("# 构建配置")
    lines.append(f"PROJECT_NAME = '{config['project_name']}'")
    lines.append(f"VERSION = '{config['version']}'")
    if config.get("company_name"):
        lines.append(f"COMPANY_NAME = '{config['company_name']}'")
    lines.append(f"ENTRY_FILE = '{config['entry_file']}'")
    if config.get("icon_file"):
        lines.append(f"ICON_FILE = '{config['icon_file']}'")
    if config.get("splash_image"):
        lines.append(f"SPLASH_IMAGE = '{config['splash_image']}'")
    lines.append(f"OUTPUT_DIR = '{config['output_dir']}'")
    lines.append("")

    # 构建函数
    lines.append("def build():")
    lines.append('    """执行 PyInstaller 构建"""')
    lines.append("    # 获取终端宽度")
    lines.append("    width = shutil.get_terminal_size().columns")
    lines.append("    separator = '-' * width")
    lines.append("    start_time = time.time()")
    lines.append("")
    lines.append(
        "    print(f'{Color.CYAN}{Color.BOLD}Building {PROJECT_NAME} v{VERSION}{Color.RESET}')"
    )
    lines.append("    print(separator)")
    lines.append("")

    # 添加数据文件分隔符检测（如果需要）
    add_data = config.get("add_data", "")
    if add_data:
        lines.append("    # 添加数据文件（根据操作系统使用不同分隔符）")
        lines.append("    import platform")
        lines.append(
            "    data_separator = ';' if platform.system() == 'Windows' else ':'"
        )
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

    # 图标
    if config.get("icon_file"):
        lines.append("        f'--icon={ICON_FILE}',")

    # 启动画面（仅单文件模式）
    if config.get("splash_image") and onefile_mode:
        lines.append("        f'--splash={SPLASH_IMAGE}',")

    # UAC 管理员权限
    if config.get("uac_admin", False):
        lines.append("        '--uac-admin',")

    # 运行时临时目录（仅单文件模式）
    runtime_tmpdir = config.get("runtime_tmpdir", "")
    if runtime_tmpdir and onefile_mode:
        lines.append(f"        '--runtime-tmpdir={runtime_tmpdir}',")

    # 系统特性参数（使用字典映射）
    platform_params = {
        "target_architecture": "--target-architecture",
        "win_version_file": "--version-file",
        "win_manifest": "--manifest",
        "osx_bundle_identifier": "--osx-bundle-identifier",
        "osx_entitlements_file": "--osx-entitlements-file",
        "codesign_identity": "--codesign-identity",
    }

    for config_key, param_name in platform_params.items():
        value = config.get(config_key, "")
        if value:
            lines.append(f"        '{param_name}={value}',")

    # 隐藏导入
    hidden_imports = config.get("hidden_imports", "")
    if hidden_imports:
        # 支持多种分隔符：空格、逗号
        modules = [m.strip() for m in re.split(r"[,\s]+", hidden_imports) if m.strip()]
        for module in modules:
            lines.append(f"        '--hidden-import={module}',")

    # 排除模块
    exclude_modules = config.get("exclude_modules", "")
    if exclude_modules:
        # 支持多种分隔符：空格、逗号
        modules = [m.strip() for m in re.split(r"[,\s]+", exclude_modules) if m.strip()]
        for module in modules:
            lines.append(f"        '--exclude-module={module}',")

    # 收集子模块
    collect_submodules = config.get("collect_submodules", "")
    if collect_submodules:
        # 支持多种分隔符：空格、逗号
        packages = [
            p.strip() for p in re.split(r"[,\s]+", collect_submodules) if p.strip()
        ]
        for package in packages:
            lines.append(f"        '--collect-submodules={package}',")

    # 收集数据文件
    collect_data = config.get("collect_data", "")
    if collect_data:
        # 支持多种分隔符：空格、逗号
        packages = [p.strip() for p in re.split(r"[,\s]+", collect_data) if p.strip()]
        for package in packages:
            lines.append(f"        '--collect-data={package}',")

    # 收集二进制文件
    collect_binaries = config.get("collect_binaries", "")
    if collect_binaries:
        # 支持多种分隔符：空格、逗号
        packages = [
            p.strip() for p in re.split(r"[,\s]+", collect_binaries) if p.strip()
        ]
        for package in packages:
            lines.append(f"        '--collect-binaries={package}',")

    # 收集所有（子模块+数据+二进制）
    collect_all = config.get("collect_all", "")
    if collect_all:
        # 支持多种分隔符：空格、逗号
        packages = [p.strip() for p in re.split(r"[,\s]+", collect_all) if p.strip()]
        for package in packages:
            lines.append(f"        '--collect-all={package}',")

    # 添加数据文件
    if add_data:
        entries = [e.strip() for e in add_data.split() if e.strip()]
        for data_entry in entries:
            if ";" in data_entry:
                src, dest = data_entry.split(";", 1)
                # 将路径分割为部分，用于 os.path.join
                src_parts = [p for p in src.replace("\\", "/").split("/") if p]
                dest_parts = [p for p in dest.replace("\\", "/").split("/") if p]

                # 生成 os.path.join 调用
                src_code = (
                    f"os.path.join({', '.join(repr(p) for p in src_parts)})"
                    if len(src_parts) > 1
                    else repr(src_parts[0] if src_parts else src)
                )
                dest_code = (
                    f"os.path.join({', '.join(repr(p) for p in dest_parts)})"
                    if len(dest_parts) > 1
                    else repr(dest_parts[0] if dest_parts else dest)
                )

                lines.append(
                    f"        f'--add-data={{{src_code}}}{{data_separator}}{{{dest_code}}}',"
                )
            else:
                lines.append(f"        '--add-data={data_entry}',")

    # 添加二进制文件
    add_binary = config.get("add_binary", "")
    if add_binary:
        entries = [e.strip() for e in add_binary.split() if e.strip()]
        for binary_entry in entries:
            if ";" in binary_entry:
                src, dest = binary_entry.split(";", 1)
                # 将路径分割为部分，用于 os.path.join
                src_parts = [p for p in src.replace("\\", "/").split("/") if p]
                dest_parts = [p for p in dest.replace("\\", "/").split("/") if p]

                # 生成 os.path.join 调用
                src_code = (
                    f"os.path.join({', '.join(repr(p) for p in src_parts)})"
                    if len(src_parts) > 1
                    else repr(src_parts[0] if src_parts else src)
                )
                dest_code = (
                    f"os.path.join({', '.join(repr(p) for p in dest_parts)})"
                    if len(dest_parts) > 1
                    else repr(dest_parts[0] if dest_parts else dest)
                )

                lines.append(
                    f"        f'--add-binary={{{src_code}}}{{data_separator}}{{{dest_code}}}',"
                )
            else:
                lines.append(f"        '--add-binary={binary_entry}',")

    # 入口文件
    lines.append("        ENTRY_FILE,")
    lines.append("    ]")
    lines.append("")

    # 执行构建
    lines.append("    # 执行构建")
    lines.append("    print(f'{Color.GRAY}Command:{Color.RESET}')")
    lines.append("    print(f'{Color.GRAY}' + ' '.join(cmd) + f'{Color.RESET}')")
    lines.append("    print(separator)")
    lines.append("    print(f'{Color.YELLOW}Building, please wait...{Color.RESET}')")
    lines.append("    print()")
    lines.append("")
    lines.append("    try:")
    lines.append("        subprocess.run(cmd, check=True)")
    lines.append("        print(separator)")
    lines.append("        elapsed_time = time.time() - start_time")
    lines.append("        minutes = int(elapsed_time // 60)")
    lines.append("        seconds = int(elapsed_time % 60)")
    lines.append(
        "        print(f'{Color.GREEN}{Color.BOLD}Build successful!{Color.RESET}')"
    )
    lines.append("        # 清理 .spec 文件")
    lines.append("        spec_file = f'{PROJECT_NAME}.spec'")
    lines.append("        if os.path.exists(spec_file):")
    lines.append("            os.remove(spec_file)")
    lines.append("            print(f'{Color.GRAY}Cleaned: {spec_file}{Color.RESET}')")
    lines.append("        abs_output = os.path.abspath(OUTPUT_DIR)")
    lines.append("        print(f'{Color.GREEN}Output: {abs_output}{Color.RESET}')")
    lines.append("        if minutes > 0:")
    lines.append(
        "            print(f'{Color.CYAN}Build time: {minutes}m {seconds}s{Color.RESET}')"
    )
    lines.append("        else:")
    lines.append(
        "            print(f'{Color.CYAN}Build time: {seconds}s{Color.RESET}')"
    )
    lines.append("        return 0")
    lines.append("    except subprocess.CalledProcessError as e:")
    lines.append("        print(separator)")
    lines.append(
        "        print(f'{Color.RED}{Color.BOLD}Build failed: {Color.RESET}{Color.RED}{e}{Color.RESET}')"
    )
    lines.append("        return 1")
    lines.append("    except Exception as e:")
    lines.append("        print(separator)")
    lines.append(
        "        print(f'{Color.RED}{Color.BOLD}Error: {Color.RESET}{Color.RED}{e}{Color.RESET}')"
    )
    lines.append("        return 1")
    lines.append("")

    # 主函数
    lines.append("")
    lines.append("if __name__ == '__main__':")
    lines.append("    sys.exit(build())")
    lines.append("")

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
