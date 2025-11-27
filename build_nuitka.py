# -*- coding: utf-8 -*-
"""
PyBuilder - Nuitka 构建脚本
版本: 1.0.0
"""

import sys
import subprocess
import shutil


# 构建配置
PROJECT_NAME = 'PyBuilder'
VERSION = '1.0.0'
ENTRY_FILE = 'main.py'
COMPANY_NAME = 'ASLant'
ICON_FILE = 'assets/app.ico'
OUTPUT_DIR = 'build'

def build():
    """执行 Nuitka 构建"""
    # 获取终端宽度
    width = shutil.get_terminal_size().columns
    separator = '-' * width

    print(f'开始构建 {PROJECT_NAME} v{VERSION}...')
    print(separator)

    # 构建 Nuitka 命令
    cmd = [
        sys.executable,
        '-m', 'nuitka',
        '--standalone',
        f'--output-dir={OUTPUT_DIR}',
        '--jobs=16',
        '--quiet',
        '--remove-output',
        f'--windows-icon-from-ico={ICON_FILE}',
        f'--windows-company-name={COMPANY_NAME}',
        f'--windows-product-version={VERSION}',
        f'--windows-file-version={VERSION}',
        ENTRY_FILE,
    ]

    # 执行构建
    print('执行命令:')
    print(' '.join(cmd))
    print(separator)
    print('正在执行构建，请稍候...')
    print()

    try:
        subprocess.run(cmd, check=True)
        print(separator)
        print('✓ 构建成功！')
        print(f'输出目录: {OUTPUT_DIR}')
        return 0
    except subprocess.CalledProcessError as e:
        print(separator)
        print(f'✗ 构建失败: {e}')
        return 1
    except Exception as e:
        print(separator)
        print(f'✗ 发生错误: {e}')
        return 1


if __name__ == '__main__':
    sys.exit(build())
