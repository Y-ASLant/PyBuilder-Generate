"""
程序启动入口
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
