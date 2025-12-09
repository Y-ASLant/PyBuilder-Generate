# PyInstaller 编译参数完整列表

> 基于 PyInstaller 6.17.0 版本
> 最后更新：2024年12月

---

## 参数状态说明

- ✅ **已添加** - 项目已支持的参数
- 🔧 **可添加** - 官方支持但项目尚未实现的参数
- **特定场景** - 仅在特定场景下使用

---

## 基础打包模式

### ✅ --onedir
**状态**：已添加（默认）  
**说明**：创建包含可执行文件和依赖的文件夹  
**使用场景**：标准发布模式  
**项目实现**：onefile: false

### ✅ --onefile
**状态**：已添加  
**说明**：打包为单个可执行文件  
**使用场景**：便携式应用  
**项目实现**：onefile: true

### 🔧 --specpath DIR
**状态**：可添加  
**说明**：指定 .spec 文件存放目录  
**默认值**：当前目录  
**建议优先级**：中

---

## 输出控制

### ✅ --distpath DIR
**状态**：已添加  
**说明**：指定输出目录  
**默认值**：./dist  
**项目实现**：output_dir 配置

### ✅ --workpath DIR
**状态**：已添加  
**说明**：临时工作目录  
**默认值**：./build  
**项目实现**：自动处理（onedir 模式避免冲突）

### ✅ --name NAME
**状态**：已添加  
**说明**：可执行文件名称  
**项目实现**：project_name 配置

### ✅ --contents-directory DIR
**状态**：已添加  
**说明**：onedir 模式下内部目录名称  
**默认值**：.  
**使用场景**：组织输出结构  
**项目实现**：contents_directory 配置

---

## 清理与确认

### ✅ --clean
**状态**：已添加  
**说明**：构建前清理缓存和临时文件  
**项目实现**：clean 配置

### 🔧 --clean-cache
**状态**：可添加  
**说明**：只清理 PyInstaller 缓存  
**建议优先级**：中

### ✅ --noconfirm / -y
**状态**：已添加  
**说明**：自动确认覆盖输出目录  
**项目实现**：noconfirm 配置

---

## 日志控制

### ✅ --log-level LEVEL
**状态**：已添加  
**说明**：设置日志级别  
**可选值**：
- `TRACE`：最详细
- `DEBUG`：调试信息
- `INFO`：标准信息（默认）
- `WARN`：警告
- `DEPRECATION`：弃用警告
- `ERROR`：错误
- `FATAL`：致命错误

**项目实现**：quiet_mode 时设为 WARN

### 🔧 --version
**状态**：可添加  
**说明**：显示 PyInstaller 版本  
**建议优先级**：低

---

## 控制台窗口

### ✅ --console / -c
**状态**：已添加（默认）  
**说明**：显示控制台窗口  
**项目实现**：show_console: true

### ✅ --noconsole / -w
**状态**：已添加  
**说明**：不显示控制台（GUI 应用）  
**项目实现**：show_console: false

### 🔧 --hide-console {hide-early,minimize-early,minimize-late,hide-late}
**状态**：可添加  
**说明**：Windows 控制台窗口精细控制  
**选项说明**：
- `hide-early`：启动时立即隐藏
- `minimize-early`：启动时最小化
- `minimize-late`：程序运行后最小化
- `hide-late`：程序运行后隐藏

**建议优先级**：高

---

## 图标设置

### ✅ --icon ICON
**状态**：已添加  
**说明**：设置应用图标  
**支持格式**：
- Windows：.ico
- macOS：.icns
- 通用：.png（需要 Pillow）

**项目实现**：icon_file 配置

### 🔧 --icon=NONE
**状态**：可添加  
**说明**：不使用任何图标  
**建议优先级**：低

---

## 启动画面

### ✅ --splash IMAGE
**状态**：已添加  
**说明**：添加启动画面（仅 onefile 模式）  
**支持格式**：.png, .jpg  
**项目实现**：splash_image 配置

### 🔧 --splash-args ARGS
**状态**：可添加  
**说明**：传递参数给启动画面  
**建议优先级**：低

---

## 数据文件

### ✅ --add-data SRC:DST
**状态**：已添加  
**说明**：添加数据文件或目录  
**格式**：
- Windows：`source;destination`
- Linux/macOS：`source:destination`

**示例**：
```bash
--add-data "config.json:."
--add-data "assets:assets"
```

**项目实现**：add_data 配置

### ✅ --add-binary SRC:DST
**状态**：已添加  
**说明**：添加二进制文件（DLL、SO 等）  
**格式**：同 --add-data  
**项目实现**：add_binary 配置

---

## 模块控制

### ✅ --hidden-import MODULE
**状态**：已添加  
**说明**：包含隐藏导入的模块  
**使用场景**：动态导入、插件系统  
**项目实现**：hidden_imports 配置（支持多个，用逗号或空格分隔）

### ✅ --exclude-module MODULE
**状态**：已添加  
**说明**：排除特定模块  
**使用场景**：减小体积  
**项目实现**：exclude_modules 配置

### ✅ --collect-submodules PACKAGE
**状态**：已添加  
**说明**：收集包的所有子模块  
**使用场景**：确保包完整性  
**项目实现**：collect_submodules 配置

### ✅ --collect-data PACKAGE
**状态**：已添加  
**说明**：收集包的数据文件  
**项目实现**：collect_data 配置

### ✅ --collect-binaries PACKAGE
**状态**：已添加  
**说明**：收集包的二进制文件  
**项目实现**：collect_binaries 配置

### ✅ --collect-all PACKAGE
**状态**：已添加  
**说明**：收集包的所有内容（子模块+数据+二进制）  
**使用场景**：复杂包的完整打包  
**项目实现**：collect_all 配置

### 🔧 --copy-metadata PACKAGE
**状态**：可添加  
**说明**：复制包的元数据  
**使用场景**：某些包需要读取自身元数据  
**建议优先级**：高

### 🔧 --recursive-copy-metadata PACKAGE
**状态**：可添加  
**说明**：递归复制包及其依赖的元数据  
**建议优先级**：中

---

## 搜索路径

### 🔧 --paths DIR / -p DIR
**状态**：可添加  
**说明**：添加模块搜索路径  
**使用场景**：非标准位置的模块  
**建议优先级**：高

### 🔧 --additional-hooks-dir DIR
**状态**：可添加  
**说明**：自定义 hook 脚本目录  
**使用场景**：处理特殊包的打包问题  
**建议优先级**：中

### 🔧 --runtime-hook FILE
**状态**：可添加  
**说明**：添加运行时 hook 脚本  
**使用场景**：在程序启动前执行初始化代码  
**建议优先级**：中

---

## 调试选项

### ✅ --debug all/imports/bootloader/noarchive
**状态**：已添加  
**说明**：启用调试模式  
**选项说明**：
- `all`：启用所有调试
- `imports`：打印模块导入信息
- `bootloader`：启动器调试信息
- `noarchive`：不使用归档（文件形式存储）

**项目实现**：debug 配置

### 🔧 --python-option OPTION
**状态**：可添加  
**说明**：传递选项给 Python 解释器  
**支持选项**：
- `v`：详细模式（相当于 --debug imports）
- `u`：无缓冲模式
- `W <warning>`：警告控制
- `X <xoption>`：扩展选项
- `hash_seed=<value>`：哈希种子

**建议优先级**：高

---

## 优化选项

### 🔧 --optimize LEVEL
**状态**：可添加  
**说明**：字节码优化级别  
**可选值**：
- `0`：无优化（默认）
- `1`：移除断言、docstrings
- `2`：更激进的优化

**建议优先级**：高

### 🔧 --strip
**状态**：可添加  
**说明**：移除符号表（Linux/macOS）  
**影响**：减小体积，但降低调试能力  
**建议优先级**：中

### 🔧 --noupx
**状态**：可添加  
**说明**：不使用 UPX 压缩  
**默认**：如果检测到 UPX 会自动使用  
**建议优先级**：中

### 🔧 --upx-dir DIR
**状态**：可添加  
**说明**：指定 UPX 工具路径  
**建议优先级**：低

### 🔧 --upx-exclude FILE
**状态**：可添加  
**说明**：排除特定文件不进行 UPX 压缩  
**使用场景**：某些二进制文件压缩后损坏  
**建议优先级**：中

---

## Windows 特定选项

### ✅ --version-file FILE
**状态**：已添加  
**说明**：添加版本信息文件  
**项目实现**：win_version_file 配置

### ✅ --manifest FILE
**状态**：已添加  
**说明**：添加或更新清单文件  
**项目实现**：win_manifest 配置

### 🔧 --embed-manifest
**状态**：可添加  
**说明**：嵌入清单文件（默认行为）  
**建议优先级**：低

### 🔧 --resource FILE
**状态**：可添加  
**说明**：添加或更新 Windows 资源  
**格式**：`FILE[,TYPE[,NAME[,LANGUAGE]]]`  
**使用场景**：嵌入自定义资源  
**建议优先级**：中

### ✅ --uac-admin
**状态**：已添加  
**说明**：请求管理员权限  
**项目实现**：uac_admin 配置

### ✅ --uac-uiaccess
**状态**：已添加  
**说明**：允许远程桌面 UAC 提升  
**项目实现**：可通过 win_manifest 实现

### 🔧 --win-private-assemblies
**状态**：可添加  
**说明**：使用私有程序集  
**建议优先级**：低

### 🔧 --win-no-prefer-redirects
**状态**：可添加  
**说明**：不优先使用重定向程序集  
**建议优先级**：低

---

## macOS 特定选项

### 🔧 --osx-bundle-identifier ID
**状态**：可添加  
**说明**：设置 Bundle Identifier  
**格式**：反向 DNS 格式（com.company.app）  
**使用场景**：App Store 发布  
**项目实现**：osx_bundle_identifier 配置  
**建议优先级**：高

### 🔧 --target-architecture ARCH
**状态**：可添加  
**说明**：目标架构  
**可选值**：
- `x86_64`：Intel
- `arm64`：Apple Silicon
- `universal2`：通用二进制

**建议优先级**：高

### 🔧 --codesign-identity IDENTITY
**状态**：可添加  
**说明**：代码签名身份  
**使用场景**：macOS 公证和发布  
**项目实现**：codesign_identity 配置  
**建议优先级**：高

### 🔧 --osx-entitlements-file FILE
**状态**：可添加  
**说明**：授权文件  
**使用场景**：请求系统权限  
**项目实现**：osx_entitlements_file 配置  
**建议优先级**：中

### 🔧 --osx-deep-codesign
**状态**：可添加  
**说明**：深度代码签名（包括所有依赖）  
**建议优先级**：中

### 🔧 --argv-emulation
**状态**：可添加  
**说明**：启用 argv 模拟（macOS app bundle）  
**使用场景**：处理文件关联打开  
**建议优先级**：中

---

## 运行时选项

### ✅ --runtime-tmpdir PATH
**状态**：已添加  
**说明**：指定运行时临时目录（仅 onefile）  
**使用场景**：自定义解压位置  
**项目实现**：runtime_tmpdir 配置

### 🔧 --bootloader-ignore-signals
**状态**：可添加  
**说明**：启动器忽略信号  
**使用场景**：进程组信号处理  
**建议优先级**：低

### 🔧 --disable-windowed-traceback
**状态**：可添加  
**说明**：禁用无控制台模式的异常回溯  
**建议优先级**：低

---

## Spec 文件相关

### 🔧 --specpath DIR
**状态**：可添加  
**说明**：.spec 文件保存目录  
**建议优先级**：中

### 🔧 --additional-analysis-options OPTIONS
**状态**：可添加  
**说明**：传递额外选项给分析器  
**建议优先级**：低

---

## 实验性功能

### 🔧 --experimental=FEATURE
**状态**：可添加  
**说明**：启用实验性功能  
**警告**：可能不稳定  
**建议优先级**：低

---

## 项目当前支持总结

### 基础打包 ✅
- [x] onefile/onedir 模式
- [x] 输出目录控制
- [x] 清理选项
- [x] 日志级别

### 界面控制 ✅
- [x] 控制台显示/隐藏
- [x] 图标设置
- [x] 启动画面

### 数据与资源 ✅
- [x] 添加数据文件
- [x] 添加二进制文件
- [x] 收集包数据

### 模块管理 ✅
- [x] 隐藏导入
- [x] 排除模块
- [x] 收集子模块/数据/二进制
- [x] 收集所有

### Windows 支持 ✅
- [x] 版本信息
- [x] 清单文件
- [x] UAC 权限

### macOS 支持 ✅
- [x] Bundle Identifier
- [x] 代码签名
- [x] 授权文件

### 调试选项 ✅
- [x] 调试模式

---

## 推荐的下一步添加

### 优先级：高
1. ✅ `--copy-metadata` - 包元数据复制
2. ✅ `--paths` - 自定义搜索路径
3. ✅ `--python-option` - Python 解释器选项
4. ✅ `--optimize` - 字节码优化
5. ✅ `--hide-console` - 精细控制台控制
6. ✅ `--target-architecture` - macOS 架构选择

### 优先级：中
1. ✅ `--strip` - 符号表移除
2. ✅ `--upx-exclude` - UPX 排除
3. ✅ `--runtime-hook` - 运行时钩子
4. ✅ `--additional-hooks-dir` - 自定义 hooks
5. ✅ `--resource` - Windows 资源
6. ✅ `--recursive-copy-metadata` - 递归元数据
7. ✅ `--specpath` - Spec 文件路径

### 优先级：低
1. ✅ `--clean-cache` - 仅清理缓存
2. ✅ `--noupx` - 禁用 UPX
3. ✅ `--upx-dir` - UPX 路径
4. ✅ `--bootloader-ignore-signals` - 信号处理

---

## 与 Nuitka 的对比

| 功能 | PyInstaller | Nuitka |
|------|-------------|--------|
| **打包速度** | 快 | 慢（需要编译） |
| **运行性能** | 原生 Python | 编译后更快 |
| **兼容性** | 更好 | 某些包需要特殊处理 |
| **体积** | 较大 | 可以更小（优化后） |
| **调试** | 容易 | 较难 |
| **插件支持** | 内置多种 hook | 插件系统 |
| **macOS 支持** | 完善 | 完善 |
| **代码保护** | 中等 | 更好（编译为机器码） |

---

## 最佳实践

### 开发阶段
```bash
# 使用 onedir 模式，方便调试
--onedir --console --clean
```

### 发布阶段
```bash
# 使用 onefile 模式，优化体积
--onefile --noconsole --optimize 1 --strip
```

### GUI 应用
```bash
# 添加图标和启动画面
--noconsole --icon=app.ico --splash=splash.png
```

### 数据密集型应用
```bash
# 使用 onedir，外部数据文件
--onedir --add-data "data:data" --add-data "config.json:."
```

---

## 常见问题解决

### 缺少模块
```bash
--hidden-import=missing_module
--collect-all=package_name
```

### 体积过大
```bash
--exclude-module=unused_module
--optimize 2
--strip
```

### DLL/SO 缺失
```bash
--add-binary "path/to/lib.dll:."
--collect-binaries=package
```

### 运行时错误
```bash
--debug=all  # 查看详细信息
--runtime-hook=fix.py  # 添加修复脚本
```

---

## 参考资源

- [PyInstaller 官方文档](https://pyinstaller.org/en/stable/)
- [PyInstaller GitHub](https://github.com/pyinstaller/pyinstaller)
- [使用指南](https://pyinstaller.org/en/stable/usage.html)
- [常见问题](https://pyinstaller.org/en/stable/when-things-go-wrong.html)
