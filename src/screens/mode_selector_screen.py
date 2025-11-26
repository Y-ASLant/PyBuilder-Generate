"""
模式选择屏幕
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, Select
from textual.binding import Binding


class ModeSelectorScreen(Screen):
    """模式选择屏幕"""

    CSS = """
    ModeSelectorScreen {
        align: center middle;
        overflow: hidden;
    }
    
    #mode-container {
        width: 96;
        height: auto;
        max-height: 30;
        padding: 1 2;
    }
    
    #screen-title {
        width: 100%;
        height: 1;
        color: $primary;
        text-align: center;
        text-style: bold;
        margin-bottom: 0;
    }
    
    #screen-description {
        width: 100%;
        height: 1;
        color: $text-muted;
        text-align: center;
        margin-bottom: 0;
    }
    
    #project-info {
        width: 100%;
        height: 1;
        color: $accent;
        text-align: center;
        margin-bottom: 1;
    }
    
    Select {
        width: 100%;
        height: auto;
        margin: 1 0;
    }
    
    #mode-description {
        width: 100%;
        height: auto;
        color: $text;
        margin: 1 0 0 0;
        padding: 1;
    }
    
    #button-container {
        width: 100%;
        height: auto;
        layout: horizontal;
        align: center middle;
        margin-top: 1;
    }
    
    Button {
        margin: 0 2;
        min-width: 16;
        height: 3;
    }
    """

    BINDINGS = [
        Binding("escape", "back", "返回"),
        Binding("enter", "confirm", "确认"),
    ]

    def __init__(self):
        super().__init__()
        self.selected_mode = "simple"  # 默认选择简单模式
        self.mode_descriptions = {
            "simple": "简单模式 - 快速生成基础构建脚本，适合大多数项目\n- 自动检测依赖并生成基本打包配置\n- 最少参数，快速上手",
            "full": "完整模式 - 包含所有配置选项和高级功能，适合复杂项目\n- 细粒度构建参数与优化\n- 多平台打包与插件支持",
            "expert": "专家模式 - 完全自定义所有参数，适合有经验的用户\n- 完全脚本化与钩子扩展\n- 高级缓存与CI集成",
        }

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        with Container(id="mode-container"):
            yield Static("选择构建模式", id="screen-title")
            yield Static("请选择适合您项目的构建模式", id="screen-description")

            # 显示项目信息
            project_name = getattr(self.app, "project_dir", None)
            if project_name:
                yield Static(f"项目: {project_name.name}", id="project-info")

            # 模式选择
            # 下拉选择构建模式
            yield Select(
                options=[
                    ("简单模式", "simple"),
                    ("完整模式", "full"),
                    ("专家模式", "expert"),
                ],
                prompt="选择构建模式",
                allow_blank=False,
                value="simple",
                id="mode-select",
            )

            # 详细说明区域
            yield Static(
                self.mode_descriptions.get(self.selected_mode, ""),
                id="mode-description",
            )

            # 按钮
            with Horizontal(id="button-container"):
                yield Button("返回", variant="warning", id="back-btn", flat=True)
                yield Button("下一步", variant="success", id="next-btn", flat=True)

    def on_select_changed(self, event: Select.Changed) -> None:
        """下拉选择变化事件"""
        # 更新选中的模式值
        mode_value = event.value
        if mode_value in ("simple", "full", "expert"):
            self.selected_mode = mode_value
            # 更新下方说明
            desc = self.mode_descriptions.get(self.selected_mode, "")
            desc_widget = self.query_one("#mode-description", Static)
            desc_widget.update(desc)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击事件"""
        button_id = event.button.id

        if button_id == "back-btn":
            self.action_back()
        elif button_id == "next-btn":
            self.action_confirm()

    def action_back(self) -> None:
        """返回上一屏"""
        self.app.pop_screen()

    def action_confirm(self) -> None:
        """确认选择并进入下一步"""
        # 保存选择的模式到 app
        self.app.build_mode = self.selected_mode

        # 显示提示
        mode_names = {
            "simple": "简单模式",
            "full": "完整模式",
            "expert": "专家模式",
        }
        self.app.notify(
            f"已选择: {mode_names.get(self.selected_mode, '未知模式')}",
            severity="information",
        )

        # TODO: 跳转到下一个配置屏幕
        self.app.notify("基础配置功能开发中...", severity="warning")
