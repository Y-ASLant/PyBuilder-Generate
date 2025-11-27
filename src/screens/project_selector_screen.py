"""
项目目录选择屏幕
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Tuple
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button, Input, ListView, ListItem, Label
from textual.binding import Binding


class ProjectSelectorScreen(Screen):
    """项目目录选择屏幕"""

    CSS_PATH = Path(__file__).parent.parent / "style" / "project_selector_screen.tcss"

    BINDINGS = [
        Binding("escape", "back", "返回"),
        Binding("enter", "confirm", "确认"),
    ]

    def __init__(self):
        super().__init__()
        self.selected_path: Path = Path.cwd()  # 默认当前目录
        self.current_page = 0  # 当前页面
        self.items_per_page = 12  # 每页显示12条
        self._dir_cache: Dict[Path, List[Path]] = {}  # 目录内容缓存
        self._loading = False  # 加载状态标志

    def compose(self) -> ComposeResult:
        """创建界面组件"""
        with Container(id="selector-container"):
            yield Static("选择项目目录", id="screen-title")
            yield Static("请选择需要打包的 Python 项目目录", id="screen-description")

            # 路径输入框
            with Vertical(id="path-input-container"):
                yield Label("项目路径:", id="path-label")
                yield Input(
                    placeholder="输入项目路径或从下方选择...",
                    value=str(self.selected_path),
                    id="path-input",
                )

            # 目录列表
            with Container(id="tree-container"):
                yield ListView(id="directory-list")

            # 显示选中的路径
            yield Static(f"选中路径: {self.selected_path}", id="selected-path")

            # 按钮
            with Horizontal(id="button-container"):
                yield Button("返回", variant="warning", id="back-btn", flat=True)
                yield Button("确认", variant="success", id="confirm-btn", flat=True)

    def on_mount(self) -> None:
        """挂载时刷新目录列表"""
        self.refresh_directory_list_async()

    async def _scan_directory_async(self, path: Path) -> Tuple[List[Path], str]:
        """异步扫描目录，返回（项目列表, 错误信息）"""
        try:
            # 在线程池中执行文件系统操作
            loop = asyncio.get_event_loop()
            dir_items = await loop.run_in_executor(None, lambda: list(path.iterdir()))

            # 排序：文件夹在前，文件在后
            dir_items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            return dir_items, ""
        except PermissionError:
            return [], f"无权限访问: {path}"
        except Exception as e:
            return [], f"读取目录失败: {e}"

    def refresh_directory_list_async(self) -> None:
        """异步刷新目录列表"""
        if self._loading:
            return  # 防止重复加载

        self._loading = True
        self.run_worker(self._load_directory(), exclusive=True)

    async def _load_directory(self) -> None:
        """加载目录内容（带缓存）"""
        try:
            # 检查缓存
            if self.selected_path in self._dir_cache:
                dir_items = self._dir_cache[self.selected_path]
                error_msg = ""
            else:
                # 异步扫描目录
                dir_items, error_msg = await self._scan_directory_async(
                    self.selected_path
                )

                if error_msg:
                    self.app.notify(error_msg, severity="error")
                    self._loading = False
                    return

                # 缓存结果（最多缓存100个目录）
                if len(self._dir_cache) > 100:
                    # 清理最旧的缓存
                    oldest_key = next(iter(self._dir_cache))
                    del self._dir_cache[oldest_key]

                self._dir_cache[self.selected_path] = dir_items

            # 更新 UI（必须在主线程）
            self._update_list_view(dir_items)

        finally:
            self._loading = False

    def _update_list_view(self, dir_items: List[Path]) -> None:
        """更新列表视图（在主线程调用）"""
        list_view = self.query_one("#directory-list", ListView)
        list_view.clear()

        all_items = []

        # 添加 ".." 返回上一级
        parent = self.selected_path.parent
        if parent != self.selected_path:
            parent_item = ListItem(Label("📁 .."), classes="parent-dir")
            parent_item.is_parent = True
            all_items.append(parent_item)

        # 添加目录项（限制数量）
        max_items = self.items_per_page - len(all_items)
        for item in dir_items[:max_items]:
            if item.is_dir():
                icon = "📁"
                label = Label(f"{icon} {item.name}")
                list_item = ListItem(label, classes="directory")
                list_item.item_path = item
                all_items.append(list_item)
            else:
                icon = "📄"
                label = Label(f"{icon} {item.name}")
                list_item = ListItem(label, classes="file")
                list_item.item_path = item
                all_items.append(list_item)

        # 添加到 ListView
        for item in all_items:
            list_view.append(item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """列表项选择事件"""
        # 检查是否是父目录项
        if hasattr(event.item, "is_parent") and event.item.is_parent:
            # 点击 ".." 返回上一级
            parent_path = self.selected_path.parent
            if parent_path != self.selected_path:
                self.selected_path = parent_path
                self.update_selected_path()
                self.refresh_directory_list_async()
        elif hasattr(event.item, "item_path"):
            item_path = event.item.item_path
            if item_path.is_dir():
                # 点击文件夹，进入该目录
                self.selected_path = item_path
                self.update_selected_path()
                self.refresh_directory_list_async()
            # 文件不做处理

    def on_input_changed(self, event: Input.Changed) -> None:
        """输入框变化事件"""
        if event.input.id == "path-input":
            try:
                path = Path(event.value)
                if path.exists() and path.is_dir():
                    self.selected_path = path
                    self.update_selected_path()
                    self.refresh_directory_list_async()
            except Exception:
                pass  # 忽略无效路径

    def update_selected_path(self) -> None:
        """更新选中路径显示"""
        selected_label = self.query_one("#selected-path", Static)
        selected_label.update(f"选中路径: {self.selected_path}")

        # 同步到输入框
        path_input = self.query_one("#path-input", Input)
        if path_input.value != str(self.selected_path):
            path_input.value = str(self.selected_path)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击事件"""
        button_id = event.button.id

        if button_id == "back-btn":
            self.action_back()
        elif button_id == "confirm-btn":
            self.action_confirm()

    def action_back(self) -> None:
        """返回上一屏"""
        self.app.pop_screen()

    def action_confirm(self) -> None:
        """确认选择"""
        if not self.selected_path.exists():
            self.app.notify("所选路径不存在，请重新选择", severity="error")
            return

        if not self.selected_path.is_dir():
            self.app.notify("请选择一个目录", severity="error")
            return

        # 保存选中的项目路径到 app
        self.app.project_dir = self.selected_path

        # 跳转到模式选择屏幕
        from src.screens.mode_selector_screen import ModeSelectorScreen

        self.app.notify(
            f"已选择项目: {self.selected_path.name}", severity="information"
        )
        self.app.push_screen(ModeSelectorScreen())
