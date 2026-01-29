"""
配置屏幕基类
提供配置加载、保存、验证的通用逻辑
"""

import asyncio
from pathlib import Path
from typing import Any

from textual.screen import Screen
from textual.binding import Binding

from src.utils import (
    async_load_build_config,
    async_save_build_config,
    validate_build_config,
)


class BaseConfigScreen(Screen):
    """配置屏幕基类

    提供以下通用功能：
    - 项目目录初始化和验证
    - 配置的异步加载和保存
    - 配置验证
    - 返回上一屏、保存配置等通用操作

    子类需要实现：
    - compose(): 创建界面组件
    - _load_config_to_ui(): 将配置加载到UI
    - _save_config_from_ui(): 从UI保存配置到内存

    子类可以重写：
    - _validate_config(): 自定义验证逻辑
    - _on_config_loaded(): 配置加载后的额外处理
    """

    BINDINGS = [
        Binding("escape", "back", "返回"),
        Binding("ctrl+s", "save", "保存"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.config: dict[str, Any] = {}
        self.project_dir: Path | None = None

    async def on_mount(self) -> None:
        """挂载时加载配置"""
        if not self._init_project_dir():
            return

        # 异步加载现有配置或使用默认配置
        self.config = await async_load_build_config(self.project_dir)  # type: ignore[arg-type]
        self._load_config_to_ui()
        self._on_config_loaded()

    def _init_project_dir(self) -> bool:
        """初始化项目目录

        Returns:
            bool: 初始化是否成功
        """
        # 使用 getattr 确保类型安全
        project_dir = getattr(self.app, "project_dir", None)
        if not project_dir:
            self.app.notify("未选择项目目录", severity="error")
            self.app.pop_screen()
            return False
        self.project_dir = project_dir
        return True

    def _load_config_to_ui(self) -> None:
        """将配置加载到UI（子类必须实现）"""
        raise NotImplementedError("子类必须实现 _load_config_to_ui 方法")

    def _save_config_from_ui(self) -> None:
        """从UI保存配置到内存（子类必须实现）"""
        raise NotImplementedError("子类必须实现 _save_config_from_ui 方法")

    def _on_config_loaded(self) -> None:
        """配置加载后的额外处理（子类可重写）"""
        pass

    def _validate_config(self) -> tuple[bool, str]:
        """验证配置

        Returns:
            tuple[bool, str]: (是否有效, 错误信息)
        """
        return validate_build_config(self.config, self.project_dir)  # type: ignore[arg-type]

    def _validate_and_save(self) -> bool:
        """验证并保存配置到内存

        Returns:
            bool: 验证是否成功
        """
        self._save_config_from_ui()

        is_valid, error_msg = self._validate_config()
        if not is_valid:
            self.app.notify(f"配置验证失败: {error_msg}", severity="error")
            return False

        return True

    async def _async_save_config(self) -> bool:
        """异步保存配置到文件

        Returns:
            bool: 保存是否成功
        """
        success = await async_save_build_config(self.project_dir, self.config)  # type: ignore[arg-type]
        if not success:
            self.app.notify("配置保存失败", severity="error")
        return success

    async def _async_save_notify(self) -> None:
        """异步保存并显示通知"""
        success = await self._async_save_config()
        if success:
            self.app.notify("配置已保存", severity="information")

    def action_back(self) -> None:
        """返回上一屏"""
        self.app.pop_screen()

    def action_save(self) -> None:
        """保存配置（同步触发异步保存）"""
        if self._validate_and_save():
            asyncio.create_task(self._async_save_notify())

    async def action_save_async(self) -> None:
        """异步保存配置"""
        if self._validate_and_save():
            success = await self._async_save_config()
            if success:
                self.app.notify("配置已保存", severity="information")
