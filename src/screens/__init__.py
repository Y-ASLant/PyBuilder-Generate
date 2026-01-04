"""
屏幕模块
"""

from src.screens.welcome_screen import WelcomeScreen
from src.screens.project_selector_screen import ProjectSelectorScreen
from src.screens.mode_selector_screen import ModeSelectorScreen
from src.screens.compile_config_screen import CompileConfigScreen
from src.screens.package_options_screen import PackageOptionsScreen
from src.screens.plugin_selector_screen import PluginSelectorScreen
from src.screens.compiler_selector_screen import CompilerSelectorScreen
from src.screens.installer_config_screen import InstallerConfigScreen
from src.screens.installer_options_screen import InstallerOptionsScreen
from src.screens.installer_generation_screen import InstallerGenerationScreen

__all__ = [
    "WelcomeScreen",
    "ProjectSelectorScreen",
    "ModeSelectorScreen",
    "CompileConfigScreen",
    "PackageOptionsScreen",
    "PluginSelectorScreen",
    "CompilerSelectorScreen",
    "InstallerConfigScreen",
    "InstallerOptionsScreen",
    "InstallerGenerationScreen",
]
