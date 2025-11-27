"""
应用入口点
"""

import sys
import argparse
from src import __version__, __author__, __repo__
from src.app import PyBuildTUI
from src.utils import resize_terminal, load_config


def show_version():
    """显示版本和作者信息"""
    print(f"PyBuild-Generate v{__version__}")
    print(f"作者: {__author__}")
    print(f"GitHub: {__repo__}")


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="PyBuild-Generate - 跨平台 Python 编译脚本生成器", add_help=True
    )
    parser.add_argument(
        "-V", "--version", action="store_true", help="显示版本和作者信息"
    )

    args = parser.parse_args()

    # 如果指定了 -V 参数，显示版本信息后退出
    if args.version:
        show_version()
        sys.exit(0)

    # 加载配置
    config = load_config()
    cols, rows = config["terminal_min_cols"], config["terminal_min_rows"]

    # 调整终端窗口大小
    resize_terminal(cols=cols, rows=rows)

    # 启动应用（指定终端大小）
    app = PyBuildTUI()
    app.run(size=(cols, rows))


if __name__ == "__main__":
    main()
