# PyInstaller 参数对照表

> 本文档说明 PyBuilder-Generate TUI 界面选项与 PyInstaller 命令行参数的对应关系

---

## 📋 基本选项

| TUI 界面描述 | PyInstaller 参数 | 说明 | 配置键名 |
|------------|-----------------|------|---------|
| 单文件模式 | `--onefile` | 打包为单个可执行文件 | `onefile` |
| 管理员权限 (Windows UAC) | `--uac-admin` | 要求管理员权限运行 | `uac_admin` |
| 内部目录名称 | `--contents-directory=NAME` | 自定义内部文件夹名（默认 `_internal`） | `contents_directory` |
| 启动画面图片 (仅单文件模式) | `--splash=IMAGE` | 添加启动画面（.png 格式） | `splash_image` |
| 运行时临时目录 (仅单文件模式) | `--runtime-tmpdir=PATH` | 指定解压临时目录 | `runtime_tmpdir` |

### 注意事项
- **内部目录名称**：仅在非单文件模式下有效
- **启动画面** 和 **运行时临时目录**：仅在单文件模式下有效

---

## ⚙️ 高级选项

| TUI 界面描述 | PyInstaller 参数 | 说明 | 配置键名 |
|------------|-----------------|------|---------|
| 清理临时文件 | `--clean` | 构建前清理缓存和临时文件 | `clean` |
| 自动确认 (跳过删除提示) | `--noconfirm` | 覆盖输出目录时不询问 | `noconfirm` |
| 静默输出 (仅进度条) | `--log-level=WARN` | 减少输出信息 | `quiet_mode` |
| 调试模式 (输出详细信息) | `--debug=all` | 输出详细的调试信息 | `debug` |

### 控制台窗口
| 配置 | PyInstaller 参数 |
|------|-----------------|
| 显示控制台 | 默认行为 |
| 隐藏控制台 | `--noconsole` |

---

## 📦 数据导入选项

| TUI 界面描述 | PyInstaller 参数 | 示例 | 配置键名 |
|------------|-----------------|------|---------|
| 隐藏导入 | `--hidden-import=MODULE` | `--hidden-import=PIL` | `hidden_imports` |
| 排除模块 | `--exclude-module=MODULE` | `--exclude-module=tkinter` | `exclude_modules` |
| 收集子模块 | `--collect-submodules=PACKAGE` | `--collect-submodules=textual` | `collect_submodules` |
| 收集数据文件 | `--collect-data=PACKAGE` | `--collect-data=textual` | `collect_data` |
| 收集二进制文件 | `--collect-binaries=PACKAGE` | `--collect-binaries=numpy` | `collect_binaries` |
| 收集所有 | `--collect-all=PACKAGE` | `--collect-all=cv2` | `collect_all` |
| 数据文件 | `--add-data=SRC;DEST` | `--add-data=config.yaml;.` | `add_data` |
| 二进制文件 | `--add-binary=SRC;DEST` | `--add-binary=lib.dll;.` | `add_binary` |

### 参数说明

#### 收集选项优先级
```
--collect-all  >  --collect-submodules + --collect-data + --collect-binaries
```

- **收集所有** (`--collect-all`)：包含包的子模块、数据和二进制文件（推荐用于复杂包）
- **收集子模块**：只收集 Python 代码
- **收集数据文件**：只收集数据文件（如配置、模板）
- **收集二进制文件**：只收集 .dll、.so 等二进制文件

#### 输入格式说明

- **模块类选项**（隐藏导入、排除模块等）：支持多种分隔符
  - 空格分隔：`PIL numpy pandas`
  - 逗号分隔：`PIL,numpy,pandas`
  - 中文逗号：`PIL，numpy，pandas`

- **文件类选项**（数据文件、二进制文件）：使用 `;` 分隔源和目标
  - Windows：`src/config.yaml;config.yaml`
  - 多个文件：`config.yaml;. assets/icon.png;assets`

---

## 🖥️ 系统特性选项

### Windows 特性

| TUI 界面描述 | PyInstaller 参数 | 说明 | 配置键名 |
|------------|-----------------|------|---------|
| Windows 版本信息文件 | `--version-file=FILE` | 指定版本信息文件 | `win_version_file` |
| Windows Manifest 文件 | `--manifest=FILE` | 自定义清单文件 | `win_manifest` |
| 图标文件 | `--icon=FILE` | 设置 .exe 图标 | `icon_file` |

### macOS 特性

| TUI 界面描述 | PyInstaller 参数 | 说明 | 配置键名 |
|------------|-----------------|------|---------|
| 目标架构 | `--target-architecture=ARCH` | 指定架构（x86_64/arm64/universal2） | `target_architecture` |
| macOS Bundle 标识符 | `--osx-bundle-identifier=ID` | 设置 Bundle ID | `osx_bundle_identifier` |
| macOS 权限文件 | `--osx-entitlements-file=FILE` | 指定权限配置文件 | `osx_entitlements_file` |
| 代码签名身份 | `--codesign-identity=IDENTITY` | 代码签名证书 | `codesign_identity` |

---

## 🔄 与 Nuitka 的主要区别

| 功能 | PyInstaller | Nuitka |
|------|------------|--------|
| **编译方式** | 打包 Python 解释器 | 编译为 C 代码 |
| **性能** | 接近原生 Python | 显著提升（2-10倍） |
| **体积** | 较大（包含解释器） | 较小 |
| **兼容性** | 更好 | 可能需要额外配置 |
| **编译速度** | 快（几秒到几分钟） | 慢（几分钟到几十分钟） |
| **隐藏导入** | `--hidden-import` | `--include-module` |
| **包含包** | `--collect-submodules` | `--include-package` |
| **数据文件** | `--add-data` | `--include-data-files` |

---

## 📝 完整示例

### 界面配置
```
基本选项：
  ✓ 单文件模式
  □ 管理员权限
  启动画面图片: splash.png

高级选项：
  ✓ 清理临时文件
  ✓ 自动确认
  □ 静默输出

数据导入：
  隐藏导入: PIL numpy
  收集所有: textual
  数据文件: config.yaml;. assets;assets
```

### 生成的命令
```bash
python -m PyInstaller \
    --onefile \
    --distpath=build \
    --name=MyApp \
    --clean \
    --noconfirm \
    --icon=app.ico \
    --splash=splash.png \
    --hidden-import=PIL \
    --hidden-import=numpy \
    --collect-all=textual \
    --add-data=config.yaml;. \
    --add-data=assets;assets \
    main.py
```

### Windows 路径示例
```bash
--add-data=C:\Project\config.yaml;.
--add-binary=C:\libs\mylib.dll;libs
```

### macOS/Linux 路径示例
```bash
--add-data=/home/user/project/config.yaml:.
--add-binary=/usr/lib/mylib.so:libs
```

---

## 🔍 常见问题

### Q: "隐藏导入" 和 "收集子模块" 有什么区别？

- **隐藏导入** (`--hidden-import`)：用于动态导入的模块
  ```python
  # PyInstaller 无法自动检测这种导入
  module_name = "PIL.Image"
  module = __import__(module_name)
  ```

- **收集子模块** (`--collect-submodules`)：收集整个包的所有子模块
  ```python
  # 这种情况用 --collect-submodules=textual
  from textual import app
  from textual.widgets import Button
  ```

### Q: 什么时候使用 "收集所有"？

当遇到以下情况时推荐使用 `--collect-all`：
- 包含大量子模块和数据文件的复杂库（如 `cv2`、`scipy`）
- 出现 "No module named xxx" 错误
- 运行时缺少数据文件

### Q: 单文件模式下为什么不能设置内部目录？

单文件模式 (`--onefile`) 会将所有文件压缩到一个 .exe 中，运行时解压到临时目录，因此不需要自定义内部目录结构。

### Q: 如何处理路径分隔符？

- **Windows**：使用分号 `;`
  ```
  --add-data=src\data.txt;dest
  ```

- **macOS/Linux**：使用冒号 `:`
  ```
  --add-data=src/data.txt:dest
  ```

PyBuilder-Generate 会在生成脚本时自动处理平台差异。

---

## 冲突检测

本项目在配置时会自动检测以下冲突：

### 收集选项冲突
如果在 **收集所有** 中已包含某个包，再在其他收集选项中重复指定会显示警告：

```
以下包在'收集所有'中已包含，无需重复配置:
  收集子模块: textual
  收集数据文件: textual
```

**建议**：使用 `--collect-all` 时，不要再单独配置该包的其他收集选项。

---

## 📚 相关文档

- [PyInstaller 完整参数列表](./PyInstaller-Parameters.md)
- [Nuitka 参数对照表](./参数对照表.md)
- [使用教程](./Tutorial.md)
- [实战经验](./Experience.md)
