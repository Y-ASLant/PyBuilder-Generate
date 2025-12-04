# Nuitka 参数完整指南

> 基于 Nuitka 2.8.9 版本
> 标注说明：✅ 已实现 | ⚠️ 部分实现 | ❌ 未实现

---

## 📊 实现概况

- **总参数数量**: ~180
- **已实现**: 11 个 (6%)
- **部分实现**: 2 个 (1%)
- **未实现**: 167 个 (93%)

> **说明**: 
> - Nuitka 官方推荐使用 `--mode=MODE` 统一指定编译模式
> - 项目当前使用内部配置字段（`standalone`, `onefile`）映射到实际参数
> - 旧的 `--standalone` 和 `--onefile` 参数仍可用（向后兼容，但不显示在帮助中）

---

## 🔥 核心必备参数（推荐优先级：⭐⭐⭐⭐⭐）

### 编译模式

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--mode=MODE` | 编译模式（官方推荐） | ❌ | - |
| `--main=FILE` | 主入口文件 | ⚠️ | `entry_file` (通过位置参数) |
| `--python-debug` | 使用 Python 调试版本 | ❌ | - |
| `--version` | 显示 Nuitka 版本信息 | ❌ | - |

**`--mode` 支持的值**：
- `accelerated` - 加速模式（默认）
- `standalone` - 独立模式
- `onefile` - 单文件模式
- `app` - 应用模式（macOS 创建 .app bundle，其他平台等同 onefile）
- `app-dist` - 应用分发模式（macOS 创建 .app bundle，其他平台等同 standalone）
- `module` - 扩展模块模式
- `package` - 包模式
- `dll` - DLL 模式（开发中）

> **注意**: 项目当前未使用 `--mode` 参数，而是通过内部配置字段转换。建议未来迁移到 `--mode` 参数

### 输出控制

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--output-dir=DIR` | 指定输出目录 | ✅ | `output_dir` |
| `--output-filename=NAME` | 指定输出文件名 | ❌ | - |
| `--output-folder-name=NAME` | 指定分发文件夹名 | ❌ | - |
| `--remove-output` | 移除构建目录 | ✅ | `remove_output` |

### 编译器选择

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--clang` | 使用 Clang 编译器 | ✅ | `compiler: clang` |
| `--mingw64` | 使用 MinGW64 (Windows) | ✅ | `compiler: mingw64` |
| `--msvc=VERSION` | 使用 MSVC (latest, 14.3等) | ⚠️ | `compiler: msvc` (仅支持默认) |

### 优化选项

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--lto=CHOICE` | 链接时优化 (yes/no/auto) | ⚠️ | `lto` (仅 yes/no) |
| `--jobs=N` | 并行编译任务数 | ✅ | `jobs` |
| `--python-flag=FLAG` | Python 优化标志 (-O等) | ✅ | `python_flag` |

---

## 📦 模块与包控制（推荐优先级：⭐⭐⭐⭐）

### 包含控制

| 参数 | 说明 | 状态 |
|------|------|------|
| `--include-package=PACKAGE` | 强制包含包 | ❌ |
| `--include-module=MODULE` | 强制包含模块 | ❌ |
| `--include-plugin-directory=PATH` | 包含插件目录 | ❌ |
| `--include-plugin-files=PATTERN` | 包含插件文件 | ❌ |

### 跟随控制

| 参数 | 说明 | 状态 |
|------|------|------|
| `--follow-imports` | 跟随所有导入 | ❌ |
| `--follow-import-to=MODULE` | 跟随特定导入 | ❌ |
| `--nofollow-import-to=MODULE` | 不跟随特定导入 | ❌ |
| `--nofollow-imports` | 不跟随导入 | ❌ |
| `--follow-stdlib` | 跟随标准库 | ❌ |

### 插件系统

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--enable-plugins=PLUGIN` | 启用插件 | ✅ | `plugins` |
| `--disable-plugins=PLUGIN` | 禁用插件 | ❌ | - |
| `--plugin-list` | 列出所有插件 | ❌ | - |
| `--plugin-no-detection` | 禁用插件自动检测 | ❌ | - |
| `--user-plugin=PATH` | 用户自定义插件 | ❌ | - |

---

## 📁 数据文件管理（推荐优先级：⭐⭐⭐⭐）

### 包数据

| 参数 | 说明 | 状态 |
|------|------|------|
| `--include-package-data=PACKAGE` | 包含包数据文件 | ❌ |
| `--include-data-files=SRC=DST` | 包含指定数据文件 | ❌ |
| `--include-data-dir=SRC=DST` | 包含数据目录 | ❌ |
| `--noinclude-data-files=PATTERN` | 排除数据文件 | ❌ |
| `--include-data-files-external=SRC=DST` | 外部数据文件 | ❌ |
| `--include-raw-dir=DIR` | 包含原始目录 | ❌ |

### DLL 管理

| 参数 | 说明 | 状态 |
|------|------|------|
| `--include-module-dll=MODULE` | 包含模块 DLL | ❌ |
| `--noinclude-module-dll=MODULE` | 排除模块 DLL | ❌ |
| `--list-package-dlls=PACKAGE` | 列出包 DLL | ❌ |
| `--list-package-exe=PACKAGE` | 列出包 EXE | ❌ |

### 扩展模块控制

| 参数 | 说明 | 状态 |
|------|------|------|
| `--recompile-extension-modules=PATTERN` | 重新编译扩展模块 | ❌ |
| `--prefer-source-code` | 优先使用源码 | ❌ |
| `--no-prefer-source-code` | 不优先使用源码 | ❌ |

### 元数据支持

| 参数 | 说明 | 状态 |
|------|------|------|
| `--include-distribution-metadata=DIST` | 包含分发元数据 | ❌ |
| `--list-package-data=PACKAGE` | 列出包数据 | ❌ |

---

## 🎯 Onefile 高级选项（推荐优先级：⭐⭐⭐）

| 参数 | 说明 | 状态 |
|------|------|------|
| `--onefile-tempdir-spec=SPEC` | 临时目录规范 | ❌ |
| `--onefile-cache-mode=MODE` | 缓存模式 | ❌ |
| `--onefile-child-grace-time=MS` | 子进程等待时间 | ❌ |
| `--onefile-no-compression` | 禁用压缩 | ❌ |
| `--onefile-as-archive` | 作为归档 | ❌ |
| `--onefile-no-dll` | 不包含 DLL | ❌ |

---

## 🪟 Windows 特定选项（推荐优先级：⭐⭐⭐⭐）

### 控制台

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--disable-console` | 禁用控制台窗口 | ✅ | `show_console: false` |
| `--enable-console` | 启用控制台窗口 | ✅ | `show_console: true` |
| `--windows-console-mode=MODE` | 控制台模式 (force/disable/attach/hide) | ❌ | - |

### 图标和资源

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--windows-icon-from-ico=PATH` | 从 ICO 文件添加图标 | ✅ | `icon_file` |
| `--windows-icon-from-exe=PATH` | 从 EXE 复制图标 | ❌ | - |
| `--onefile-windows-splash-screen-image=PATH` | 启动画面 | ❌ | - |

### UAC 权限

| 参数 | 说明 | 状态 |
|------|------|------|
| `--windows-uac-admin` | 请求管理员权限 | ❌ |
| `--windows-uac-uiaccess` | UI 访问权限 | ❌ |

### 依赖工具

| 参数 | 说明 | 状态 |
|------|------|------|
| `--windows-dependency-tool=TOOL` | 依赖分析工具选择 | ❌ |
| `--force-dll-dependency-cache-update` | 强制更新 DLL 缓存 (Windows) | ❌ |

### 版本信息

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--company-name=NAME` | 公司名称 | ✅ | `company_name` |
| `--product-name=NAME` | 产品名称 | ❌ | - |
| `--file-version=VERSION` | 文件版本 | ⚠️ | `version` |
| `--product-version=VERSION` | 产品版本 | ⚠️ | `version` |
| `--file-description=DESC` | 文件描述 | ❌ | - |
| `--copyright=TEXT` | 版权信息 | ❌ | - |
| `--trademarks=TEXT` | 商标信息 | ❌ | - |

---

## 🍎 macOS 特定选项（推荐优先级：⭐⭐⭐）

### App Bundle

| 参数 | 说明 | 状态 |
|------|------|------|
| `--macos-create-app-bundle` | 创建 App Bundle | ❌ |
| `--macos-app-name=NAME` | App 名称 | ❌ |
| `--macos-app-icon=PATH` | App 图标 | ❌ |
| `--macos-app-version=VERSION` | App 版本 | ❌ |
| `--macos-app-mode=MODE` | App 模式 (gui/background/ui-element) | ❌ |

### 代码签名

| 参数 | 说明 | 状态 |
|------|------|------|
| `--macos-sign-identity=IDENTITY` | 签名身份 | ❌ |
| `--macos-signed-app-name=NAME` | 签名应用名 | ❌ |
| `--macos-sign-notarization` | 公证签名 | ❌ |
| `--macos-sign-keyring-filename=PATH` | 证书文件 | ❌ |
| `--macos-sign-keyring-password=PWD` | 证书密码 | ❌ |

### 架构和权限

| 参数 | 说明 | 状态 |
|------|------|------|
| `--macos-target-arch=ARCH` | 目标架构 (universal/arm64/x86_64) | ❌ |
| `--macos-app-protected-resource=DESC` | 受保护资源 | ❌ |
| `--macos-prohibit-multiple-instances` | 禁止多实例 | ❌ |

---

## 🐧 Linux 特定选项（推荐优先级：⭐⭐⭐）

| 参数 | 说明 | 状态 |
|------|------|------|
| `--linux-icon=PATH` | Linux 图标 | ❌ |

---

## 🐛 调试功能（推荐优先级：⭐⭐⭐）

### 基本调试

| 参数 | 说明 | 状态 |
|------|------|------|
| `--debug` | 启用调试模式 | ❌ |
| `--unstripped` | 保留调试信息 | ❌ |
| `--trace-execution` | 追踪执行 | ❌ |
| `--profile` | 性能分析 | ❌ |

### 输出控制

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--quiet` | 静默模式 | ✅ | `quiet_mode` |
| `--show-progress` | 显示进度 | ✅ | `show_progress` |
| `--show-scons` | 显示 Scons 输出 | ❌ | - |
| `--verbose` | 详细输出 | ❌ | - |
| `--show-modules` | 显示模块信息 | ❌ | - |
| `--show-memory` | 显示内存使用 | ❌ | - |

### 高级调试

| 参数 | 说明 | 状态 |
|------|------|------|
| `--xml=FILE` | XML 输出 | ❌ |
| `--explain-imports` | 解释导入 | ❌ |
| `--experimental=FLAG` | 实验性特性 | ❌ |

---

## 📊 报告和追踪（推荐优先级：⭐⭐⭐）

| 参数 | 说明 | 状态 |
|------|------|------|
| `--report=FILE` | 生成编译报告 | ❌ |
| `--report-diffable` | 可比较的报告 | ❌ |
| `--report-user-provided=KEY=VALUE` | 用户提供的报告数据 | ❌ |
| `--report-template=TEMPLATE:OUTPUT` | 报告模板 | ❌ |
| `--progress-bar=MODE` | 进度条模式 (auto/tqdm/rich/none) | ❌ |

---

## 🚀 性能优化（推荐优先级：⭐⭐⭐）

### C 编译优化

| 参数 | 说明 | 状态 |
|------|------|------|
| `--lto=CHOICE` | 链接时优化 | ⚠️ |
| `--static-libpython=CHOICE` | 静态链接 Python | ❌ |
| `--cf-protection=MODE` | 控制流保护 (GCC) | ❌ |

### PGO 优化

| 参数 | 说明 | 状态 |
|------|------|------|
| `--pgo-c` | C 级别 PGO | ❌ |
| `--pgo-python` | Python 级别 PGO | ❌ |
| `--pgo-args=ARGS` | PGO 参数 | ❌ |
| `--pgo-executable=PATH` | PGO 可执行文件 | ❌ |

---

## 💾 缓存控制（推荐优先级：⭐⭐）

| 参数 | 说明 | 状态 |
|------|------|------|
| `--disable-cache=CACHE` | 禁用缓存 (all/ccache/bytecode/compression/dll-dependencies) | ❌ |
| `--clean-cache=CACHE` | 清理缓存 | ❌ |

---

## ⚙️ 编译行为控制（推荐优先级：⭐⭐）

### 配置文件

| 参数 | 说明 | 状态 |
|------|------|------|
| `--user-package-configuration-file=FILE` | 用户包配置文件 | ❌ |
| `--full-compat` | 完全兼容 CPython | ❌ |

### 文件引用

| 参数 | 说明 | 状态 |
|------|------|------|
| `--file-reference-choice=MODE` | `__file__` 引用 (original/runtime/frozen) | ❌ |
| `--module-name-choice=MODE` | `__name__` 选择 (original/runtime) | ❌ |

### 其他

| 参数 | 说明 | 状态 | 项目配置 |
|------|------|------|----------|
| `--no-pyi-file` | 不生成 .pyi 文件 | ✅ | `no_pyi_file` |
| `--no-pyi-stubs` | 不使用 stubgen | ❌ | - |

---

## ⚠️ 警告控制（推荐优先级：⭐⭐）

| 参数 | 说明 | 状态 |
|------|------|------|
| `--warn-implicit-exceptions` | 隐式异常警告 | ❌ |
| `--warn-unusual-code` | 异常代码警告 | ❌ |
| `--assume-yes-for-downloads` | 自动确认下载 | ❌ |
| `--nowarn-mnemonic=MNEMONIC` | 禁用特定警告 | ❌ |

---

## 🔧 部署和环境（推荐优先级：⭐⭐）

### 部署模式

| 参数 | 说明 | 状态 |
|------|------|------|
| `--deployment` | 部署模式 | ❌ |
| `--no-deployment-flag=FLAG` | 禁用部署标志 | ❌ |

### 环境控制

| 参数 | 说明 | 状态 |
|------|------|------|
| `--force-runtime-environment-variable=SPEC` | 强制环境变量 | ❌ |
| `--force-stdout-spec=SPEC` | 强制标准输出 | ❌ |
| `--force-stderr-spec=SPEC` | 强制标准错误 | ❌ |

---

## 🎮 立即执行（推荐优先级：⭐）

| 参数 | 说明 | 状态 |
|------|------|------|
| `--run` | 编译后立即运行 | ❌ |
| `--debugger` | 在调试器中运行 | ❌ |
| `--debugger-choice=DEBUGGER` | 选择调试器 | ❌ |

---

## 🌍 交叉编译（推荐优先级：⭐⭐）

| 参数 | 说明 | 状态 |
|------|------|------|
| `--target=TARGET_DESC` | 交叉编译目标 (实验性) | ❌ |

> 注意：交叉编译功能高度实验性，目前主要支持 WASI 目标

---

## 🔬 开发者选项（推荐优先级：⭐）

| 参数 | 说明 | 状态 |
|------|------|------|
| `--low-memory` | 低内存模式 | ❌ |
| `--generate-c-only` | 仅生成 C 代码 | ❌ |
| `--show-source-changes=PATTERN` | 显示源码变更 | ❌ |
| `--module-parameter=SPEC` | 模块参数 | ❌ |
| `--python-for-scons=PATH` | 指定 Scons 使用的 Python | ❌ |
| `--create-environment-from-report=PATH` | 从报告创建环境 | ❌ |
| `--must-not-re-execute` | 禁止重新执行 (测试用) | ❌ |
| `--edit-module-code=MODULE` | 编辑模块代码 (开发用) | ❌ |

### GitHub Actions 集成

| 参数 | 说明 | 状态 |
|------|------|------|
| `--github-workflow-options` | 从 GitHub Actions 环境读取选项 | ❌ |

### Nuitka 内部开发选项

| 参数 | 说明 | 状态 |
|------|------|------|
| `--devel-missing-code-helpers` | 报告缺失代码助手 | ❌ |
| `--devel-missing-trust` | 报告缺失信任导入 | ❌ |
| `--devel-recompile-c-only` | 仅重编译 C | ❌ |
| `--devel-internal-graph` | 创建优化图 | ❌ |
| `--devel-generate-mingw64-header` | 生成 MinGW64 头文件 | ❌ |

---

## 📝 项目实现建议

### 高优先级（立即实现）

1. **数据文件管理** ⭐⭐⭐⭐
   - `--include-data-files`
   - `--include-data-dir`
   - `--noinclude-data-files`

2. **模块控制** ⭐⭐⭐⭐
   - `--include-package`
   - `--include-module`
   - `--follow-import-to`
   - `--nofollow-import-to`

3. **Windows 增强** ⭐⭐⭐⭐
   - `--windows-uac-admin`
   - `--windows-console-mode`
   - `--product-name`
   - `--file-description`

### 中优先级（后续实现）

4. **调试和报告** ⭐⭐⭐
   - `--debug`
   - `--report`
   - `--verbose`
   - `--show-modules`

5. **macOS 支持** ⭐⭐⭐
   - `--macos-create-app-bundle`
   - `--macos-app-icon`
   - `--macos-sign-identity`

6. **Onefile 高级** ⭐⭐⭐
   - `--onefile-tempdir-spec`
   - `--onefile-no-compression`

### 低优先级（可选）

7. **性能优化** ⭐⭐
   - `--pgo-c`
   - `--static-libpython`

8. **缓存控制** ⭐⭐
   - `--disable-cache`
   - `--clean-cache`

---

## 🎯 快速参考

### 最常用的 10 个参数

1. `--mode=standalone` ✅ 支持（项目未使用）
2. `--output-dir=DIR` ✅
3. `--windows-icon-from-ico=PATH` ✅
4. `--disable-console` ✅
5. `--enable-plugins=PLUGIN` ✅
6. `--jobs=N` ✅
7. `--lto=yes` ⚠️
8. `--include-data-files=SRC=DST` ❌
9. `--windows-uac-admin` ❌
10. `--company-name=NAME` ✅

### 项目当前配置映射

```yaml
# build_config.yaml 示例
project_name: MyApp
version: 1.0.0
company_name: MyCompany
entry_file: main.py
icon_file: icon.ico
build_tool: nuitka
output_dir: dist

# Nuitka 配置（内部使用简化字段，生成脚本时转换）
standalone: true          # 内部配置，建议迁移到 --mode=standalone
onefile: true            # 内部配置，建议迁移到 --mode=onefile
show_console: false      # --disable-console ✅
remove_output: true      # --remove-output ✅
show_progress: true      # --show-progress ✅
lto: false              # --lto=no ⚠️
jobs: 0                 # --jobs=N (0=自动) ✅
python_flag: ""         # --python-flag ✅
compiler: msvc          # --msvc ✅
no_pyi_file: false      # --no-pyi-file ✅
plugins: "numpy,torch"  # --enable-plugins ✅
quiet_mode: false       # --quiet ✅
```

> **重要**: 
> - 项目配置使用简化字段（`standalone`, `onefile`）保持易用性
> - Nuitka 官方推荐使用 `--mode=MODE` 参数
> - 建议未来版本直接支持 `mode` 配置字段

---

## 📚 参考资源

- [Nuitka 官方文档](https://nuitka.net/doc/user-manual.html)
- [Nuitka GitHub](https://github.com/Nuitka/Nuitka)
- [插件列表](https://nuitka.net/doc/plugins.html)

---

## ⚠️ 已知问题和注意事项

### 参数兼容性

1. **平台特定参数**
   - Windows: `--mingw64`, `--msvc`, `--clang-cl`, `--windows-*`
   - macOS: `--macos-*`, `--osx-*`
   - Linux: `--linux-*`
   - 跨平台时需要条件判断

3. **插件命名变化**
   - 某些插件名称可能在不同版本有变化
   - 建议使用 `--plugin-list` 查看当前可用插件

### 项目实现状态说明

**已完整实现** (11个)：
- 输出控制：`output_dir`, `remove_output`
- 编译器选择：`clang`, `mingw64`, `msvc`
- 性能选项：`jobs`, `python_flag`
- Windows 特定：`disable-console`, `windows-icon-from-ico`, `company-name`
- 插件系统：`enable-plugins`
- 输出控制：`quiet`, `show-progress`, `no-pyi-file`

**部分实现** (2个)：
- `--lto`: 仅支持 yes/no，不支持 auto
- 版本信息：使用同一个 `version` 字段

**注意**：
- 项目使用简化配置字段（`standalone`, `onefile`）
- Nuitka 官方现已推荐使用 `--mode=MODE` 参数（支持 8 种模式）
- 旧的 `--standalone`, `--onefile` 参数仍可用但已隐藏（SUPPRESS_HELP）

**高优先级待实现**：
1. 数据文件管理（`--include-data-files`, `--include-data-dir`）
2. 模块控制（`--include-package`, `--follow-import-to`）
3. Windows UAC（`--windows-uac-admin`）
4. 调试报告（`--report`, `--verbose`）

### 性能优化建议

1. **编译线程数**
   ```yaml
   jobs: 0  # 自动检测 CPU 核心数（推荐）
   jobs: 8  # 手动指定 8 线程
   ```

2. **LTO 优化**
   ```yaml
   lto: true  # 启用链接时优化，编译慢但性能好
   ```

3. **Python 优化**
   ```yaml
   python_flag: "-O"  # 移除断言和 __debug__
   ```

4. **静默模式**
   ```yaml
   quiet_mode: true      # 减少输出
   show_progress: false  # 禁用进度显示
   ```

### 常见错误排查

1. **编译器未找到**
   - Windows: 确保安装 Visual Studio 或 MinGW64
   - macOS: 安装 Xcode Command Line Tools
   - Linux: 安装 gcc 或 clang

2. **插件加载失败**
   - 检查插件名称是否正确（大小写敏感）
   - 确保相关库已安装
   - 使用 `--plugin-list` 查看可用插件

3. **DLL 缺失**
   - 使用 `--include-module-dll` 手动包含
   - 检查依赖分析工具是否正常工作

4. **编译内存不足**
   - 使用 `--low-memory` 选项
   - 减少 `--jobs` 数量
   - 分批编译大型项目

---

## 🔄 更新历史

### v1.1 (2025-12-04)
- 移除所有已弃用参数
- 只保留 Nuitka 最新推荐参数
- 更新参数总数为 ~180
- 调整实现状态统计 (11 已实现 / 2 部分实现 / 167 未实现)

### v1.0 (2025-12-04)
- 初始版本
- 基于 Nuitka 2.8.9
- 覆盖 185 个参数（包含已弃用）
- 添加性能优化建议和常见错误排查

---

**最后更新**: 2025-12-04  
**Nuitka 版本**: 2.8.9  
**文档版本**: 1.1

