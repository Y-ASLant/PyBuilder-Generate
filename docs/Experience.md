# PyBuild-Generate 项目记录

## 技术栈
- **UI框架**: Textual (Python TUI框架)
- **语言**: Python
- **项目类型**: 交互式终端应用

## Textual CSS 注意事项

### 数值类型限制
- **padding、margin等属性只接受整数值**，不支持小数
  - ❌ 错误: `padding: 0.5 1;`
  - ✅ 正确: `padding: 0 1;` 或 `padding: 1 2;`
- 支持的格式:
  - 1个值: `padding: 1;` (四周相同)
  - 2个值: `padding: 1 2;` (垂直、水平)
  - 4个值: `padding: 1 2 3 4;` (上、右、下、左)

## 项目结构
```
PyBuild-Generate/
├── src/
│   ├── screens/          # 各个界面屏幕
│   │   ├── mode_selector_screen.py    # 模式选择界面
│   │   ├── compile_config_screen.py   # 编译配置界面
│   │   ├── project_selector_screen.py # 项目选择界面
│   │   └── ...
│   ├── utils/            # 工具类
│   └── app.py            # 主应用
├── main.py               # 启动入口
└── docs/                 # 文档
```

## UI调整经验
- 减少间距: 调整 `margin` 和 `padding` 值为0或更小的整数
- 向上移动内容: 减少容器的上padding值
- 紧凑布局: 设置组件的 `margin-top: 0` 和 `margin-bottom: 0`

## PyInstaller Splash 启动画面功能实现经验

### 问题：配置数据丢失
**现象**: 用户输入的 `splash_image` 路径在返回上一页后丢失，每次进入界面都被重置为空。

**根本原因**: 
1. ❌ `DEFAULT_BUILD_CONFIG` 中缺少 `splash_image` 字段定义
2. ❌ `save_build_config()` 函数没有将 `splash_image` 写入 YAML 配置文件
3. ❌ 每次加载配置时，从文件读取不到该字段，导致使用默认空值

**解决方案**:
```python
# 1. 在 DEFAULT_BUILD_CONFIG 中添加字段
DEFAULT_BUILD_CONFIG = {
    # ... 其他配置 ...
    "splash_image": "",  # ✅ 添加默认值
}

# 2. 在 save_build_config() 中添加保存逻辑
if config.get("splash_image"):
    lines.append(f"splash_image: {config.get('splash_image')}\n")
```

### 关键教训
1. **配置持久化三要素**:
   - ✅ 在默认配置字典中定义字段
   - ✅ 在保存函数中写入文件
   - ✅ 在加载函数中读取（通常自动处理）

2. **禁用输入框的保存逻辑**:
   - 参考 `contents_directory` 的实现
   - 当输入框被禁用时，不从 UI 读取值
   - 而是保留配置文件中的原值或设置默认值
   ```python
   if existing_config["onefile"]:
       # 启用时读取 UI 值
       value = self.query_one("#input", Input).value.strip()
       existing_config["field"] = value
   else:
       # 禁用时保留配置文件中的值
       existing_config["field"] = self.config.get("field", "")
   ```

3. **UI 状态与数据分离**:
   - UI 的禁用/启用只控制用户交互
   - 数据的保存/加载独立于 UI 状态
   - 不要在切换开关时清空数据（除非业务需要）

### PyInstaller Splash 图片要求
- **格式**: PNG（推荐，支持透明）
- **最大尺寸**: 760x480 像素
- **常见错误**: 
  - 图片尺寸超限需要安装 Pillow 或手动调整
  - JPG 格式需要 Pillow 转换为 PNG

### 实现文件清单
- `src/screens/package_options_screen.py` - UI 输入框和状态控制
- `src/utils/script_generator.py` - 生成 `--splash` 参数
- `src/utils/build_config.py` - 配置持久化（关键！）
