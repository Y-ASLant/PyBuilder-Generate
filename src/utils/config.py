"""
配置管理模块
"""

import sys
from pathlib import Path

# 默认配置
DEFAULT_CONFIG = {
    "theme": "textual-dark",
    "terminal_min_cols": 112,
    "terminal_min_rows": 32,
}


def get_config_path() -> Path:
    """获取配置文件路径"""
    is_frozen = getattr(sys, "frozen", False) or "__compiled__" in dir()
    base = (
        Path(sys.executable).parent
        if is_frozen
        else Path(__file__).resolve().parent.parent.parent
    )
    return base / "config.yaml"


def load_config() -> dict:
    """加载配置，不存在则返回默认值"""
    config = DEFAULT_CONFIG.copy()
    path = get_config_path()
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    s = line.strip()
                    if ":" in s and not s.startswith("#"):
                        key, value = s.split(":", 1)
                        key, value = key.strip(), value.strip()
                        if key in config:
                            # 转换类型
                            if isinstance(DEFAULT_CONFIG[key], int):
                                config[key] = int(value)
                            else:
                                config[key] = value
    except Exception:
        pass
    return config


def save_config(config: dict) -> None:
    """保存配置到文件"""
    try:
        lines = [f"{k}: {v}\n" for k, v in config.items()]
        get_config_path().write_text("".join(lines), encoding="utf-8")
    except Exception:
        pass
