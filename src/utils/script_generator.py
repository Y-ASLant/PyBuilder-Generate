"""
脚本生成器模块
根据配置生成 Nuitka 或 PyInstaller 构建脚本
"""

import re
from pathlib import Path
from typing import Dict, Any


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
    lines.append("import subprocess")
    lines.append("import shutil")
    lines.append("import time")
    lines.append("")
    lines.append("")
    lines.append("# ANSI 颜色代码")
    lines.append("class Color:")
    lines.append("    RESET = '\\033[0m'")
    lines.append("    BOLD = '\\033[1m'")
    lines.append("    GREEN = '\\033[92m'")
    lines.append("    YELLOW = '\\033[93m'")
    lines.append("    RED = '\\033[91m'")
    lines.append("    CYAN = '\\033[96m'")
    lines.append("    GRAY = '\\033[90m'")
    lines.append("")
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
        "    print(f'{Color.CYAN}{Color.BOLD}开始构建 {PROJECT_NAME} v{VERSION} {Color.RESET}')"
    )
    lines.append("    print(separator)")
    lines.append("")

    # 构建命令
    lines.append("    # 构建 Nuitka 命令")
    lines.append("    cmd = [")
    lines.append("        sys.executable,")
    lines.append("        '-m', 'nuitka',")

    # 基本选项
    if config.get("standalone", True):
        lines.append("        '--standalone',")
    if config.get("onefile", True):
        lines.append("        '--onefile',")

    # 输出选项
    lines.append("        f'--output-dir={OUTPUT_DIR}',")

    # 控制台选项
    if not config.get("show_console", False):
        lines.append("        '--disable-console',")

    # 性能选项
    if config.get("lto", False):
        lines.append("        '--lto=yes',")

    jobs = config.get("jobs", 4)
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
    lines.append("    print(f'{Color.GRAY}执行命令:{Color.RESET}')")
    lines.append("    print(f'{Color.GRAY}' + ' '.join(cmd) + f'{Color.RESET}')")
    lines.append("    print(separator)")
    lines.append("    print(f'{Color.YELLOW}正在执行构建，请稍候...{Color.RESET}')")
    lines.append("    print()")
    lines.append("")
    lines.append("    try:")
    lines.append("        subprocess.run(cmd, check=True)")
    lines.append("        print(separator)")
    lines.append("        elapsed_time = time.time() - start_time")
    lines.append("        minutes = int(elapsed_time // 60)")
    lines.append("        seconds = int(elapsed_time % 60)")
    lines.append("        print(f'{Color.GREEN}{Color.BOLD}构建成功！{Color.RESET}')")
    lines.append("        import os")
    lines.append("        abs_output = os.path.abspath(OUTPUT_DIR)")
    lines.append("        print(f'{Color.GREEN}输出目录: {abs_output}{Color.RESET}')")
    lines.append("        if minutes > 0:")
    lines.append(
        "            print(f'{Color.CYAN}本次构建时长: {minutes}分{seconds}秒{Color.RESET}')"
    )
    lines.append("        else:")
    lines.append(
        "            print(f'{Color.CYAN}本次构建时长: {seconds}秒{Color.RESET}')"
    )
    lines.append("        return 0")
    lines.append("    except subprocess.CalledProcessError as e:")
    lines.append("        print(separator)")
    lines.append(
        "        print(f'{Color.RED}{Color.BOLD}✗ 构建失败: {Color.RESET}{Color.RED}{e}{Color.RESET}')"
    )
    lines.append("        return 1")
    lines.append("    except Exception as e:")
    lines.append("        print(separator)")
    lines.append(
        "        print(f'{Color.RED}{Color.BOLD}✗ 发生错误: {Color.RESET}{Color.RED}{e}{Color.RESET}')"
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
    lines.append("# ANSI 颜色代码")
    lines.append("class Color:")
    lines.append("    RESET = '\\033[0m'")
    lines.append("    BOLD = '\\033[1m'")
    lines.append("    GREEN = '\\033[92m'")
    lines.append("    YELLOW = '\\033[93m'")
    lines.append("    RED = '\\033[91m'")
    lines.append("    CYAN = '\\033[96m'")
    lines.append("    GRAY = '\\033[90m'")
    lines.append("")
    lines.append("")

    # 配置部分
    lines.append("# 构建配置")
    lines.append(f"PROJECT_NAME = '{config['project_name']}'")
    lines.append(f"VERSION = '{config['version']}'")
    lines.append(f"ENTRY_FILE = '{config['entry_file']}'")
    if config.get("icon_file"):
        lines.append(f"ICON_FILE = '{config['icon_file']}'")
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
        "    print(f'{Color.CYAN}{Color.BOLD}开始构建 {PROJECT_NAME} v{VERSION}{Color.RESET}')"
    )
    lines.append("    print(separator)")
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

    # UAC 管理员权限
    if config.get("uac_admin", False):
        lines.append("        '--uac-admin',")

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

    # 添加数据文件
    add_data = config.get("add_data", "")
    if add_data:
        # 按空格分割，每个条目应该是 src;dest 格式（保留分号）
        entries = [e.strip() for e in add_data.split() if e.strip()]
        for data_entry in entries:
            lines.append(f"        '--add-data={data_entry}',")

    # 入口文件
    lines.append("        ENTRY_FILE,")
    lines.append("    ]")
    lines.append("")

    # 执行构建
    lines.append("    # 执行构建")
    lines.append("    print(f'{Color.GRAY}执行命令:{Color.RESET}')")
    lines.append("    print(f'{Color.GRAY}' + ' '.join(cmd) + f'{Color.RESET}')")
    lines.append("    print(separator)")
    lines.append("    print(f'{Color.YELLOW}正在执行构建，请稍候...{Color.RESET}')")
    lines.append("    print()")
    lines.append("")
    lines.append("    try:")
    lines.append("        subprocess.run(cmd, check=True)")
    lines.append("        print(separator)")
    lines.append("        elapsed_time = time.time() - start_time")
    lines.append("        minutes = int(elapsed_time // 60)")
    lines.append("        seconds = int(elapsed_time % 60)")
    lines.append("        print(f'{Color.GREEN}{Color.BOLD}构建成功！{Color.RESET}')")
    lines.append("        # 清理 .spec 文件")
    lines.append("        spec_file = f'{PROJECT_NAME}.spec'")
    lines.append("        if os.path.exists(spec_file):")
    lines.append("            os.remove(spec_file)")
    lines.append("            print(f'{Color.GRAY}已清理: {spec_file}{Color.RESET}')")
    lines.append("        abs_output = os.path.abspath(OUTPUT_DIR)")
    lines.append("        print(f'{Color.GREEN}输出目录: {abs_output}{Color.RESET}')")
    lines.append("        if minutes > 0:")
    lines.append(
        "            print(f'{Color.CYAN}本次构建时长: {minutes}分{seconds}秒{Color.RESET}')"
    )
    lines.append("        else:")
    lines.append(
        "            print(f'{Color.CYAN}本次构建时长: {seconds}秒{Color.RESET}')"
    )
    lines.append("        return 0")
    lines.append("    except subprocess.CalledProcessError as e:")
    lines.append("        print(separator)")
    lines.append(
        "        print(f'{Color.RED}{Color.BOLD}✗ 构建失败: {Color.RESET}{Color.RED}{e}{Color.RESET}')"
    )
    lines.append("        return 1")
    lines.append("    except Exception as e:")
    lines.append("        print(separator)")
    lines.append(
        "        print(f'{Color.RED}{Color.BOLD}✗ 发生错误: {Color.RESET}{Color.RED}{e}{Color.RESET}')"
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
