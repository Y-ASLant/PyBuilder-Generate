"""
构建配置管理模块
用于管理项目目录中的 build_config.yaml
"""

from pathlib import Path
from typing import Dict, Any
import platform


# 默认构建配置
DEFAULT_BUILD_CONFIG = {
    "project_name": "MyApp",
    "version": "1.0.0",
    "company_name": "",
    "entry_file": "main.py",
    "icon_file": "",
    "build_tool": "pyinstaller",  # pyinstaller | nuitka
    "output_dir": "dist",
    "standalone": True,
    "onefile": True,
    "show_console": False,
    "quiet_mode": False,
    # Nuitka特有
    "remove_output": True,
    "show_progress": True,
    "lto": False,
    "jobs": 4,
    "python_flag": "",  # 空字符串表示不使用，可选值: "-O", "no_asserts", "no_docstrings"
    "compiler": "msvc",
    # PyInstaller特有
    "clean": True,
    "debug": False,
    "contents_directory": ".",
    "uac_admin": False,
    "hidden_imports": "",
    "exclude_modules": "",
    "add_data": "",
    "plugins": [],
    "exclude_packages": [],
}


def get_build_config_path(project_dir: Path) -> Path:
    """获取项目目录中的 build_config.yaml 路径"""
    return project_dir / "build_config.yaml"


def load_build_config(project_dir: Path) -> Dict[str, Any]:
    """
    从项目目录加载构建配置
    如果文件不存在，返回默认配置
    """
    config = DEFAULT_BUILD_CONFIG.copy()
    path = get_build_config_path(project_dir)

    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                current_list = None

                for line in f:
                    s = line.strip()

                    # 跳过注释和空行
                    if not s or s.startswith("#"):
                        continue

                    # 处理列表项
                    if s.startswith("- "):
                        if current_list is not None:
                            item = s[2:].strip()
                            current_list.append(item)
                        continue

                    # 处理键值对
                    if ":" in s:
                        key, value = s.split(":", 1)
                        key = key.strip()
                        value = value.strip()

                        # 去除行内注释
                        if "#" in value:
                            value = value.split("#")[0].strip()

                        # 如果值为空，可能是列表开始
                        if not value:
                            if key in ["plugins", "exclude_packages"]:
                                config[key] = []
                                current_list = config[key]
                            continue

                        # 重置列表指针
                        current_list = None

                        # 根据默认配置的类型转换值
                        if key in config:
                            default_value = DEFAULT_BUILD_CONFIG[key]
                            if isinstance(default_value, bool):
                                config[key] = value.lower() in ["true", "yes", "1"]
                            elif isinstance(default_value, int):
                                try:
                                    config[key] = int(value)
                                except ValueError:
                                    pass
                            elif isinstance(default_value, list):
                                # 单行列表格式
                                config[key] = [
                                    v.strip() for v in value.split(",") if v.strip()
                                ]
                            else:
                                config[key] = value
    except Exception as e:
        print(f"加载构建配置失败: {e}")

    # 根据操作系统设置默认编译器（如果未指定）
    if not config.get("compiler"):
        os_type = platform.system()
        if os_type == "Windows":
            config["compiler"] = "msvc"
        elif os_type == "Linux":
            config["compiler"] = "gcc"
        else:  # macOS
            config["compiler"] = "clang"

    return config


def save_build_config(project_dir: Path, config: Dict[str, Any]) -> bool:
    """
    保存构建配置到项目目录
    返回是否成功
    """
    try:
        path = get_build_config_path(project_dir)

        lines = []
        lines.append("# build_config.yaml - 项目构建配置\n")
        lines.append("\n")
        lines.append("# 项目基本信息\n")
        lines.append(f"project_name: {config['project_name']}\n")
        lines.append(f"version: {config['version']}\n")
        if config.get("company_name"):
            lines.append(f"company_name: {config['company_name']}\n")
        lines.append(f"entry_file: {config['entry_file']}\n")
        if config.get("icon_file"):
            lines.append(f"icon_file: {config['icon_file']}\n")
        lines.append("\n")

        lines.append("# 构建配置\n")
        lines.append(f"build_tool: {config['build_tool']}\n")
        lines.append(f"output_dir: {config['output_dir']}\n")
        lines.append(f"quiet_mode: {str(config.get('quiet_mode', False)).lower()}\n")
        lines.append("\n")

        lines.append("# 打包选项\n")
        lines.append(f"onefile: {str(config['onefile']).lower()}\n")
        lines.append(f"show_console: {str(config['show_console']).lower()}\n")

        # Nuitka特有选项
        if config.get("build_tool") == "nuitka":
            lines.append(f"standalone: {str(config.get('standalone', True)).lower()}\n")
            lines.append(
                f"remove_output: {str(config.get('remove_output', True)).lower()}\n"
            )
            lines.append(
                f"show_progress: {str(config.get('show_progress', True)).lower()}\n"
            )
            lines.append(f"lto: {str(config.get('lto', False)).lower()}\n")
            lines.append(f"jobs: {config.get('jobs', 4)}\n")
            python_flag = config.get("python_flag", "")
            if python_flag:
                lines.append(f"python_flag: {python_flag}\n")
            lines.append(f"compiler: {config.get('compiler', 'msvc')}\n")

        # PyInstaller特有选项
        if config.get("build_tool") == "pyinstaller":
            lines.append(f"clean: {str(config.get('clean', True)).lower()}\n")
            lines.append(f"debug: {str(config.get('debug', False)).lower()}\n")
            lines.append(
                f"show_progressbar: {str(config.get('show_progressbar', True)).lower()}\n"
            )
            lines.append(
                f"contents_directory: {config.get('contents_directory', '.')}\n"
            )
            lines.append(f"uac_admin: {str(config.get('uac_admin', False)).lower()}\n")
            if config.get("hidden_imports"):
                lines.append(f"hidden_imports: {config.get('hidden_imports')}\n")
            if config.get("exclude_modules"):
                lines.append(f"exclude_modules: {config.get('exclude_modules')}\n")
            if config.get("add_data"):
                lines.append(f"add_data: {config.get('add_data')}\n")

        lines.append("\n")

        # 插件列表
        plugins = config.get("plugins")
        if plugins:
            lines.append("# 插件\n")
            # 如果plugins是字符串，转换为列表
            if isinstance(plugins, str):
                plugin_list = [p.strip() for p in plugins.split(",") if p.strip()]
            else:
                plugin_list = plugins

            if plugin_list:
                lines.append("plugins:\n")
                for plugin in plugin_list:
                    lines.append(f"  - {plugin}\n")
                lines.append("\n")

        # 排除包列表
        if config.get("exclude_packages"):
            lines.append("# 排除的包\n")
            lines.append("exclude_packages:\n")
            for pkg in config["exclude_packages"]:
                lines.append(f"  - {pkg}\n")
            lines.append("\n")

        path.write_text("".join(lines), encoding="utf-8")
        return True

    except Exception as e:
        print(f"保存构建配置失败: {e}")
        return False


def validate_build_config(
    config: Dict[str, Any], project_dir: Path
) -> tuple[bool, str]:
    """
    验证构建配置是否有效
    返回 (是否有效, 错误信息)
    """
    # 检查项目名称
    if not config.get("project_name"):
        return False, "项目名称不能为空"

    # 检查入口文件
    entry_file = config.get("entry_file", "")
    if not entry_file:
        return False, "入口文件不能为空"

    entry_path = project_dir / entry_file
    if not entry_path.exists():
        return False, f"入口文件不存在: {entry_file}"

    if not entry_path.suffix == ".py":
        return False, "入口文件必须是 .py 文件"

    # 检查图标文件（如果指定）
    icon_file = config.get("icon_file", "")
    if icon_file:
        icon_path = project_dir / icon_file
        if not icon_path.exists():
            return False, f"图标文件不存在: {icon_file}"

    # 检查构建工具
    build_tool = config.get("build_tool", "")
    if build_tool not in ["pyinstaller", "nuitka"]:
        return False, "构建工具必须是 pyinstaller 或 nuitka"

    return True, ""
