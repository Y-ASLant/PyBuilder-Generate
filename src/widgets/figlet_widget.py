"""
自定义 Figlet Widget - 兼容 Textual 7.x
"""

from typing import Literal

from pyfiglet import Figlet
from textual.widgets import Static


# 常用字体列表（从小到大）
FontSize = Literal[
    "small",
    "standard",
    "big",
    "banner",
    "block",
    "3-d",
    "3x5",
    "5lineoblique",
    "acrobatic",
    "alligator",
    "alphabet",
    "avatar",
    "basic",
    "bubble",
    "calgphy2",
    "caligraphy",
    "computer",
    "digital",
    "doom",
    "epic",
    "fourtops",
    "gothic",
    "graceful",
    "grafitti",
    "heart",
    "helv",
    "horizontal",
    "italic",
    "larry3d",
    "lean",
    "letter",
    "lockergnome",
    "madrid",
    "marquee",
    "mini",
    "mike",
    "nancyj",
    "pebble",
    "poison",
    "puffy",
    "roman",
    "rounded",
    "rowancap",
    "script",
    "shadow",
    "slant",
    "slide",
    "speed",
    "starwars",
    "stampate",
    "standard",
    "stop",
    "straight",
    "tanja",
    "thick",
    "thin",
    "tinker",
    "tom",
    "trek",
    "tsalagi",
    "twisted",
    "usa",
    "weird",
]

JustifyType = Literal["left", "center", "right"]


class FigletWidget(Static):
    """
    使用 pyfiglet 生成 ASCII 艺术文本的 Widget

    特性：
    - 支持所有 pyfiglet 字体（带���型提示）
    - 动态更新文本和字体
    - 支持对齐方式
    - 兼容 Textual 7.x
    """

    DEFAULT_CSS = """
    FigletWidget {
        content-align: center middle;
        min-height: 3;
        text-style: bold;
    }
    """

    def __init__(
        self,
        text: str,
        *,
        font: str = "standard",
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        self._text = text
        self._font = font
        self._figlet = self._create_figlet(font)
        # 生成初始内容
        ascii_art = self._render_ascii(text)
        super().__init__(
            ascii_art,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    def _create_figlet(self, font: str) -> Figlet:
        """创建 Figlet 实例，处理字体不存在的情况"""
        try:
            return Figlet(font=font)
        except Exception:
            # 字体不存在时回退到 standard
            return Figlet(font="standard")

    def _render_ascii(self, text: str) -> str:
        """渲染 ASCII 艺术文本"""
        try:
            return self._figlet.renderText(text)
        except Exception:
            # 降级方案：直接显示文本
            return f"\n{text}\n"

    @property
    def text(self) -> str:
        """获取当前文本"""
        return self._text

    @property
    def font(self) -> str:
        """获取当前字体"""
        return self._font

    def set_text(self, text: str, font: str | None = None) -> None:
        """
        更新 Widget 内容

        Args:
            text: 新文本
            font: 新字体（不改变则传 None）
        """
        self._text = text
        if font is not None:
            self._font = font
            self._figlet = self._create_figlet(font)

        # 重新渲染并更新显示
        ascii_art = self._render_ascii(self._text)
        super().update(ascii_art)

    def set_font(self, font: str) -> None:
        """设置字体（提供更直观的 API）"""
        self._font = font
        self._figlet = self._create_figlet(font)
        ascii_art = self._render_ascii(self._text)
        super().update(ascii_art)


class AnimatedFiglet(FigletWidget):
    """
    支持颜色的 Figlet Widget

    使用 Textual 的样式标记实现颜色效果
    """

    DEFAULT_CSS = """
    AnimatedFiglet {
        content-align: center middle;
        min-height: 3;
        text-style: bold;
    }
    """

    def __init__(
        self,
        text: str,
        *,
        font: str = "standard",
        color: str = "primary",
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        self._color = color
        super().__init__(text, font=font, name=name, id=id, classes=classes)
        # 重新渲染带颜色的内容
        self._update_color()

    def _update_color(self) -> None:
        """更新带颜色的内容"""
        ascii_art = self._render_ascii(self._text)
        colored_art = f"[{self._color}]{ascii_art}[/{self._color}]"
        super().update(colored_art)

    def set_text(self, text: str, font: str | None = None) -> None:
        """更新内容并重新应用颜色"""
        self._text = text
        if font is not None:
            self._font = font
            self._figlet = self._create_figlet(font)
        self._update_color()

    def set_color(self, color: str) -> None:
        """设置颜色"""
        self._color = color
        self._update_color()
