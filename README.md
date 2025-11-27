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
uv run build.py
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
| `Ctrl+C` | 退出程序 |

## 配置文件

程序会在运行目录下生成 `config.yaml` 配置文件：

```yaml
theme: textual-dark      # 界面主题
terminal_min_cols: 112   # 最小终端宽度
terminal_min_rows: 32    # 最小终端高度
```

## 项目结构

```
PyBuilder-Generate/
├── main.py              # 程序入口
├── build.py             # Nuitka 构建脚本
├── config.yaml          # 用户配置文件
├── build_config.yaml    # 构建配置模板
├── src/
│   ├── __main__.py      # 应用入口点
│   ├── app.py           # 主应用类
│   ├── screens/         # TUI 屏幕
│   │   ├── welcome_screen.py
│   │   ├── project_selector_screen.py
│   │   └── mode_selector_screen.py
│   └── utils/           # 工具模块
│       ├── config.py    # 配置管理
│       └── terminal.py  # 终端工具
└── assets/
    └── app.ico          # 应用图标
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
