# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

PyBuild-Generate 是一个基于 Textual TUI 框架的跨平台 Python 编译脚本生成器。它通过可视化界面配置 PyInstaller 或 Nuitka 参数，自动生成零外部依赖的构建脚本。

## 运行和构建

### 安装依赖
```bash
uv sync
```

### 运行程序
```bash
# 推荐
uv run main.py

# 或
python -m src
```

### 构建可执行文件
```bash
# Nuitka 构建
uv run build_nuitka.py

# PyInstaller 构建
uv run build_pyinstaller.py
```

构建产物输出到 `build/` 目录。

### CI/CD 触发
提交信息包含特定前缀时自动触发 GitHub Actions 构建：
- `build_0:` 或 `build:` - PyInstaller 构建
- `build_1:` - Nuitka 构建

## 架构设计

### 应用架构
- **入口点**: `main.py` → `src/__main__.py` → `src/app.py`
- **应用类**: `PyBuildTUI` 继承自 `textual.app.App`，管理屏幕导航、主题切换和配置持久化
- **屏幕系统**: 9 个独立屏幕模块（见 `src/screens/`），每个屏幕处理特定功能步骤

### 屏幕流程
1. `WelcomeScreen` - 欢迎/选择功能模式
2. `ProjectSelectorScreen` - 选择项目目录
3. `ModeSelectorScreen` - 选择构建模式（simple/full/expert）
4. `CompilerSelectorScreen` - 选择 PyInstaller 或 Nuitka
5. `CompileConfigScreen` - 配置基本编译参数
6. `PackageOptionsScreen` - 配置数据文件、导入等高级选项
7. `PluginSelectorScreen` - 选择 Nuitka 插件
8. `InstallerConfigScreen` / `InstallerOptionsScreen` - 配置安装包（Inno Setup）
9. `GenerationScreen` - 生成最终脚本

### 核心工具模块

**`src/utils/build_config.py`**
- 定义 `DEFAULT_BUILD_CONFIG` - 所有构建参数的默认值
- `load_build_config(project_dir)` - 从项目的 `build_config.yaml` 加载配置
- `save_build_config(project_dir, config)` - 保存配置到项目目录
- `validate_build_config(config, project_dir)` - 验证配置有效性

**`src/utils/script_generator.py`**
- `generate_nuitka_script(config, project_dir)` - 生成 Nuitka 构建脚本
- `generate_pyinstaller_script(config, project_dir)` - 生成 PyInstaller 构建脚本
- 生成的脚本仅使用 Python 标准库，零外部依赖

**`src/utils/installer_generator.py`**
- `generate_inno_setup_script(config, project_dir)` - 生成 Inno Setup (.iss) 安装包脚本

**`src/utils/config.py`**
- 管理应用级配置 (`config.yaml`)：主题、终端尺寸限制

### 主题系统
应用支持 8 种主题，通过 F1-F8 快捷键切换：
- F1: textual-dark (默认)
- F2: gruvbox
- F3: dracula
- F4: monokai
- F5: flexoki
- F6: tokyo-night
- F7: catppuccin-latte
- F8: textual-light

主题选择会持久化到 `config.yaml`。

### 跨平台路径处理
生成的构建脚本使用 `os.path.join()` 处理路径，确保跨平台兼容性。对于数据文件的源/目标分隔符：
- PyInstaller 使用 `;` (Windows) 或 `:` (Unix)
- Nuitka 使用 `=` 分隔源和目标路径

### Nuitka 模式系统
Nuitka 使用官方推荐的 `--mode` 参数：
- `accelerated` - 加速模式（.pyd）
- `standalone` - 独立目录
- `onefile` - 单文件
- `app` / `app-dist` - macOS 应用
- `module` / `package` - 模块/包

向后兼容：如果不设置 `mode`，自动从 `standalone` + `onefile` 组合推导。

## 项目目录结构

```
PyBuild-Generate/
├── main.py                   # 程序启动入口
├── build_*.py                # 本项目的构建脚本
├── src/
│   ├── __main__.py           # 模块入口
│   ├── app.py                # PyBuildTUI 主应用类
│   ├── screens/              # TUI 屏幕模块（9个）
│   └── utils/                # 工具模块
│       ├── build_config.py   # 构建配置管理
│       ├── script_generator.py  # 构建脚本生成
│       ├── installer_generator.py  # 安装包脚本生成
│       ├── config.py         # 应用配置管理
│       └── terminal.py       # 终端工具
├── assets/                   # 资源文件（字体、图标、文档）
├── .github/workflows/        # CI/CD 配置
└── config.yaml               # 应用配置（运行时生成）
```

## 开发注意事项

### 添加新的构建参数
1. 更新 `DEFAULT_BUILD_CONFIG` in `src/utils/build_config.py`
2. 在 `script_generator.py` 中对应生成函数添加参数处理
3. 在相关屏幕类中添加 UI 控件

### 添加新屏幕
1. 在 `src/screens/` 创建新文件，继承自 `textual.widgets.Screen`
2. 在 `src/screens/__init__.py` 中导出
3. 使用 `self.app.push_screen()` 或 `self.app.pop_screen()` 导航

### 配置文件格式
- `config.yaml` - 应用级配置（键: 值）
- `build_config.yaml` - 项目级配置，支持注释、列表（用 `- ` 前缀）

### Python 版本要求
- 运行本工具: Python >= 3.12
- 生成的脚本: Python >= 3.6（推荐 3.8+），使用 f-string 语法
