# PyBuilder-Generate - 正在重构中(20251126)

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

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-lightgrey.svg)]()

</div>

## 特性

- **现代 TUI 界面** - 基于 [Textual](https://github.com/Textualize/textual) 构建的终端用户界面
- **多打包工具支持** - 支持 PyInstaller 和 Nuitka 两种主流打包方案
- **8 种主题切换** - F1-F8 快捷键即时切换界面主题
- **配置持久化** - 自动保存主题和终端大小偏好
- **一键生成** - 智能分析项目依赖，自动生成构建脚本
- **独立可执行** - 支持打包为单文件可执行程序

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
# 使用 uv
uv run main.py
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

## 项目结构

```
PyBuild-Generate/
├── main.py                      # 程序入口
├── build_nuitka.py              # Nuitka 构建脚本
├── build_pyinstaller.py         # PyInstaller 构建脚本
├── config.yaml                  # 用户配置文件
├── build_config.yaml            # 项目构建配置
├── pyproject.toml               # 项目依赖配置
├── src/
│   ├── __main__.py              # 应用入口点
│   ├── app.py                   # 主应用类
│   ├── screens/                 # TUI 界面屏幕
│   │   ├── welcome_screen.py            # 欢迎界面
│   │   ├── project_selector_screen.py   # 项目选择界面
│   │   ├── mode_selector_screen.py      # 模式选择界面
│   │   ├── compile_config_screen.py     # 编译配置界面
│   │   ├── package_options_screen.py    # 打包选项界面
│   │   ├── compiler_selector_screen.py  # 编译器选择界面
│   │   ├── plugin_selector_screen.py    # 插件选择界面
│   │   └── generation_screen.py         # 脚本生成界面
│   └── utils/                   # 工具模块
│       ├── config.py            # 用户配置管理
│       ├── build_config.py      # 构建配置管理
│       ├── script_generator.py  # 脚本生成器
│       └── terminal.py          # 终端工具
├── assets/                      # 资源文件
│   ├── app.ico                  # 应用图标
│   ├── app.png                  # 应用图片
│   └── img/                     # README.md插图
└── docs/                        # 文档
    └── PLAN.md            # 开发计划(旧版)
```

## 依赖

- Python >= 3.12
- textual >= 0.47.0
- rich >= 13.0.0
- pydantic >= 2.0.0
- pyfiglet >= 1.0.4
- nuitka >= 2.8.6
- pyinstaller >= 6.17.0

## License

MIT License © [ASLant](https://github.com/Y-ASLant)

## 贡献

欢迎提交 Issue 和 Pull Request！

---

<div align="center">
  <sub>Made with love by ASLant</sub>
</div>
