"""
应用入口点
"""

from src.app import PyBuildTUI
from src.utils import resize_terminal, load_config


def main():
    """主函数"""
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
