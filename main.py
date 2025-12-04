"""PyBuilder-Generate 启动入口"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from src.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
