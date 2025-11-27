# -*- coding: utf-8 -*-
"""
PyBuilder - Nuitka 构建脚本
版本: 1.0.0
"""

import sys
import subprocess
import shutil
import time


# ANSI 颜色代码
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"


# 构建配置
PROJECT_NAME = "PyBuilder"
VERSION = "1.0.0"
ENTRY_FILE = "main.py"
COMPANY_NAME = "ASLant"
ICON_FILE = "assets/app.ico"
OUTPUT_DIR = "build"


def build():
    """执行 Nuitka 构建"""
    # 获取终端宽度
    width = shutil.get_terminal_size().columns
    separator = "-" * width
    start_time = time.time()

    print(f"{Color.CYAN}{Color.BOLD}Building {PROJECT_NAME} v{VERSION}{Color.RESET}")
    print(separator)

    # 构建 Nuitka 命令
    cmd = [
        sys.executable,
        "-m",
        "nuitka",
        "--standalone",
        f"--output-dir={OUTPUT_DIR}",
        "--jobs=16",
        "--quiet",
        "--remove-output",
        f"--windows-icon-from-ico={ICON_FILE}",
        f"--windows-company-name={COMPANY_NAME}",
        f"--windows-product-version={VERSION}",
        f"--windows-file-version={VERSION}",
        ENTRY_FILE,
    ]

    # 执行构建
    print(f"{Color.GRAY}Command:{Color.RESET}")
    print(f"{Color.GRAY}" + " ".join(cmd) + f"{Color.RESET}")
    print(separator)
    print(f"{Color.YELLOW}Building, please wait...{Color.RESET}")
    print()

    try:
        subprocess.run(cmd, check=True)
        print(separator)
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f"{Color.GREEN}{Color.BOLD}Build successful!{Color.RESET}")
        import os

        abs_output = os.path.abspath(OUTPUT_DIR)
        print(f"{Color.GREEN}Output: {abs_output}{Color.RESET}")
        if minutes > 0:
            print(f"{Color.CYAN}Build time: {minutes}m {seconds}s{Color.RESET}")
        else:
            print(f"{Color.CYAN}Build time: {seconds}s{Color.RESET}")
        return 0
    except subprocess.CalledProcessError as e:
        print(separator)
        print(
            f"{Color.RED}{Color.BOLD}Build failed: {Color.RESET}{Color.RED}{e}{Color.RESET}"
        )
        return 1
    except Exception as e:
        print(separator)
        print(
            f"{Color.RED}{Color.BOLD}Error: {Color.RESET}{Color.RED}{e}{Color.RESET}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(build())
