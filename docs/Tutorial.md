# PyBuild-Generate 使用教程

## 快速开始

### 1. 运行程序
```bash
uv run main.py
```

### 2. 选择项目
- 点击"开始使用"
- 输入项目路径（或拖拽文件夹）
- 选择入口文件（如 `main.py`）

### 3. 配置打包选项
- 选择打包工具：PyInstaller 或 Nuitka
- 配置基本选项、高级选项、系统特性

### 4. 生成构建脚本
- 点击"生成脚本"
- 脚本保存在项目根目录：`build_pyinstaller.py` 或 `build_nuitka.py`

### 5. 执行构建
```bash
# 使用生成的脚本
python build_pyinstaller.py

# 或直接使用 uv
uv run build_pyinstaller.py
```

---

## PyInstaller 配置说明

### 基本选项

| 选项 | 说明 | 推荐 |
|------|------|------|
| **单文件模式** | 打包成单个 .exe 文件 | ✅ 推荐 |
| **管理员权限** | 运行时需要管理员权限 | 按需 |
| **内部目录名称** | 单文件模式下的临时目录名 | 默认 `_internal` |
| **启动画面** | 启动时显示的图片 | 可选 |
| **运行时临时目录** | 单文件解压的临时目录 | 可选 |

### 高级选项

| 选项 | 说明 | 示例 |
|------|------|------|
| **隐藏导入** | 手动指定需要打包的模块 | `textual,pyfiglet` |
| **排除模块** | 排除不需要的模块 | `tkinter,matplotlib` |
| **收集子模块** | 收集包的所有子模块 | `textual` |
| **收集数据** | 收集数据文件 | `textual:textual` |
| **收集全部** | 自动收集所有依赖 | 会增大体积 |

### 系统特性（Windows）

| 选项 | 说明 | 文件格式 |
|------|------|----------|
| **版本信息文件** | 程序版本信息 | `.txt` 格式 |
| **清单文件** | Windows 清单 | `.xml` 格式 |

**版本信息文件示例：**
```python
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
  ),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [
        StringStruct('CompanyName', '公司名称'),
        StringStruct('FileDescription', '程序描述'),
        StringStruct('FileVersion', '1.0.0.0'),
        StringStruct('ProductName', '产品名称'),
        StringStruct('ProductVersion', '1.0.0.0'),
      ])
    ]),
  ]
)
```

### 系统特性（macOS）

| 选项 | 说明 |
|------|------|
| **Bundle 标识符** | 应用包标识符，如 `com.company.app` |
| **Entitlements 文件** | 权限配置文件 `.plist` |
| **代码签名身份** | 开发者证书标识 |
| **目标架构** | `x86_64` 或 `arm64` |

---

## 常见问题

### 1. 打包后体积过大？
- ❌ 不要使用"收集全部"
- ✅ 手动指定需要的模块
- ✅ 使用"排除模块"排除不需要的库

### 2. 运行时缺少模块？
- 在"隐藏导入"中添加缺失的模块
- 或使用"收集子模块"收集整个包

### 3. 缺少数据文件？
- 使用"收集数据"添加数据文件
- 格式：`包名:目标路径`

### 4. 打包失败？
- 检查入口文件路径是否正确
- 检查图标文件是否存在
- 查看构建日志中的错误信息

---

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| `F1-F8` | 切换主题 |
| `ESC` | 返回上一步 |
| `Ctrl+C` | 退出程序 |
| `Ctrl+S` | 保存配置 |

---

## 提示

- 💾 配置会自动保存在项目目录的 `build_config.yaml`
- 🎨 支持 8 种主题，按 F1-F8 切换
- 📝 生成的脚本可以直接运行，也可以手动修改
- 🚀 构建产物在 `build/` 目录下
