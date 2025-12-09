# PyBuild-Generate

<div align="center">

```
  _____       ____        _ _     _           
 |  __ \     |  _ \      (_) |   | |          
 | |__) |   _| |_) |_   _ _| | __| | ___ _ __ 
 |  ___/ | | |  _ <| | | | | |/ _` |/ _ \ '__|
 | |   | |_| | |_) | |_| | | | (_| |  __/ |   
 |_|    \__, |____/ \__,_|_|_|\__,_|\___|_|   
         __/ |                                
        |___/                                 
```



**跨平台 Python 编译脚本生成器**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-lightgrey.svg)]()

</div>

## 特性

- 🎨 **现代 TUI 界面** - 基于 Textual 构建，支持 8 种主题切换
- 📦 **双打包工具** - 支持 PyInstaller 和 Nuitka
- ⚙️ **可视化配置** - 图形化配置编译选项，自动生成构建脚本
- 🍃 **跨平台路径** - 智能路径处理，统一输入体验，自动适配不同平台
- ✨ **零外部依赖** - 生成的构建脚本仅使用标准库，无需额外安装依赖
- 🎉 **CI/CD 集成** - GitHub Actions 自动构建
- 💾 **配置持久化** - 自动保存项目配置和用户偏好

## 截图

<div align="center">

### 主界面
![主界面](assets/img/1.png)

### 功能展示
<table>
  <tr>
    <td width="50%">
      <img src="assets/img/2.png" alt="功能展示2" />
    </td>
    <td width="50%">
      <img src="assets/img/3.png" alt="功能展示3" />
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="assets/img/4.png" alt="功能展示4" />
    </td>
    <td width="50%">
      <img src="assets/img/5.png" alt="功能展示5" />
    </td>
  </tr>
</table>

</div>

## 快速开始

### 安装依赖

```bash
# 使用 uv (推荐)
uv sync
```

### 运行

```bash
# 方式1：使用 uv（推荐）
uv run main.py

# 方式2：直接运行
python main.py

# 方式3：模块方式运行
python -m src
```

### 构建可执行文件

```bash
# 使用Nuitka
uv run build_nuitka.py

# 使用Pyinstaller
uv run build_pyinstaller.py
```

构建产物将输出到 `build/` 目录。

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| `F1` | textual-dark 主题 |
| `F2` | gruvbox 主题 |
| `F3` | dracula 主题 |
| `F4` | monokai 主题 |
| `F5` | flexoki 主题 |
| `F6` | tokyo-night 主题 |
| `F7` | catppuccin-latte 主题 |
| `F8` | textual-light 主题 |
| `ESC` | 返回上一步 |
| `Ctrl+C` | 退出程序 |
| `Ctrl+S` | 保存配置 |



## 配置文件

程序会在运行目录下生成 `config.yaml` 配置文件：

```yaml
theme: textual-dark      # 界面默认主题
terminal_min_cols: 112   # 最小终端宽度
terminal_min_rows: 32    # 最小终端高度
```

## CI/CD 自动构建

提交信息包含特定前缀时自动触发构建：

```bash
git commit -m "build_0: 更新"  # 触发 PyInstaller 构建
git commit -m "build_1: 更新"  # 触发 Nuitka 构建
```

构建产物在 Actions → Artifacts 下载，保留 7 天。

## 项目结构

```
PyBuild-Generate/
├── main.py                   # 程序入口
├── build_*.py                # 构建脚本
├── src/
│   ├── app.py                # 主应用
│   ├── screens/              # 8个界面屏幕
│   └── utils/                # 工具模块
├── .github/workflows/        # CI/CD 配置
└── assets/                   # 资源文件
```

## 依赖

### 运行本工具需要

- Python >= 3.12
- textual >= 6.8.0
- pyfiglet >= 1.0.4
- loguru >= 0.7.3
- nuitka >= 2.8.9
- pyinstaller >= 6.17.0

### 打包目标项目支持

生成的构建脚本最低运行的Python版本为3.6，推荐Python3.8+：

> **说明**: 
> - 生成的脚本使用了 f-string 语法，需要 Python 3.6+ 运行
> - **推荐**: 目标项目使用 Python 3.8+ 以获得最佳兼容性和性能

## License

MIT License © [ASLant](https://github.com/Y-ASLant)

## 贡献

欢迎提交 Issue 和 Pull Request！

---

<div align="center">
  <sub>Made with love by ASLant</sub>
</div>
