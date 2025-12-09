# PyInstaller 参数完整指南

> 基于 PyInstaller 6.0+ 版本
> 标注说明：✅ 已实现 | 部分实现 | ❌ 未实现

---

## 📊 实现概况

- **总参数数量**: ~120
- **已实现**: 28 个 (23%)
- **部分实现**: 2 个 (2%)
- **未实现**: 90 个 (75%)

---

## 🔥 核心必备参数（推荐优先级：⭐⭐⭐⭐⭐）

### 打包模式

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--onefile` / `-F` | 打包为单个可执行文件 | ✅ | `onefile` |
| `--onedir` / `-D` | 打包为目录（默认） | ✅ | `onefile: false` |

### 输出控制

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--name=NAME` / `-n NAME` | 指定程序名称 | ✅ | `project_name` |
| `--distpath=DIR` | 指定输出目录 | ✅ | `output_dir` |
| `--workpath=DIR` | 指定临时工作目录 | | 自动设置（非 onefile） |
| `--specpath=DIR` | 指定 .spec 文件目录 | ❌ | - |
| `--clean` | 清理临时文件 | ✅ | `clean` |
| `--noconfirm` / `-y` | 替换输出目录时不提示 | ✅ | `noconfirm` |

### 调试选项

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--debug=LEVEL` | 调试模式 (all/imports/bootloader/noarchive) | ✅ | `debug` |
| `--log-level=LEVEL` | 日志级别 (TRACE/DEBUG/INFO/WARN/ERROR/CRITICAL) | | `quiet_mode` → WARN |
| `--console` / `-c` | 显示控制台窗口（默认） | ✅ | `show_console: true` |
| `--windowed` / `--noconsole` / `-w` | 隐藏控制台窗口 | ✅ | `show_console: false` |

---

## 📦 捆绑内容控制（推荐优先级：⭐⭐⭐⭐⭐）

### 数据文件

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--add-data=SRC;DEST` | 添加数据文件或目录 | ✅ | `add_data` |
| `--add-binary=SRC;DEST` | 添加二进制文件 | ✅ | `add_binary` |

> Windows 使用分号 `;` 分隔，Linux/macOS 使用冒号 `:`

### 模块收集

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--hidden-import=MODULE` | 添加隐藏导入模块 | ✅ | `hidden_imports` |
| `--collect-submodules=PACKAGE` | 收集包的所有子模块 | ✅ | `collect_submodules` |
| `--collect-data=PACKAGE` | 收集包的数据文件 | ✅ | `collect_data` |
| `--collect-binaries=PACKAGE` | 收集包的二进制文件 | ✅ | `collect_binaries` |
| `--collect-all=PACKAGE` | 收集包的所有内容 | ✅ | `collect_all` |
| `--copy-metadata=PACKAGE` | 复制包的元数据 | ❌ | - |
| `--recursive-copy-metadata=PACKAGE` | 递归复制元数据 | ❌ | - |

### 模块排除

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--exclude-module=MODULE` | 排除模块 | ✅ | `exclude_modules` |

---

## 🎨 应用外观（推荐优先级：⭐⭐⭐⭐）

### 图标和资源

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--icon=FILE.ico` / `-i FILE.ico` | 设置应用图标 | ✅ | `icon_file` |
| `--splash=IMAGE` | 启动画面（仅 onefile） | ✅ | `splash_image` |
| `--version-file=FILE` | Windows 版本信息文件 | ✅ | `win_version_file` |
| `--manifest=FILE` | Windows manifest 文件 | ✅ | `win_manifest` |
| `--resource=RESOURCE` | 添加或更新资源 | ❌ | - |

### 单文件选项

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--runtime-tmpdir=PATH` | 单文件模式运行时临时目录 | ✅ | `runtime_tmpdir` |
| `--contents-directory=DIR` | 内部目录名称 | ✅ | `contents_directory` |

---

## 🪟 Windows 特定选项（推荐优先级：⭐⭐⭐⭐）

### 权限和清单

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--uac-admin` | 请求管理员权限 | ✅ | `uac_admin` |
| `--uac-uiaccess` | UI 访问权限 | ❌ | - |
| `--win-private-assemblies` | 私有程序集 | ❌ | - |
| `--win-no-prefer-redirects` | 不优先重定向 | ❌ | - |

### 嵌入清单

| 参数 | 说明 | 状态 |
|------|------|------|
| `--embed-manifest` | 嵌入 manifest（默认） | ❌ |
| `--no-embed-manifest` | 不嵌入 manifest | ❌ |

---

## 🍎 macOS 特定选项（推荐优先级：⭐⭐⭐⭐）

### App Bundle

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--osx-bundle-identifier=ID` | Bundle 标识符 | ✅ | `osx_bundle_identifier` |
| `--osx-entitlements-file=FILE` | 授权文件 | ✅ | `osx_entitlements_file` |
| `--target-architecture=ARCH` | 目标架构 (x86_64/arm64/universal2) | ✅ | `target_architecture` |

### 代码签名

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--codesign-identity=ID` | 代码签名身份 | ✅ | `codesign_identity` |
| `--codesign-entitlements-file=FILE` | 代码签名授权文件 | ❌ | - |

---

## 🐧 Linux 特定选项（推荐优先级：⭐⭐⭐）

| 参数 | 说明 | 状态 |
|------|------|------|
| `--strip` | 剥离二进制文件（减小体积） | ❌ |

---

## 🛠️ 高级选项（推荐优先级：⭐⭐⭐）

### Hook 系统

| 参数 | 说明 | 状态 |
|------|------|------|
| `--additional-hooks-dir=DIR` | 额外 hook 目录 | ❌ |
| `--runtime-hook=HOOK` | 运行时 hook 脚本 | ❌ |
| `--exclude-hook=HOOK` | 排除 hook | ❌ |

### 路径控制

| 参数 | 说明 | 状态 |
|------|------|------|
| `--paths=DIR` / `-p DIR` | 搜索路径 | ❌ |
| `--hiddenimport=MODULE` | 隐藏导入（同 --hidden-import） | ❌ |

### 运行时选项

| 参数 | 说明 | 状态 |
|------|------|------|
| `--runtime-hook=FILE` | 运行时钩子脚本 | ❌ |
| `--bootloader-ignore-signals` | Bootloader 忽略信号 | ❌ |

---

## 🔒 安全和混淆（推荐优先级：⭐⭐⭐）

### 加密

| 参数 | 说明 | 状态 |
|------|------|------|
| `--key=KEY` | 加密密钥 | ❌ |

> 使用 AES256 加密 Python 字节码

---

## 📊 Python 优化（推荐优先级：⭐⭐）

### 编译选项

| 参数 | 说明 | 状态 |
|------|------|------|
| `--optimize=LEVEL` | Python 优化级别 (0/1/2) | ❌ |
| `--noupx` | 不使用 UPX 压缩 | ❌ |
| `--upx-dir=DIR` | UPX 工具目录 | ❌ |
| `--upx-exclude=FILE` | UPX 排除文件 | ❌ |

---

## 🧪 Spec 文件选项（推荐优先级：⭐⭐）

### Spec 文件

| 参数 | 说明 | 状态 |
|------|------|------|
| `--specpath=DIR` | .spec 文件保存路径 | ❌ |
| `FILE.spec` | 使用现有 .spec 文件构建 | ❌ |

> Spec 文件是 PyInstaller 配置文件，类似于配方

---

## 🔍 分析和诊断（推荐优先级：⭐⭐）

### 导入分析

| 参数 | 说明 | 状态 |
|------|------|------|
| `--ascii` | 不包含 Unicode 编码支持 | ❌ |

---

## 🎛️ 其他选项（推荐优先级：⭐）

### 杂项

| 参数 | 说明 | 状态 |
|------|------|------|
| `--help` / `-h` | 显示帮助 | ❌ |
| `--version` | 显示版本 | ❌ |
| `--argv-emulation` | macOS argv 模拟 | ❌ |
| `--disable-windowed-traceback` | 禁用窗口化回溯 | ❌ |

---

## 📝 项目实现建议

### 高优先级（立即实现）

1. **Hook 系统支持** ⭐⭐⭐⭐
   - `--additional-hooks-dir`
   - `--runtime-hook`
   - `--exclude-hook`

2. **Python 优化** ⭐⭐⭐⭐
   - `--optimize=LEVEL`
   - `--noupx`

3. **元数据支持** ⭐⭐⭐⭐
   - `--copy-metadata`
   - `--recursive-copy-metadata`

4. **Windows 增强** ⭐⭐⭐
   - `--uac-uiaccess`
   - `--win-private-assemblies`

### 中优先级（后续实现）

5. **加密支持** ⭐⭐⭐
   - `--key=KEY` (字节码加密)

6. **UPX 压缩** ⭐⭐⭐
   - `--upx-dir`
   - `--upx-exclude`

7. **Spec 文件** ⭐⭐
   - `--specpath`
   - 支持使用现有 .spec 文件

### 低优先级（可选）

8. **Linux 优化** ⭐⭐
   - `--strip` (二进制剥离)

9. **高级选项** ⭐
   - `--argv-emulation`
   - `--bootloader-ignore-signals`

---

## 🎯 快速参考

### 最常用的 10 个参数

1. `--onefile` ✅
2. `--name=NAME` ✅
3. `--icon=FILE` ✅
4. `--noconsole` ✅
5. `--add-data=SRC;DEST` ✅
6. `--hidden-import=MODULE` ✅
7. `--clean` ✅
8. `--uac-admin` ✅
9. `--exclude-module=MODULE` ✅
10. `--collect-all=PACKAGE` ✅

### 项目当前配置映射

```yaml
# build_config.yaml 示例
project_name: MyApp
version: 1.0.0
company_name: MyCompany
entry_file: main.py
icon_file: icon.ico
build_tool: pyinstaller
output_dir: dist

# PyInstaller 配置
onefile: true                    # --onefile ✅
show_console: false              # --noconsole ✅
clean: true                      # --clean ✅
noconfirm: false                 # --noconfirm ✅
quiet_mode: false                # --log-level=WARN ⚠️
debug: false                     # --debug=all ✅

# 数据和模块
add_data: "data;data config.ini;."           # --add-data ✅
add_binary: "lib/custom.dll;lib"             # --add-binary ✅
hidden_imports: "pkg_resources numpy.core"   # --hidden-import ✅
exclude_modules: "tkinter matplotlib"        # --exclude-module ✅
collect_submodules: "my_package"             # --collect-submodules ✅
collect_data: "my_package"                   # --collect-data ✅
collect_binaries: "my_package"               # --collect-binaries ✅
collect_all: "my_package"                    # --collect-all ✅

# 单文件选项
splash_image: "splash.png"       # --splash ✅ (仅 onefile)
runtime_tmpdir: ".\\temp"        # --runtime-tmpdir ✅ (仅 onefile)
contents_directory: "_internal"  # --contents-directory ✅ (仅 onedir)

# Windows 特定
uac_admin: false                 # --uac-admin ✅
win_version_file: "version.txt"  # --version-file ✅
win_manifest: "manifest.xml"     # --manifest ✅

# macOS 特定
osx_bundle_identifier: "com.myapp"           # --osx-bundle-identifier ✅
osx_entitlements_file: "entitlements.plist"  # --osx-entitlements-file ✅
codesign_identity: "Developer ID"            # --codesign-identity ✅
target_architecture: "universal2"            # --target-architecture ✅
```

---

## 📚 参考资源

- [PyInstaller 官方文档](https://pyinstaller.org/en/stable/)
- [PyInstaller GitHub](https://github.com/pyinstaller/pyinstaller)
- [使用手册](https://pyinstaller.org/en/stable/usage.html)
- [Spec 文件说明](https://pyinstaller.org/en/stable/spec-files.html)
- [Hook 开发](https://pyinstaller.org/en/stable/hooks.html)

---

## 已知问题和注意事项

### 参数兼容性

1. **平台特定参数**
   - Windows: `--uac-*`, `--win-*`, `--version-file`, `--manifest`
   - macOS: `--osx-*`, `--codesign-*`, `--target-architecture`
   - Linux: `--strip`
   - 跨平台时需要条件判断

2. **数据文件路径分隔符**
   - Windows: 使用分号 `;` 作为源和目标分隔符
   - Linux/macOS: 使用冒号 `:` 作为分隔符
   - 项目会自动处理

3. **Onefile vs Onedir**
   - `--splash` 仅在 `--onefile` 模式有效
   - `--runtime-tmpdir` 仅在 `--onefile` 模式有效
   - `--contents-directory` 仅在 `--onedir` 模式有效

### 项目实现状态说明

**已完整实现** (28个)：
- 打包模式：`onefile`
- 输出控制：`name`, `distpath`, `clean`, `noconfirm`
- 调试选项：`debug`, `console/noconsole`
- 数据文件：`add-data`, `add-binary`
- 模块控制：`hidden-import`, `exclude-module`, `collect-*`
- 应用外观：`icon`, `splash`, `version-file`, `manifest`
- 单文件选项：`runtime-tmpdir`, `contents-directory`
- Windows：`uac-admin`
- macOS：`osx-bundle-identifier`, `osx-entitlements-file`, `codesign-identity`, `target-architecture`

**部分实现** (2个)：
- `--log-level`: 仅通过 `quiet_mode` 控制，固定为 WARN
- `--workpath`: 仅在特定情况下自动设置

**高优先级待实现**：
1. Hook 系统（`--additional-hooks-dir`, `--runtime-hook`）
2. Python 优化（`--optimize`, UPX 压缩）
3. 元数据复制（`--copy-metadata`, `--recursive-copy-metadata`）
4. 加密支持（`--key`）

### 性能优化建议

1. **单文件 vs 目录模式**
   ```yaml
   onefile: true   # 单文件，启动慢但分发方便
   onefile: false  # 目录模式，启动快但文件多
   ```

2. **模块排除**
   ```yaml
   exclude_modules: "tkinter matplotlib scipy"  # 减小体积
   ```

3. **UPX 压缩**（未实现）
   - 可大幅减小可执行文件体积
   - 可能增加启动时间
   - 某些杀毒软件可能误报

4. **优化级别**（未实现）
   ```yaml
   optimize: 2  # 最高优化，移除文档字符串和断言
   ```

### 常见错误排查

1. **模块未找到**
   - 使用 `--hidden-import=MODULE` 添加隐藏导入
   - 或使用 `--collect-all=PACKAGE` 收集整个包

2. **数据文件缺失**
   - 使用 `--add-data=SRC;DEST` 添加
   - 或使用 `--collect-data=PACKAGE` 自动收集

3. **DLL 缺失**
   - 使用 `--add-binary=SRC;DEST` 添加
   - 或使用 `--collect-binaries=PACKAGE` 自动收集

4. **打包体积过大**
   - 使用 `--exclude-module` 排除不需要的模块
   - 考虑使用 UPX 压缩（未实现）
   - 检查是否误包含了开发工具

5. **macOS 签名问题**
   - 确保提供正确的 `--codesign-identity`
   - 使用 `--osx-entitlements-file` 指定权限
   - 对于分发，需要公证（Notarization）

6. **Windows Defender 误报**
   - 使用合法的代码签名证书
   - 考虑使用 `--key` 加密（未实现）
   - 向 Microsoft 提交误报

### 与 Nuitka 对比

| 特性 | PyInstaller | Nuitka | 说明 |
|------|-------------|---------|------|
| **打包速度** | 快 ⚡⚡⚡ | 慢 ⚡ | PyInstaller 仅打包，Nuitka 需编译 |
| **运行速度** | 慢 🐌 | 快 🚀 | Nuitka 编译为机器码 |
| **体积** | 大 | 中等 | PyInstaller 包含解释器 |
| **兼容性** | 好 ✅ | 一般 | PyInstaller 更成熟 |
| **调试** | 容易 | 困难 | PyInstaller 保留原始代码 |
| **安全性** | 低（可解包） | 高（编译） | Nuitka 更难逆向 |

**选择建议**：
- 快速原型 → PyInstaller
- 性能要求高 → Nuitka
- 代码保护 → Nuitka
- 兼容性优先 → PyInstaller

---

## 🔄 更新历史

### v1.0 (2025-12-04)
- 初始版本
- 基于 PyInstaller 6.0+
- 覆盖 120 个参数
- 标注项目实现状态 (28 已实现 / 2 部分实现 / 90 未实现)
- 添加性能优化建议和常见错误排查
- 添加与 Nuitka 对比分析

---

**最后更新**: 2025-12-04  
**PyInstaller 版本**: 6.0+  
**文档版本**: 1.0
