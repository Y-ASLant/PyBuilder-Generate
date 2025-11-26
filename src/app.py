"""
主应用类
"""

from textual.app import App
from textual.binding import Binding
from textual import events

from src.screens.welcome_screen import WelcomeScreen
from src.utils import load_config, save_config


class PyBuildTUI(App):
    """Python 构建脚本生成器 TUI 应用"""

    TITLE = "Python Build Script Generator"
    SUB_TITLE = "跨平台Python编译脚本生成器"

    ENABLE_COMMAND_PALETTE = False

    # Toast 通知样式：定位到右上角
    CSS = """
    ToastRack {
        dock: top;
        width: auto;
        height: auto;
    }
    """

    # 主题映射表：键位 -> 主题名
    THEME_MAP = {
        "f1": "textual-dark",
        "f2": "gruvbox",
        "f3": "dracula",
        "f4": "monokai",
        "f5": "flexoki",
        "f6": "tokyo-night",
        "f7": "catppuccin-latte",
        "f8": "textual-light",
    }

    BINDINGS = [
        Binding("ctrl+c", "quit", "退出", priority=True),
        Binding("ctrl+p", "noop", show=False, priority=True),
    ] + [
        Binding(key, f"set_theme('{theme}')", theme, priority=True)
        for key, theme in THEME_MAP.items()
    ]

    def __init__(self):
        super().__init__()

        # 项目配置
        self.project_dir = None  # 选中的项目目录
        self.build_mode = None  # 构建模式: simple, full, expert

        # 加载配置
        self.config = load_config()
        self.initial_theme = self.config["theme"]

    def on_mount(self) -> None:
        """应用启动时调用"""
        # 设置启动主题
        self.theme = self.initial_theme
        self.push_screen(WelcomeScreen())

    # 主题切换
    def action_set_theme(self, theme: str) -> None:
        """统一主题切换动作"""
        self.theme = theme
        self._save_theme_to_config(theme)
        try:
            self.notify(f"已切换主题: {theme}", severity="information")
        except Exception:
            pass

    def on_key(self, event: events.Key) -> None:
        """全局按键处理：F1..F8 切换主题"""
        theme = self.THEME_MAP.get(event.key)
        if theme:
            self.action_set_theme(theme)
            event.stop()

    def action_noop(self) -> None:
        """空动作：用于屏蔽默认 Ctrl+P 行为"""
        return

    def _save_theme_to_config(self, theme: str) -> None:
        """将主题写入配置文件"""
        self.config["theme"] = theme
        save_config(self.config)
