"""
终端相关工具函数
"""

import sys
import subprocess
import shutil


def resize_terminal(cols=92, rows=32):
    """
    调整终端窗口大小

    Args:
        cols: 终端列数（宽度）
        rows: 终端行数（高度）

    Note:
        该函数尝试使用两种方法调整终端大小：
        1. ANSI转义序列（适用于大多数现代终端）
        2. stty命令（适用于Linux/Unix系统）

        如果当前终端大小已经大于等于目标大小，则不做任何调整。
        如果调整失败，不会抛出异常，仅忽略错误。
    """
    try:
        # 获取当前终端大小
        current_size = shutil.get_terminal_size(fallback=(80, 24))
        current_cols = current_size.columns
        current_rows = current_size.lines

        # 如果当前终端已经足够大，不做调整
        if current_cols >= cols and current_rows >= rows:
            return

        # 方法1: 使用ANSI转义序列调整终端大小
        # ESC[8;{rows};{cols}t - 这是一个ANSI控制序列
        sys.stdout.write(f"\033[8;{rows};{cols}t")
        sys.stdout.flush()

        # 方法2: 尝试使用stty命令（某些终端需要）
        if sys.platform == "linux":
            try:
                subprocess.run(
                    ["stty", "rows", str(rows), "cols", str(cols)],
                    check=False,
                    capture_output=True,
                )
            except Exception:
                pass  # 静默失败

    except Exception:
        pass  # 如果失败就忽略，不影响程序运行
