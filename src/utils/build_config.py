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
    # Nuitka 编译模式（推荐使用）
    # 可选值: accelerated, standalone, onefile, app, app-dist, module, package
    # 空字符串表示自动根据 standalone/onefile 组合决定
    "mode": "",
    # 向后兼容配置（仅在 mode 为空时生效）
    "standalone": True,
    "onefile": True,
    "show_console": False,
    "quiet_mode": False,
    # Nuitka特有
    "remove_output": True,
    "show_progress": True,
    "lto": "no",  # yes/no/auto - 链接时优化
    "jobs": 0,  # 0或负数表示自动分配，正数表示指定线程数
    "python_flag": "",  # 空字符串表示不使用，可选值: "-O", "no_asserts", "no_docstrings"
    "compiler": "msvc",
    "no_pyi_file": False,
    "follow_imports": True,  # 跟随所有导入的模块
    "assume_yes_for_downloads": False,  # 自动下载依赖工具
    # Nuitka 数据导入选项
    "include_packages": "",  # 包含的包
    "include_modules": "",  # 包含的模块
    "nofollow_imports": "",  # 不跟随的导入
    "include_data_files": "",  # 数据文件
    "include_data_dirs": "",  # 数据目录
    # PyInstaller特有
    "clean": True,
    "noconfirm": False,
    "debug": False,
    "contents_directory": ".",
    "uac_admin": False,
    "hidden_imports": "",
    "exclude_modules": "",
    "add_data": "",
    "add_binary": "",
    "splash_image": "",
    "collect_submodules": "",
    "collect_data": "",
    "collect_binaries": "",
    "collect_all": "",
    "runtime_tmpdir": "",
    "target_architecture": "",
    # 系统特性
    "win_version_file": "",
    "win_manifest": "",
    "osx_bundle_identifier": "",
    "osx_entitlements_file": "",
    "codesign_identity": "",
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
            lto = config.get("lto", "no")
            # 兼容旧的布尔值
            if isinstance(lto, bool):
                lto = "yes" if lto else "no"
            lines.append(f"lto: {lto}  # yes/no/auto\n")
            lines.append(f"jobs: {config.get('jobs', 0)}  # 0或负数=自动分配\n")
            python_flag = config.get("python_flag", "")
            if python_flag:
                lines.append(f"python_flag: {python_flag}\n")
            lines.append(f"compiler: {config.get('compiler', 'msvc')}\n")
            lines.append(
                f"no_pyi_file: {str(config.get('no_pyi_file', False)).lower()}\n"
            )
            lines.append(
                f"follow_imports: {str(config.get('follow_imports', True)).lower()}\n"
            )
            lines.append(
                f"assume_yes_for_downloads: {str(config.get('assume_yes_for_downloads', False)).lower()}\n"
            )
            # Nuitka 数据导入选项
            if config.get("include_packages"):
                lines.append(f"include_packages: {config.get('include_packages')}\n")
            if config.get("include_modules"):
                lines.append(f"include_modules: {config.get('include_modules')}\n")
            if config.get("nofollow_imports"):
                lines.append(f"nofollow_imports: {config.get('nofollow_imports')}\n")
            if config.get("include_data_files"):
                lines.append(
                    f"include_data_files: {config.get('include_data_files')}\n"
                )
            if config.get("include_data_dirs"):
                lines.append(f"include_data_dirs: {config.get('include_data_dirs')}\n")

        # PyInstaller特有选项
        if config.get("build_tool") == "pyinstaller":
            lines.append(f"clean: {str(config.get('clean', True)).lower()}\n")
            lines.append(f"noconfirm: {str(config.get('noconfirm', False)).lower()}\n")
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
            if config.get("collect_submodules"):
                lines.append(
                    f"collect_submodules: {config.get('collect_submodules')}\n"
                )
            if config.get("collect_data"):
                lines.append(f"collect_data: {config.get('collect_data')}\n")
            if config.get("collect_binaries"):
                lines.append(f"collect_binaries: {config.get('collect_binaries')}\n")
            if config.get("collect_all"):
                lines.append(f"collect_all: {config.get('collect_all')}\n")
            if config.get("add_data"):
                lines.append(f"add_data: {config.get('add_data')}\n")
            if config.get("add_binary"):
                lines.append(f"add_binary: {config.get('add_binary')}\n")
            if config.get("splash_image"):
                lines.append(f"splash_image: {config.get('splash_image')}\n")
            if config.get("runtime_tmpdir"):
                lines.append(f"runtime_tmpdir: {config.get('runtime_tmpdir')}\n")
            if config.get("target_architecture"):
                lines.append(
                    f"target_architecture: {config.get('target_architecture')}\n"
                )
            if config.get("win_version_file"):
                lines.append(f"win_version_file: {config.get('win_version_file')}\n")
            if config.get("win_manifest"):
                lines.append(f"win_manifest: {config.get('win_manifest')}\n")
            if config.get("osx_bundle_identifier"):
                lines.append(
                    f"osx_bundle_identifier: {config.get('osx_bundle_identifier')}\n"
                )
            if config.get("osx_entitlements_file"):
                lines.append(
                    f"osx_entitlements_file: {config.get('osx_entitlements_file')}\n"
                )
            if config.get("codesign_identity"):
                lines.append(f"codesign_identity: {config.get('codesign_identity')}\n")

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
