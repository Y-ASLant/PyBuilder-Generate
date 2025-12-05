# Nuitka 编译参数完整列表

> 基于 Nuitka 2.8+ 版本
> 最后更新：2024年12月

---

## 参数状态说明

- ✅ **已添加** - 项目已支持的参数
- 🔧 **可添加** - 官方支持但项目尚未实现的参数
- 📦 **商业版** - 需要 Nuitka Commercial 才能使用

---

## 基础编译模式

### ✅ --standalone
**状态**：已添加  
**说明**：创建独立可执行文件，包含所有依赖  
**使用场景**：发布应用给没有 Python 环境的用户  
**项目实现**：在打包选项中配置

### ✅ --onefile
**状态**：已添加  
**说明**：将所有内容打包到单个可执行文件  
**使用场景**：需要单文件分发的应用  
**项目实现**：在打包选项中配置

### 🔧 --module
**状态**：可添加  
**说明**：编译为 Python 扩展模块（.pyd/.so）  
**使用场景**：加速关键模块，保持 Python 导入方式  
**建议优先级**：中

---

## 输出控制

### ✅ --output-dir=DIR
**状态**：已添加  
**说明**：指定编译输出目录  
**默认值**：当前目录  
**项目实现**：build_config.yaml 中的 output_dir

### 🔧 --output-filename=NAME
**状态**：可添加  
**说明**：自定义输出文件名  
**使用场景**：控制最终可执行文件的名称  
**建议优先级**：高

### ✅ --remove-output
**状态**：已添加  
**说明**：构建成功后删除中间构建文件  
**使用场景**：保持目录整洁  
**项目实现**：在打包选项中配置

---

## 编译器选择

### ✅ --msvc=VERSION
**状态**：已添加  
**说明**：使用 Microsoft Visual C++ 编译器（Windows）  
**可选值**：latest, 14.3, 14.2 等  
**项目实现**：compiler: msvc

### ✅ --mingw64
**状态**：已添加  
**说明**：使用 MinGW64 编译器（Windows）  
**项目实现**：compiler: mingw64

### ✅ --clang
**状态**：已添加  
**说明**：使用 Clang 编译器（跨平台）  
**项目实现**：compiler: clang

### 🔧 --gcc
**状态**：可添加  
**说明**：使用 GCC 编译器（Linux/Unix）  
**建议优先级**：高

---

## 性能优化

### ✅ --lto=yes/no
**状态**：已添加  
**说明**：链接时优化（Link Time Optimization）  
**影响**：显著提升性能但延长编译时间  
**项目实现**：lto 配置项

### ✅ --jobs=N
**状态**：已添加  
**说明**：并行编译任务数  
**默认值**：CPU 核心数  
**项目实现**：jobs 配置项

### 🔧 --lto=auto
**状态**：可添加  
**说明**：自动决定是否启用 LTO  
**建议优先级**：低

### 🔧 --static-libpython=yes/no
**状态**：可添加  
**说明**：静态链接 Python 库  
**使用场景**：创建完全独立的二进制文件  
**建议优先级**：中

---

## Python 优化标志

### ✅ --python-flag=FLAG
**状态**：已添加  
**说明**：传递 Python 解释器标志  
**可选值**：
- `-O`：基础优化
- `no_asserts`：移除断言
- `no_docstrings`：移除文档字符串
- `no_annotations`：移除类型注解

**项目实现**：python_flag 配置项

### 🔧 --python-flag=-OO
**状态**：可添加  
**说明**：激进优化（移除 asserts 和 docstrings）  
**建议优先级**：中

---

## 控制台与窗口

### ✅ --disable-console
**状态**：已添加  
**说明**：禁用控制台窗口（GUI 应用）  
**平台**：Windows  
**项目实现**：通过 show_console 反向控制

### 🔧 --windows-console-mode=MODE
**状态**：可添加  
**说明**：精细控制 Windows 控制台行为  
**可选值**：
- `force`：强制显示（默认）
- `disable`：禁用控制台
- `attach`：附加到现有控制台
- `hide`：创建但隐藏

**建议优先级**：高

---

## 插件系统

### ✅ --enable-plugin=PLUGIN
**状态**：已添加  
**说明**：启用 Nuitka 插件  
**常用插件**：
- `pyside2`, `pyside6`：Qt GUI 框架
- `pyqt5`, `pyqt6`：Qt GUI 框架
- `tk-inter`：Tkinter GUI
- `numpy`：数值计算
- `matplotlib`：数据可视化
- `multiprocessing`：多进程支持

**项目实现**：plugins 列表

### 🔧 --disable-plugin=PLUGIN
**状态**：可添加  
**说明**：禁用特定插件  
**建议优先级**：低

### 🔧 --plugin-list
**状态**：可添加  
**说明**：列出所有可用插件  
**建议优先级**：低（可作为调试工具）

---

## 图标与资源

### ✅ --windows-icon-from-ico=ICON
**状态**：已添加  
**说明**：设置 Windows 图标（支持 .ico, .png）  
**项目实现**：icon_file 配置

### 🔧 --macos-app-icon=ICON
**状态**：可添加  
**说明**：设置 macOS 应用图标（.icns, .png）  
**建议优先级**：高（跨平台支持）

### 🔧 --linux-icon=ICON
**状态**：可添加  
**说明**：设置 Linux 图标  
**建议优先级**：中

### 🔧 --windows-icon-template-exe=EXE
**状态**：可添加  
**说明**：从现有 EXE 提取图标  
**建议优先级**：低

---

## 数据文件

### 🔧 --include-data-files=SRC=DST
**状态**：可添加  
**说明**：包含特定数据文件  
**格式**：`source_path=dest_path`  
**示例**：`--include-data-files=config.json=config.json`  
**建议优先级**：高

### 🔧 --include-data-dir=DIRECTORY
**状态**：可添加  
**说明**：包含整个数据目录  
**示例**：`--include-data-dir=assets/`  
**建议优先级**：高

### 🔧 --include-package-data=PACKAGE
**状态**：可添加  
**说明**：自动包含包的数据文件  
**示例**：`--include-package-data=my_package`  
**建议优先级**：高

### 🔧 --include-onefile-external-data=PATTERN
**状态**：可添加  
**说明**：onefile 模式下提取特定文件到外部  
**使用场景**：配置文件需要用户编辑  
**建议优先级**：中

---

## 模块控制

### 🔧 --include-module=MODULE
**状态**：可添加  
**说明**：强制包含特定模块  
**使用场景**：动态导入的模块  
**建议优先级**：高

### 🔧 --include-package=PACKAGE
**状态**：可添加  
**说明**：包含整个包及其子模块  
**建议优先级**：高

### 🔧 --nofollow-import-to=MODULE
**状态**：可添加  
**说明**：不跟踪特定模块的导入  
**使用场景**：排除可选依赖  
**建议优先级**：中

### ✅ --nofollow-imports
**状态**：部分支持  
**说明**：通过 exclude_packages 实现类似功能  
**项目实现**：exclude_packages 列表

---

## Windows 特定选项

### ✅ --windows-company-name=NAME
**状态**：已添加  
**说明**：设置公司名称（版本信息）  
**项目实现**：company_name 配置

### ✅ --windows-product-version=VERSION
**状态**：已添加  
**说明**：产品版本号  
**项目实现**：自动从 version 生成

### ✅ --windows-file-version=VERSION
**状态**：已添加  
**说明**：文件版本号  
**项目实现**：自动从 version 生成

### 🔧 --windows-product-name=NAME
**状态**：可添加  
**说明**：产品名称  
**建议优先级**：中

### 🔧 --windows-file-description=DESC
**状态**：可添加  
**说明**：文件描述  
**建议优先级**：中

### 🔧 --windows-uac-admin
**状态**：可添加  
**说明**：请求管理员权限  
**使用场景**：需要系统级操作的应用  
**建议优先级**：高

### 🔧 --windows-uac-uiaccess
**状态**：可添加  
**说明**：远程桌面 UAC 支持  
**建议优先级**：低

---

## macOS 特定选项

### 🔧 --macos-create-app-bundle
**状态**：可添加  
**说明**：创建 .app 应用包  
**使用场景**：macOS 原生应用发布  
**建议优先级**：高

### 🔧 --macos-app-name=NAME
**状态**：可添加  
**说明**：应用包名称  
**建议优先级**：高

### 🔧 --macos-app-version=VERSION
**状态**：可添加  
**说明**：应用版本  
**建议优先级**：中

### 🔧 --macos-sign-identity=IDENTITY
**状态**：可添加  
**说明**：代码签名身份  
**使用场景**：App Store 发布或公证  
**建议优先级**：中

### 🔧 --macos-sign-notarization
**状态**：可添加  
**说明**：启用公证  
**建议优先级**：中

### 🔧 --macos-app-protected-resource=DESC
**状态**：可添加  
**说明**：请求系统权限（麦克风、相机等）  
**格式**：`NSMicrophoneUsageDescription:描述文字`  
**建议优先级**：中

---

## 调试与日志

### ✅ --quiet
**状态**：已添加  
**说明**：静默模式，减少输出  
**项目实现**：quiet_mode 配置

### ✅ --show-progress
**状态**：已添加  
**说明**：显示编译进度  
**项目实现**：show_progress 配置

### 🔧 --verbose
**状态**：可添加  
**说明**：详细输出模式  
**建议优先级**：中

### 🔧 --show-scons
**状态**：可添加  
**说明**：显示底层 SCons 构建命令  
**使用场景**：调试编译问题  
**建议优先级**：低

### 🔧 --show-modules
**状态**：可添加  
**说明**：显示包含的所有模块  
**建议优先级**：中

### 🔧 --show-memory
**状态**：可添加  
**说明**：显示内存使用情况  
**建议优先级**：低

### 🔧 --debug
**状态**：可添加  
**说明**：启用调试模式  
**建议优先级**：中

---

## 高级优化

### 🔧 --prefer-source-code
**状态**：可添加  
**说明**：优先使用源代码而非字节码  
**建议优先级**：低

### 🔧 --follow-stdlib
**状态**：可添加  
**说明**：包含使用到的标准库模块  
**默认**：已启用  
**建议优先级**：低

### 🔧 --noinclude-default-mode=MODE
**状态**：可添加  
**说明**：默认不包含模块的策略  
**可选值**：error, warning, nofollow  
**建议优先级**：低

---

## 报告生成

### 🔧 --report=FILE
**状态**：可添加  
**说明**：生成 XML 编译报告  
**使用场景**：分析依赖和模块包含情况  
**建议优先级**：高

### 🔧 --report-diffable
**状态**：可添加  
**说明**：生成可对比的报告格式  
**建议优先级**：低

### 🔧 --report-user-provided=KEY=VALUE
**状态**：可添加  
**说明**：在报告中添加自定义元数据  
**建议优先级**：低

---

## 商业版功能

### 📦 --enable-feature=FEATURE
**状态**：商业版  
**说明**：启用商业版特性  
**常用特性**：
- `anti-bloat`：自动排除未使用代码
- `bytecode-encryption`：加密字节码

### 📦 --deployment
**状态**：商业版  
**说明**：启用所有部署优化  

### 📦 --encryption=METHOD
**状态**：商业版  
**说明**：加密模式  

---

## 实验性功能

### 🔧 --experimental=FEATURE
**状态**：可添加  
**说明**：启用实验性功能  
**警告**：可能不稳定  
**建议优先级**：低

---

## 项目配置文件支持

### 🔧 Nuitka Project Options
**状态**：可添加  
**说明**：在源代码中嵌入编译选项  
**格式**：
```python
# nuitka-project: --onefile
# nuitka-project: --enable-plugin=pyside6
# nuitka-project-if: {OS} == "Windows":
# nuitka-project: --windows-icon-from-ico=icon.ico
```
**建议优先级**：中

---

## 推荐的下一步添加

### 优先级：高
1. ✅ `--output-filename` - 自定义输出名称
2. ✅ `--include-data-files` - 数据文件包含
3. ✅ `--include-data-dir` - 目录包含
4. ✅ `--include-module` - 模块包含
5. ✅ `--windows-console-mode` - 精细控制台控制
6. ✅ `--macos-create-app-bundle` - macOS 应用支持
7. ✅ `--report` - 编译报告生成

### 优先级：中
1. ✅ `--include-package` - 包含完整包
2. ✅ `--static-libpython` - 静态链接
3. ✅ `--windows-product-name` - 产品信息
4. ✅ `--macos-sign-identity` - macOS 签名
5. ✅ `--verbose` - 详细日志

### 优先级：低
1. ✅ `--show-modules` - 模块列表
2. ✅ `--show-scons` - 构建命令
3. ✅ `--plugin-list` - 插件列表

---

## 参考资源

- [Nuitka 官方文档](https://nuitka.net/doc/user-manual.html)
- [Nuitka GitHub](https://github.com/Nuitka/Nuitka)
- [Nuitka 商业版](https://nuitka.net/doc/commercial.html)
