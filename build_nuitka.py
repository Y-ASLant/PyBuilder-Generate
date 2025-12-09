# -*- coding: utf-8 -*-
"""
PyBuilder - Nuitka 构建脚本
版本: 1.0.0
"""

import sys
import os
import subprocess
import shutil
import time
import platform


# ANSI 颜色代码
class Color:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'


# 构建配置
PROJECT_NAME = 'PyBuilder'
VERSION = '1.0.0'
ENTRY_FILE = 'main.py'
COMPANY_NAME = 'ASLant'
ICON_FILE = 'assets/app.ico'
OUTPUT_DIR = 'build'

def build():
    """执行 Nuitka 构建"""
    # 获取平台信息
    os_type = platform.system()
    is_windows = os_type == 'Windows'
    is_macos = os_type == 'Darwin'
    is_linux = os_type == 'Linux'
    
    # 获取终端宽度
    width = shutil.get_terminal_size().columns
    separator = '-' * width
    start_time = time.time()

    print(f'{Color.CYAN}{Color.BOLD}Building {PROJECT_NAME} v{VERSION} on {os_type}{Color.RESET}')
    print(separator)

    # 构建 Nuitka 命令
    cmd = [
        sys.executable,
        '-m', 'nuitka',
        '--mode=standalone',
        f'--output-dir={OUTPUT_DIR}',
        f'--output-filename={PROJECT_NAME}',
        f'--output-folder-name={PROJECT_NAME}.dist',
        '--lto=auto',
        '--jobs=16',
        '--python-flag=-O',
        '--quiet',
        '--remove-output',
        '--include-package=pygments',
        f'--include-data-dir={os.path.join('src', 'style')}={os.path.join('src', 'style')}',
        f'--include-data-dir={'docs'}={'docs'}',
    ]

    # Windows图标（仅Windows平台）
    if is_windows:
        cmd.append(f'--windows-icon-from-ico={ICON_FILE}')

    # Windows公司名称（仅Windows平台）
    if is_windows:
        cmd.append(f'--windows-company-name={COMPANY_NAME}')

    # Windows版本信息（仅Windows平台）
    if is_windows:
        cmd.append(f'--windows-product-version={VERSION}')
        cmd.append(f'--windows-file-version={VERSION}')

    # 根据平台选择编译器
    compiler = 'msvc'
    if is_windows:
        # Windows平台编译器
        if compiler == 'clang':
            cmd.append('--clang')
        elif compiler == 'mingw64':
            cmd.append('--mingw64')
        elif compiler == 'clang-cl':
            cmd.append('--clang-cl')
        # msvc是默认，不需要参数
    elif is_linux:
        # Linux平台编译器
        if compiler == 'clang':
            cmd.append('--clang')
        # gcc是默认，不需要参数
    elif is_macos:
        # macOS平台编译器
        if compiler != 'clang':
            # clang是macOS默认，其他需要指定
            if compiler == 'gcc':
                print(f'{Color.YELLOW}注意: macOS推荐使用Clang{Color.RESET}')

    # 添加入口文件
    cmd.append(ENTRY_FILE)

    # 执行构建
    print(f'{Color.GRAY}Command:{Color.RESET}')
    print(f'{Color.GRAY}' + ' '.join(cmd) + f'{Color.RESET}')
    print(separator)
    print(f'{Color.YELLOW}Building, please wait...{Color.RESET}')
    print()

    try:
        subprocess.run(cmd, check=True)
        print(separator)
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f'{Color.GREEN}{Color.BOLD}Build successful!{Color.RESET}')
        abs_output = os.path.abspath(OUTPUT_DIR)
        print(f'{Color.GREEN}Output: {abs_output}{Color.RESET}')
        if minutes > 0:
            print(f'{Color.CYAN}Build time: {minutes}m {seconds}s{Color.RESET}')
        else:
            print(f'{Color.CYAN}Build time: {seconds}s{Color.RESET}')
        return 0
    except subprocess.CalledProcessError as e:
        print(separator)
        print(f'{Color.RED}{Color.BOLD}Build failed: {Color.RESET}{Color.RED}{e}{Color.RESET}')
        return 1
    except Exception as e:
        print(separator)
        print(f'{Color.RED}{Color.BOLD}Error: {Color.RESET}{Color.RED}{e}{Color.RESET}')
        return 1


if __name__ == '__main__':
    sys.exit(build())
