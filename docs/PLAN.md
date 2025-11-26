# 跨平台 Python 编译脚本生成器 TUI 版本 - 开发计划

## 项目概述

### 项目名称
**PythonBuildScriptGenerator-TUI** - 基于 Textual 框架的跨平台 Python 编译脚本生成器

### 项目目标
开发一个现代化、用户友好的 TUI (Text User Interface) 应用程序，用于交互式生成 Nuitka 和 PyInstaller 的构建脚本，支持 Windows/Linux/macOS 全平台。

### 核心价值
- **现代化 UI** - 美观的终端界面，媲美 GUI 应用体验
- **高效交互** - 键盘导航、实时验证、智能提示
- **配置持久化** - 仅生成两个文件：`build_config.yaml` 和 `build.py`
- **零侵入设计** - 不修改项目源码，配置文件可加入版本控制
- **快速复用** - 保存配置后可随时修改重新生成
- **跨平台** - 一套代码，多平台运行

---

## 界面设计原则

### 布局优化
1. **避免拥挤** - 合理使用 padding 和 margin，确保元素间有足够呼吸空间
2. **视觉层次** - 通过间距、颜色、字体大小建立清晰的信息层级
3. **对齐一致** - 保持元素对齐方式统一，增强专业感
4. **留白艺术** - 适当留白让界面更舒适，避免视觉疲劳

### 间距规范
- 容器内边距 (padding): 3-6 个单位
- 组件外边距 (margin): 1-3 个单位
- 标题与内容间距: 2-3 个单位
- 按钮间距: 横向 2 个单位，纵向 1 个单位
- 内容区域底部留白: 3 个单位

### 欢迎界面优化实践
已完成的改进：
- 容器宽度从 90 增加到 100，更好利用空间
- 内边距从 2x4 增加到 3x6，减少拥挤感
- 标题上边距增加到 2，与 logo 拉开距离
- 副标题底边距增加到 3，与描述文字分离
- 按钮宽度增加到 22，高度固定为 3
- 按钮行间距增加到 1，避免紧贴
- 按钮左右间距增加到 2，更加舒展
- 移除所有 emoji，保持界面简洁专业
- 去除 Header 和 Footer，聚焦核心内容

---

## 核心功能

### 1. 运行模式选择
- **完整模式** - 编译 + Linux 包生成
- **编译模式** - 仅生成编译脚本
- **打包模式** - 仅生成 Linux 包脚本

### 2. 构建工具支持
- **Nuitka** - 性能优先，编译为机器码
- **PyInstaller** - 兼容性优先，快速打包

### 3. 编译器支持
- MinGW64 (Windows)
- MSVC (Windows)
- Clang (跨平台)
- GCC (Linux/macOS)

### 4. 插件系统
- GUI 框架：PyQt5/6, PySide2/6, Tkinter
- 科学计算：NumPy, SciPy, Pandas, Matplotlib
- 其他库：Pillow, Requests, SQLAlchemy 等

### 5. Linux 包生成
- DEB 包（Debian/Ubuntu）
- RPM 包（RedHat/CentOS/Fedora）
- 支持 NFPM 和 FPM 工具

### 6. 高级特性
- **仅生成 2 个文件** - `build_config.yaml` + `build.py`，零侵入设计
- **配置自动检测** - 再次打开项目自动加载配置
- **配置保存/加载**（支持 YAML、TOML 格式）
- **从 YAML 配置文件生成 build.py 脚本**
- **配置模板管理** - GUI、科学计算、Web 服务等预设模板
- **实时配置验证** - Pydantic 数据模型验证
- **元数据追踪** - 自动记录创建/更新时间
- **智能错误提示** - 友好的错误信息和日志
- **主题切换**（亮色/暗色）
- **多语言支持**（中文/英文）

---

## 🏗️ 技术架构

### 技术栈

#### 核心框架
```toml
[project]
name = "pybuild-tui"
version = "1.0.0"
requires-python = ">=3.10"

dependencies = [
    "textual>=0.47.0",           # TUI 框架
    "textual-dev>=1.2.0",        # 开发工具
    "rich>=13.0.0",              # 富文本渲染
    "pydantic>=2.0.0",           # 数据验证
    "toml>=0.10.2",              # TOML 配置
    "pyyaml>=6.0",               # YAML 配置支持
    "jinja2>=3.1.0",             # 模板引擎
    "loguru>=0.7.3",             # 日志
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
```

#### 文件结构
```
PythonBuildScriptGenerateToolsTUI/
├── src/                    # 主应用包
│   ├── __init__.py
│   ├── __main__.py                 # 入口点
│   ├── app.py                      # 主应用类
│   │
│   ├── screens/                    # 屏幕模块
│   │   ├── __init__.py
│   │   ├── welcome_screen.py       # 欢迎屏幕
│   │   ├── mode_screen.py          # 模式选择屏幕
│   │   ├── basic_config_screen.py  # 基础配置屏幕
│   │   ├── tool_screen.py          # 工具选择屏幕
│   │   ├── compiler_screen.py      # 编译器配置屏幕
│   │   ├── plugin_screen.py        # 插件选择屏幕
│   │   ├── advanced_screen.py      # 高级配置屏幕
│   │   ├── linux_package_screen.py # Linux 包配置屏幕
│   │   ├── summary_screen.py       # 配置摘要屏幕
│   │   ├── progress_screen.py      # 进度屏幕
│   │   └── complete_screen.py      # 完成屏幕
│   │
│   ├── widgets/                    # 自定义组件
│   │   ├── __init__.py
│   │   ├── file_browser.py         # 文件浏览器
│   │   ├── directory_tree.py       # 目录树
│   │   ├── plugin_selector.py      # 插件选择器
│   │   ├── config_form.py          # 配置表单
│   │   ├── summary_tree.py         # 配置摘要树
│   │   ├── wizard_footer.py        # 向导底部导航
│   │   ├── help_panel.py           # 帮助面板
│   │   └── notification.py         # 通知组件
│   │
│   ├── models/                     # 数据模型
│   │   ├── __init__.py
│   │   ├── config.py               # 配置数据模型
│   │   ├── plugin.py               # 插件模型
│   │   ├── compiler.py             # 编译器模型
│   │   └── template.py             # 配置模板模型
│   │
│   ├── core/                       # 核心业务逻辑
│   │   ├── __init__.py
│   │   ├── generator.py            # 脚本生成器
│   │   ├── nuitka_gen.py           # Nuitka 参数生成
│   │   ├── pyinstaller_gen.py      # PyInstaller 参数生成
│   │   ├── linux_pkg_gen.py        # Linux 包生成
│   │   ├── validator.py            # 配置验证器
│   │   ├── config_loader.py        # 配置加载器（YAML/TOML）
│   │   └── template_engine.py      # 模板引擎
│   │
│   ├── utils/                      # 工具函数
│   │   ├── __init__.py
│   │   ├── file_utils.py           # 文件操作
│   │   ├── path_utils.py           # 路径处理
│   │   ├── system_utils.py         # 系统信息
│   │   ├── env_checker.py          # 环境检查
│   │   └── logger.py               # 日志工具
│   │
│   ├── styles/                     # 样式文件
│   │   ├── app.tcss                # 主样式
│   │   ├── screens.tcss            # 屏幕样式
│   │   ├── widgets.tcss            # 组件样式
│   │   ├── themes/                 # 主题
│   │   │   ├── dark.tcss           # 暗色主题
│   │   │   └── light.tcss          # 亮色主题
│   │
│   ├── templates/                  # 脚本模板
│   │   ├── build_nuitka.py.j2      # Nuitka 模板
│   │   ├── build_pyinstaller.py.j2 # PyInstaller 模板
│   │   ├── linux_package.py.j2     # Linux 包模板
│   │   └── common.py.j2            # 通用代码模板
│   │
│   ├── i18n/                       # 国际化
│   │   ├── __init__.py
│   │   ├── zh_CN.json              # 简体中文
│   │   └── en_US.json              # 英文
│   │
│   └── config/                     # 配置文件
│       ├── __init__.py
│       ├── plugins.toml            # 插件定义
│       ├── compilers.toml          # 编译器配置
│       ├── defaults.toml           # 默认配置
│       └── defaults.yaml           # 默认配置（YAML格式）
│
├── tests/                          # 测试目录
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_generator.py
│   ├── test_validator.py
│   └── test_widgets.py
│
├── docs/                           # 文档
│   ├── README.md
│   ├── ARCHITECTURE.md             # 架构文档
│   ├── API.md                      # API 文档
│   └── CONTRIBUTING.md             # 贡献指南
│
├── examples/                       # 示例配置
│   ├── simple_gui.yaml             # 简单 GUI 应用配置示例
│   ├── simple_gui.toml
│   ├── scientific_app.yaml         # 科学计算应用配置示例
│   ├── scientific_app.toml
│   ├── web_service.yaml            # Web 服务配置示例
│   └── web_service.toml
│
├── logs/                           # 日志目录
│   ├── app.log                     # 应用日志
│   ├── error.log                   # 错误日志
│   └── debug.log                   # 调试日志
│
├── pyproject.toml                  # 项目配置
├── README.md                       # 项目说明
├── LICENSE                         # 许可证
└── .gitignore                      # Git 忽略
```

---

## 🎨 界面设计

### 屏幕流程图
```
┌─────────────────┐
│  欢迎屏幕        │
│  (Logo + 介绍)   │
└────────┬────────┘
         ↓
┌─────────────────┐
│  模式选择屏幕    │
│  (3种模式)       │
└────────┬────────┘
         ↓
┌─────────────────┐
│  基础配置屏幕    │
│  (项目/入口/图标)│
└────────┬────────┘
         ↓
┌─────────────────┐
│  工具选择屏幕    │
│  (Nuitka/PyInst) │
└────────┬────────┘
         ↓
┌─────────────────┐
│  编译器配置屏幕  │
│  (编译器选择)    │
└────────┬────────┘
         ↓
┌─────────────────┐
│  插件选择屏幕    │
│  (多选插件)      │
└────────┬────────┘
         ↓
┌─────────────────┐
│  高级配置屏幕    │
│  (输出/优化等)   │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Linux包配置屏幕 │
│  (可选)          │
└────────┬────────┘
         ↓
┌─────────────────┐
│  配置摘要屏幕    │
│  (确认配置)      │
└────────┬────────┘
         ↓
┌─────────────────┐
│  进度屏幕        │
│  (生成脚本)      │
└────────┬────────┘
         ↓
┌─────────────────┐
│  完成屏幕        │
│  (结果展示)      │
└─────────────────┘
```

### 关键界面设计

#### 1. 欢迎屏幕
```python
class WelcomeScreen(Screen):
    """欢迎屏幕"""
    
    def compose(self):
        yield Header()
        yield Container(
            Static(LOGO_ASCII, classes="logo"),
            Label("Python 构建脚本生成器 TUI", classes="title"),
            Label("v1.0.0", classes="version"),
            Label("跨平台 | 高效 | 智能", classes="subtitle"),
            Button("开始", variant="primary", id="start"),
            Button("加载配置", id="load"),
            Button("退出", id="quit"),
        )
        yield Footer()
```

#### 2. 文件浏览器组件
```python
class FileBrowser(Widget):
    """文件浏览器组件"""
    
    def compose(self):
        yield DirectoryTree("./", id="tree")
        yield Input(placeholder="输入路径或搜索...", id="path_input")
        yield Container(
            Button("选择", variant="primary"),
            Button("取消"),
            classes="actions"
        )
```

#### 3. 插件选择器
```python
class PluginSelector(Widget):
    """插件选择器"""
    
    def compose(self):
        yield Input(placeholder="搜索插件...", id="search")
        yield Tabs(
            Tab("GUI 框架", id="gui"),
            Tab("科学计算", id="scientific"),
            Tab("其他", id="others"),
        )
        yield ListView(id="plugin_list")
        yield Static("已选择: 0 个插件", id="count")
```

#### 4. 配置摘要树
```python
class SummaryTree(Widget):
    """配置摘要树"""
    
    def compose(self):
        tree = Tree("配置摘要")
        
        # 基础配置
        basic = tree.root.add("📁 基础配置")
        basic.add_leaf(f"项目目录: {config.project_dir}")
        basic.add_leaf(f"入口文件: {config.entry_file}")
        
        # 构建配置
        build = tree.root.add("🔧 构建配置")
        build.add_leaf(f"构建工具: {config.build_tool}")
        build.add_leaf(f"编译器: {config.compiler}")
        
        # 插件配置
        plugins = tree.root.add("🔌 插件配置")
        for plugin in config.plugins:
            plugins.add_leaf(plugin)
        
        yield tree
```

---

## 📊 数据模型

### 配置模型（Pydantic）
```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from pathlib import Path

class BuildConfig(BaseModel):
    """构建配置模型 - 适配项目级别 YAML 配置"""
    
    # 项目元信息
    class ProjectInfo(BaseModel):
        name: str = Field(description="项目名称")
        version: str = Field(default="1.0.0", description="项目版本")
        description: Optional[str] = Field(default=None, description="项目描述")
        author: Optional[str] = Field(default=None, description="作者")
    
    # 路径配置
    class PathsConfig(BaseModel):
        project_dir: Path = Field(default=Path("."), description="项目根目录")
        entry_file: Path = Field(description="入口文件")
        icon_file: Optional[Path] = Field(default=None, description="图标文件")
        output_dir: Path = Field(default=Path("dist"), description="输出目录")
    
    # 构建工具配置
    class BuildConfig(BaseModel):
        tool: str = Field(default="pyinstaller", description="构建工具")
        compiler: Optional[str] = Field(default=None, description="编译器（仅 nuitka）")
    
    # 打包选项
    class PackageConfig(BaseModel):
        standalone: bool = Field(default=True, description="独立模式")
        onefile: bool = Field(default=True, description="单文件模式")
        console: bool = Field(default=False, description="显示控制台")
    
    # 插件配置
    class PluginsConfig(BaseModel):
        enabled: List[str] = Field(default_factory=list, description="启用的插件")
        excluded_packages: List[str] = Field(default_factory=list, description="排除的包")
    
    # 优化选项
    class OptimizationConfig(BaseModel):
        jobs: int = Field(default=4, description="并行任务数")
        optimize: int = Field(default=0, description="优化级别")
        strip: bool = Field(default=False, description="去除调试信息")
        upx: bool = Field(default=False, description="UPX 压缩")
    
    # 平台特定配置
    class PlatformConfig(BaseModel):
        class WindowsConfig(BaseModel):
            company_name: Optional[str] = None
            file_version: Optional[str] = None
            product_version: Optional[str] = None
            copyright: Optional[str] = None
        
        class LinuxConfig(BaseModel):
            generate_packages: bool = False
            package_tool: str = "nfpm"
            package_types: List[str] = Field(default_factory=lambda: ["deb"])
        
        windows: Optional[WindowsConfig] = None
        linux: Optional[LinuxConfig] = None
    
    # 资源文件配置
    class ResourcesConfig(BaseModel):
        class DataFile(BaseModel):
            src: str
            dest: str
        
        data_files: List[DataFile] = Field(default_factory=list)
        hidden_imports: List[str] = Field(default_factory=list)
    
    # 高级选项
    class AdvancedConfig(BaseModel):
        runtime_hooks: List[str] = Field(default_factory=list)
        bootloader_ignore_signals: bool = False
        debug: bool = False
    
    # 元数据
    class Metadata(BaseModel):
        created_at: Optional[str] = None
        updated_at: Optional[str] = None
        last_build_tool: str = "pybuild-tui"
        config_version: str = "1.0"
    
    # 主配置字段
    project: ProjectInfo
    paths: PathsConfig
    build: BuildConfig
    package: PackageConfig = Field(default_factory=PackageConfig)
    plugins: PluginsConfig = Field(default_factory=PluginsConfig)
    optimization: OptimizationConfig = Field(default_factory=OptimizationConfig)
    platform: Optional[PlatformConfig] = None
    resources: Optional[ResourcesConfig] = None
    advanced: Optional[AdvancedConfig] = None
    metadata: Optional[Metadata] = None
    
    class Config:
        arbitrary_types_allowed = True
```

---

## 🔧 核心功能实现

### 1. 主应用类
```python
from textual.app import App, ComposeResult
from textual.binding import Binding

class PyBuildTUI(App):
    """Python 构建脚本生成器 TUI 应用"""
    
    CSS_PATH = "styles/app.tcss"
    TITLE = "Python Build Script Generator"
    
    BINDINGS = [
        Binding("q", "quit", "退出"),
        Binding("d", "toggle_dark", "切换主题"),
        Binding("h", "help", "帮助"),
        Binding("s", "save_config", "保存配置"),
        Binding("l", "load_config", "加载配置"),
    ]
    
    SCREENS = {
        "welcome": WelcomeScreen,
        "mode": ModeScreen,
        "basic_config": BasicConfigScreen,
        "tool": ToolScreen,
        "compiler": CompilerScreen,
        "plugin": PluginScreen,
        "advanced": AdvancedScreen,
        "linux_package": LinuxPackageScreen,
        "summary": SummaryScreen,
        "progress": ProgressScreen,
        "complete": CompleteScreen,
    }
    
    def __init__(self):
        super().__init__()
        self.config = BuildConfig()
        self.screen_stack = []
        # 初始化日志系统
        self.logger = LoggerSetup.get_logger("PyBuildTUI")
    
    def on_mount(self):
        """应用启动"""
        self.logger.info("应用启动")
        self.push_screen("welcome")
    
    def action_toggle_dark(self):
        """切换主题"""
        self.dark = not self.dark
        self.logger.info(f"切换主题: {'dark' if self.dark else 'light'}")
    
    def action_help(self):
        """显示帮助"""
        self.logger.debug("打开帮助界面")
        self.push_screen(HelpScreen())
    
    def action_save_config(self):
        """保存配置"""
        try:
            self.logger.info("开始保存配置")
            # 实现配置保存逻辑
            self.logger.success("配置保存成功")
        except Exception as e:
            self.logger.error(f"保存配置失败: {e}")
            self.logger.exception(e)
    
    def action_load_config(self):
        """加载配置"""
        try:
            self.logger.info("开始加载配置")
            # 实现配置加载逻辑
            self.logger.success("配置加载成功")
        except Exception as e:
            self.logger.error(f"加载配置失败: {e}")
            self.logger.exception(e)
    
    def go_next_screen(self, next_screen: str):
        """前进到下一个屏幕"""
        self.logger.debug(f"切换屏幕: {self.screen.name} -> {next_screen}")
        self.screen_stack.append(self.screen.name)
        self.push_screen(next_screen)
    
    def go_previous_screen(self):
        """返回上一个屏幕"""
        if self.screen_stack:
            previous = self.screen_stack.pop()
            self.logger.debug(f"返回屏幕: {self.screen.name} -> {previous}")
            self.pop_screen()
```

### 2. 脚本生成器
```python
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

class ScriptGenerator:
    """脚本生成器"""
    
    def __init__(self):
        template_dir = Path(__file__).parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.logger = LoggerSetup.get_logger("ScriptGenerator")
    
    def generate_nuitka_args(self, config: BuildConfig) -> List[str]:
        """生成 Nuitka 参数"""
        self.logger.debug(f"开始生成 Nuitka 参数: {config.app_name}")
        args = ["nuitka"]
        
        if config.standalone:
            args.append("--standalone")
        if config.onefile:
            args.append("--onefile")
        if not config.show_console:
            args.append("--windows-disable-console")
        
        # 编译器
        if config.compiler == "mingw64":
            args.append("--mingw64")
        elif config.compiler == "msvc":
            args.append("--msvc=latest")
        elif config.compiler == "clang":
            args.append("--clang")
        
        # 输出
        args.append(f"--output-dir={config.output_dir}")
        args.append(f"--output-filename={config.app_name}")
        
        # 插件
        for plugin in config.plugins:
            args.append(f"--enable-plugin={plugin}")
            self.logger.debug(f"添加插件: {plugin}")
        
        # 入口文件
        args.append(str(config.entry_file))
        
        self.logger.info(f"生成 Nuitka 参数完成, 共 {len(args)} 个参数")
        return args
    
    def generate_script(self, config: BuildConfig) -> str:
        """生成构建脚本"""
        self.logger.info(f"开始生成构建脚本: {config.build_tool}")
        
        try:
            if config.build_tool == "nuitka":
                template = self.env.get_template("build_nuitka.py.j2")
            else:
                template = self.env.get_template("build_pyinstaller.py.j2")
            
            args = self.generate_nuitka_args(config)
            
            script = template.render(
                config=config,
                args=args,
                timestamp=datetime.now().isoformat(),
            )
            
            self.logger.success(f"构建脚本生成成功: {config.app_name}")
            return script
            
        except Exception as e:
            self.logger.error(f"生成构建脚本失败: {e}")
            self.logger.exception(e)
            raise
    
    def save_script(self, script: str, output_path: Path):
        """保存脚本"""
        try:
            self.logger.info(f"保存脚本到: {output_path}")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(script)
            self.logger.success(f"脚本保存成功: {output_path}")
        except Exception as e:
            self.logger.error(f"保存脚本失败: {e}")
            self.logger.exception(e)
            raise
```

### 3. 配置验证器
```python
class ConfigValidator:
    """配置验证器"""
    
    @staticmethod
    def validate_project_dir(path: str) -> tuple[bool, str]:
        """验证项目目录"""
        p = Path(path)
        if not p.exists():
            return False, f"目录不存在: {path}"
        if not p.is_dir():
            return False, f"不是有效目录: {path}"
        return True, str(p.resolve())
    
    @staticmethod
    def validate_entry_file(path: str, base_dir: str) -> tuple[bool, str]:
        """验证入口文件"""
        p = Path(base_dir) / path
        if not p.exists():
            return False, f"文件不存在: {p}"
        if p.suffix != '.py':
            return False, "入口文件必须是 .py 文件"
        return True, str(p)
    
    @staticmethod
    def validate_icon_file(path: str, base_dir: str) -> tuple[bool, str]:
        """验证图标文件"""
        if not path:
            return True, ""
        p = Path(base_dir) / path
        if not p.exists():
            return False, f"图标文件不存在: {p}"
        if p.suffix not in ['.ico', '.png']:
            return False, "图标文件必须是 .ico 或 .png 格式"
        return True, str(p)
```

### 4. YAML 配置加载器
```python
import yaml
import toml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import ValidationError

class ConfigLoader:
    """配置加载器 - 支持 YAML 和 TOML 格式"""
    
    def __init__(self):
        self.logger = LoggerSetup.get_logger("ConfigLoader")
    
    def load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """从 YAML 文件加载配置
        
        Args:
            file_path: YAML 文件路径
            
        Returns:
            配置字典
        """
        try:
            self.logger.info(f"加载 YAML 配置文件: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                config_dict = yaml.safe_load(f)
            
            if not config_dict:
                raise ValueError("配置文件为空")
            
            self.logger.success(f"YAML 配置加载成功: {file_path}")
            return config_dict
            
        except yaml.YAMLError as e:
            self.logger.error(f"YAML 解析失败: {e}")
            raise ValueError(f"YAML 文件格式错误: {e}")
        except Exception as e:
            self.logger.error(f"加载 YAML 文件失败: {e}")
            raise
    
    def load_config(self, file_path: Path) -> BuildConfig:
        """自动识别文件格式并加载配置
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            BuildConfig 实例
        """
        if not file_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {file_path}")
        
        suffix = file_path.suffix.lower()
        
        try:
            # 根据文件后缀加载配置
            if suffix in ['.yaml', '.yml']:
                config_dict = self.load_yaml(file_path)
            elif suffix == '.toml':
                config_dict = self.load_toml(file_path)
            else:
                raise ValueError(f"不支持的文件格式: {suffix}")
            
            # 验证并创建 BuildConfig 实例
            config = BuildConfig(**config_dict)
            self.logger.success(f"配置验证成功: {config.app_name}")
            return config
            
        except ValidationError as e:
            self.logger.error(f"配置验证失败: {e}")
            raise ValueError(f"配置数据验证失败: {e}")
    
    def save_yaml(self, config: BuildConfig, file_path: Path):
        """保存配置为 YAML 文件"""
        try:
            self.logger.info(f"保存配置为 YAML: {file_path}")
            config_dict = config.dict()
            
            # 转换 Path 对象为字符串
            for key, value in config_dict.items():
                if isinstance(value, Path):
                    config_dict[key] = str(value)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, allow_unicode=True, 
                         default_flow_style=False, sort_keys=False)
            
            self.logger.success(f"YAML 配置保存成功: {file_path}")
        except Exception as e:
            self.logger.error(f"保存 YAML 配置失败: {e}")
            raise
```

### 5. 从 YAML 生成 build.py
```python
class BuildScriptGenerator:
    """从 YAML 配置生成 build.py 脚本"""
    
    def __init__(self):
        template_dir = Path(__file__).parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.logger = LoggerSetup.get_logger("BuildScriptGenerator")
        self.config_loader = ConfigLoader()
    
    def generate_from_yaml(self, yaml_path: Path, output_path: Optional[Path] = None) -> str:
        """从 YAML 文件生成 build.py 脚本"""
        try:
            self.logger.info(f"开始从 YAML 生成 build.py: {yaml_path}")
            
            # 加载 YAML 配置
            config = self.config_loader.load_config(yaml_path)
            
            # 生成脚本
            if config.build_tool == "nuitka":
                template = self.env.get_template("build_nuitka.py.j2")
                args = self._generate_nuitka_args(config)
            else:
                template = self.env.get_template("build_pyinstaller.py.j2")
                args = self._generate_pyinstaller_args(config)
            
            script = template.render(
                config=config,
                args=args,
                timestamp=datetime.now().isoformat(),
            )
            
            # 保存文件
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(script)
                self.logger.success(f"build.py 生成成功: {output_path}")
            
            return script
        except Exception as e:
            self.logger.error(f"生成 build.py 失败: {e}")
            raise
    
    def _generate_nuitka_args(self, config: BuildConfig) -> list:
        """生成 Nuitka 编译参数 - 适配新的 YAML 结构"""
        args = []
        
        # 基本选项
        if config.package.standalone:
            args.append("--standalone")
        if config.package.onefile:
            args.append("--onefile")
        
        # 控制台设置
        if not config.package.console:
            args.append("--disable-console")
        
        # 编译器
        if config.build.compiler:
            if config.build.compiler == "mingw64":
                args.append("--mingw64")
            elif config.build.compiler == "msvc":
                args.append("--msvc=latest")
            elif config.build.compiler == "clang":
                args.append("--clang")
        
        # 输出配置
        args.append(f"--output-dir={config.paths.output_dir}")
        args.append(f"--output-filename={config.project.name}")
        
        # 图标
        if config.paths.icon_file:
            args.append(f"--windows-icon-from-ico={config.paths.icon_file}")
        
        # 插件
        for plugin in config.plugins.enabled:
            args.append(f"--enable-plugin={plugin}")
            self.logger.debug(f"添加插件: {plugin}")
        
        # 排除包
        for pkg in config.plugins.excluded_packages:
            args.append(f"--nofollow-import-to={pkg}")
        
        # 优化选项
        if config.optimization:
            args.append(f"--jobs={config.optimization.jobs}")
        
        # 入口文件
        args.append(str(config.paths.entry_file))
        
        self.logger.info(f"生成 Nuitka 参数完成, 共 {len(args)} 个")
        return args
```

### 6. 日志系统（Loguru）
```python
from loguru import logger
from pathlib import Path
import sys

class LoggerSetup:
    """日志系统配置"""
    
    @staticmethod
    def setup_logger(log_level: str = "INFO", enable_file: bool = True):
        """配置日志系统
        
        Args:
            log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            enable_file: 是否启用文件日志
        """
        # 移除默认处理器
        logger.remove()
        
        # 控制台输出 - 仅显示 WARNING 及以上级别
        logger.add(
            sys.stderr,
            level="WARNING",
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            colorize=True,
        )
        
        if enable_file:
            # 创建日志目录
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # 应用日志 - 记录 INFO 及以上级别
            logger.add(
                log_dir / "app.log",
                level="INFO",
                format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
                rotation="10 MB",      # 日志文件达到 10MB 时轮转
                retention="30 days",    # 保留 30 天
                compression="zip",      # 压缩旧日志
                encoding="utf-8",
            )
            
            # 错误日志 - 仅记录 ERROR 及以上级别
            logger.add(
                log_dir / "error.log",
                level="ERROR",
                format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}\n{exception}",
                rotation="10 MB",
                retention="90 days",    # 错误日志保留更久
                compression="zip",
                encoding="utf-8",
                backtrace=True,         # 显示完整回溯
                diagnose=True,          # 显示变量值
            )
            
            # 调试日志 - 记录所有级别（开发模式）
            if log_level == "DEBUG":
                logger.add(
                    log_dir / "debug.log",
                    level="DEBUG",
                    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {process} | {thread} | {name}:{function}:{line} | {message}",
                    rotation="50 MB",
                    retention="7 days",
                    compression="zip",
                    encoding="utf-8",
                )
        
        logger.info(f"日志系统初始化完成，级别: {log_level}")
    
    @staticmethod
    def get_logger(name: str = None):
        """获取日志记录器
        
        Args:
            name: 日志记录器名称
            
        Returns:
            logger 实例
        """
        if name:
            return logger.bind(name=name)
        return logger


# 使用示例
class ExampleUsage:
    """日志使用示例"""
    
    def __init__(self):
        self.logger = LoggerSetup.get_logger("ExampleUsage")
    
    def process_config(self, config):
        """处理配置示例"""
        self.logger.info(f"开始处理配置: {config.app_name}")
        
        try:
            # 处理逻辑
            self.logger.debug(f"配置详情: {config}")
            
            # 验证
            if not config.entry_file:
                self.logger.warning("未指定入口文件")
            
            self.logger.success(f"配置处理完成: {config.app_name}")
            
        except Exception as e:
            self.logger.error(f"处理配置失败: {config.app_name}")
            self.logger.exception(e)  # 记录完整异常信息
            raise


# 在应用启动时初始化
def init_app():
    """应用初始化"""
    # 开发模式
    LoggerSetup.setup_logger(log_level="DEBUG", enable_file=True)
    
    # 生产模式
    # LoggerSetup.setup_logger(log_level="INFO", enable_file=True)
```

---

## 📅 开发计划

### Phase 1: 基础框架搭建（Week 1-2）

#### Week 1: 项目初始化
- [ ] **Day 1-2**: 项目结构搭建
  - 创建目录结构
  - 配置 pyproject.toml
  - 设置开发环境
  - 初始化 Git 仓库

- [ ] **Day 3-4**: 数据模型设计
  - 实现 BuildConfig 模型
  - 实现 Plugin 模型
  - 实现 Compiler 模型
  - 编写模型测试

- [ ] **Day 5-7**: 主应用框架
  - 实现 PyBuildTUI 主类
  - 创建基础样式文件
  - 实现屏幕导航逻辑
  - 实现主题切换

#### Week 2: 基础组件开发
- [ ] **Day 1-2**: 通用组件
  - 实现 WizardFooter 组件
  - 实现 HelpPanel 组件
  - 实现 Notification 组件

- [ ] **Day 3-4**: 文件浏览器
  - 实现 FileBrowser 组件
  - 实现 DirectoryTree 组件
  - 添加搜索功能
  - 添加快捷键支持

- [ ] **Day 5-7**: 配置表单
  - 实现 ConfigForm 组件
  - 实现实时验证
  - 实现错误提示
  - 编写组件测试

### Phase 2: 核心屏幕开发（Week 3-4）

#### Week 3: 前半流程屏幕
- [ ] **Day 1**: 欢迎屏幕
  - 设计 Logo ASCII 艺术
  - 实现欢迎界面
  - 添加按钮动作

- [ ] **Day 2**: 模式选择屏幕
  - 实现 3 种模式选择
  - 添加模式说明
  - 实现模式验证

- [ ] **Day 3**: 基础配置屏幕
  - 实现项目目录选择
  - 实现入口文件选择
  - 实现图标文件选择
  - 集成文件浏览器

- [ ] **Day 4**: 工具选择屏幕
  - 实现 Nuitka/PyInstaller 选择
  - 添加工具说明
  - 实现环境检查

- [ ] **Day 5-7**: 编译器配置屏幕
  - 实现编译器选择
  - 添加平台检测
  - 实现编译器验证
  - 添加编译器说明

#### Week 4: 后半流程屏幕
- [ ] **Day 1-2**: 插件选择屏幕
  - 实现 PluginSelector 组件
  - 实现插件分类
  - 实现搜索功能
  - 实现多选逻辑

- [ ] **Day 3**: 高级配置屏幕
  - 实现输出配置
  - 实现优化选项
  - 实现版本信息配置

- [ ] **Day 4**: Linux 包配置屏幕
  - 实现包类型选择
  - 实现工具选择
  - 实现高级选项

- [ ] **Day 5-7**: 摘要和进度屏幕
  - 实现配置摘要树
  - 实现进度显示
  - 实现完成界面
  - 添加导出选项

### Phase 3: 核心功能实现（Week 5-6）

#### Week 5: 脚本生成器
- [ ] **Day 1-2**: Nuitka 生成器
  - 实现参数生成逻辑
  - 实现模板渲染
  - 添加平台适配

- [ ] **Day 3-4**: PyInstaller 生成器
  - 实现参数生成逻辑
  - 实现模板渲染
  - 添加版本文件生成

- [ ] **Day 5-7**: Linux 包生成器
  - 实现 NFPM 配置生成
  - 实现 FPM 配置生成
  - 实现 systemd 服务生成
  - 实现桌面文件生成

#### Week 6: 配置管理
- [ ] **Day 1-2**: YAML/TOML 配置支持
  - 实现 ConfigLoader 类
  - 实现 YAML 文件加载
  - 实现 TOML 文件加载
  - 实现配置保存（YAML/TOML）
  - 实现配置验证

- [ ] **Day 3-4**: YAML 生成 build.py
  - 实现 BuildScriptGenerator 类
  - 从 YAML 配置生成 Nuitka 脚本
  - 从 YAML 配置生成 PyInstaller 脚本
  - 创建配置示例文件（simple_gui.yaml, scientific_app.yaml）
  - 添加命令行工具支持

- [ ] **Day 5-7**: 配置模板管理
  - 创建预设模板（GUI、科学计算、Web 服务）
  - 实现模板选择界面
  - 实现模板导入/导出
  - 实现环境检查（Python、编译器、打包工具）

### Phase 4: 高级特性（Week 7-8）

#### Week 7: 用户体验优化
- [ ] **Day 1-2**: 国际化
  - 实现多语言支持
  - 创建中文翻译
  - 创建英文翻译

- [ ] **Day 3-4**: 主题系统
  - 创建暗色主题
  - 创建亮色主题
  - 实现主题切换动画

- [ ] **Day 5-7**: 帮助系统
  - 实现上下文帮助
  - 创建使用教程
  - 添加快捷键提示
  - 实现帮助搜索

#### Week 8: 错误处理和日志
- [ ] **Day 1-2**: 日志系统集成
  - 创建 logs 目录结构
  - 实现 LoggerSetup 类
  - 配置日志轮转和压缩
  - 配置多级别日志输出（app.log, error.log, debug.log）
  - 集成 loguru 到主应用
  - 在关键模块中添加日志记录

- [ ] **Day 3-4**: 错误处理
  - 实现全局错误捕获
  - 实现友好错误提示
  - 添加错误恢复机制
  - 错误信息自动记录到日志

- [ ] **Day 5-7**: 日志监控和性能优化
  - 实现日志级别动态控制
  - 添加日志查看功能（可选）
  - 优化启动速度
  - 优化渲染性能
  - 优化内存占用
  - 添加性能监控日志

### Phase 5: 测试和文档（Week 9-10）

#### Week 9: 测试
- [ ] **Day 1-2**: 单元测试
  - 测试数据模型
  - 测试验证器
  - 测试生成器
  - 测试工具函数

- [ ] **Day 3-4**: 集成测试
  - 测试屏幕流程
  - 测试配置保存/加载
  - 测试脚本生成

- [ ] **Day 5-7**: 用户测试
  - 内部测试
  - 收集反馈
  - 修复 Bug
  - 性能调优

#### Week 10: 文档和发布
- [ ] **Day 1-2**: 用户文档
  - 编写 README
  - 编写使用手册
  - 创建示例
  - 录制演示视频

- [ ] **Day 3-4**: 开发文档
  - 编写架构文档
  - 编写 API 文档
  - 编写贡献指南

- [ ] **Day 5-7**: 发布准备
  - 版本打包
  - 创建发布说明
  - 上传 PyPI
  - 创建 GitHub Release

---

## 🎨 样式设计

### 主样式（app.tcss）
```css
/* 全局样式 */
Screen {
    background: $surface;
    layers: base overlay;
}

/* Header */
Header {
    dock: top;
    height: 3;
    background: $primary;
    color: $text;
    content-align: center middle;
}

/* Footer */
Footer {
    dock: bottom;
    height: 3;
    background: $panel;
}

/* Container */
Container {
    width: 100%;
    height: 100%;
    padding: 1 2;
}

/* 模式选择器 */
.mode-selector {
    border: solid $primary;
    height: auto;
    padding: 1;
    margin: 1 0;
}

.mode-option {
    height: 3;
    padding: 0 2;
    margin: 1 0;
}

.mode-option:hover {
    background: $boost;
}

.mode-option.-selected {
    background: $primary;
    color: $text;
}

/* 配置面板 */
.config-panel {
    border: solid $accent;
    height: auto;
    margin: 1 0;
    padding: 1;
}

.config-panel > Label {
    color: $text-muted;
    padding: 0 0 1 0;
}

/* 插件选择器 */
.plugin-category {
    border: round $primary;
    height: auto;
    padding: 1;
    margin: 1 0;
}

.plugin-item {
    height: 3;
    padding: 0 1;
}

.plugin-item:hover {
    background: $boost;
}

.plugin-item Checkbox {
    width: 100%;
}

/* 按钮 */
Button {
    min-width: 10;
    margin: 0 1;
}

Button.-primary {
    background: $success;
}

Button.-secondary {
    background: $warning;
}

Button.-danger {
    background: $error;
}

/* 输入框 */
Input {
    width: 100%;
    margin: 1 0;
}

Input:focus {
    border: tall $accent;
}

/* 进度条 */
ProgressBar {
    width: 100%;
    margin: 1 0;
}

/* 树形视图 */
Tree {
    width: 100%;
    height: auto;
    border: solid $primary;
    padding: 1;
}

/* 通知 */
.notification {
    layer: overlay;
    align: center middle;
    width: 60;
    height: auto;
    background: $panel;
    border: heavy $primary;
    padding: 1;
}

.notification.-success {
    border: heavy $success;
}

.notification.-error {
    border: heavy $error;
}

.notification.-warning {
    border: heavy $warning;
}

/* 帮助面板 */
.help-panel {
    width: 80;
    height: 30;
    background: $panel;
    border: heavy $primary;
    padding: 1;
}

/* Wizard Footer */
.wizard-footer {
    dock: bottom;
    height: 5;
    background: $surface-darken-1;
    padding: 1;
}

.wizard-footer Button {
    margin: 0 1;
}
```

---

## 📦 配置文件示例

### plugins.toml
```toml
[gui]
pyqt5 = { name = "PyQt5", description = "Qt5 GUI 框架" }
pyqt6 = { name = "PyQt6", description = "Qt6 GUI 框架" }
pyside2 = { name = "PySide2", description = "Qt5 GUI 框架（官方）" }
pyside6 = { name = "PySide6", description = "Qt6 GUI 框架（官方）" }
tkinter = { name = "Tkinter", description = "Python 内置 GUI 框架" }

[scientific]
numpy = { name = "NumPy", description = "数值计算库" }
scipy = { name = "SciPy", description = "科学计算库" }
pandas = { name = "Pandas", description = "数据分析库" }
matplotlib = { name = "Matplotlib", description = "数据可视化库" }

[others]
pillow = { name = "Pillow", description = "图像处理库" }
requests = { name = "Requests", description = "HTTP 请求库" }
sqlalchemy = { name = "SQLAlchemy", description = "数据库 ORM" }
```

### compilers.toml
```toml
[mingw64]
name = "MinGW64"
platforms = ["win32"]
description = "Windows 上的 GCC 编译器"
check_command = "gcc --version"

[msvc]
name = "MSVC"
platforms = ["win32"]
description = "Microsoft Visual Studio 编译器"
check_command = "cl /?"

[clang]
name = "Clang"
platforms = ["win32", "linux", "darwin"]
description = "跨平台 LLVM 编译器"
check_command = "clang --version"

[gcc]
name = "GCC"
platforms = ["linux", "darwin"]
description = "GNU C/C++ 编译器"
check_command = "gcc --version"
```

### build_config.yaml 示例
```yaml
# Python 构建配置文件 - 项目级别配置

# ============= 项目元信息 =============
project:
  name: MyApplication          # 项目名称
  version: 1.0.0              # 项目版本
  description: 我的应用程序    # 项目描述
  author: 开发者               # 作者

# ============= 路径配置 =============
paths:
  project_dir: .              # 项目根目录
  entry_file: main.py         # 入口文件
  icon_file: resources/icon.ico  # 图标文件（可选）
  output_dir: dist            # 输出目录

# ============= 构建工具配置 =============
build:
  tool: pyinstaller           # 构建工具: pyinstaller | nuitka
  compiler: clang             # 编译器: mingw64 | msvc | clang | gcc (仅 nuitka)

# ============= 打包选项 =============
package:
  standalone: true            # 独立模式
  onefile: true              # 单文件模式
  console: false             # 显示控制台窗口

# ============= 插件和依赖 =============
plugins:
  enabled:                   # 启用的插件
    - pyqt5
    - numpy
    - matplotlib
  excluded_packages:         # 排除的包
    - tkinter
    - pytest
    - sphinx

# ============= 优化选项 =============
optimization:
  jobs: 4                    # 并行编译任务数
  optimize: 2                # 优化级别 (0-2)
  strip: true                # 去除调试信息
  upx: false                 # 使用 UPX 压缩（可选）

# ============= 平台特定配置 =============
platform:
  windows:
    company_name: MyCompany
    file_version: 1.0.0.0
    product_version: 1.0.0
    copyright: Copyright © 2024
  linux:
    generate_packages: true   # 生成 Linux 包
    package_tool: nfpm       # nfpm | fpm
    package_types:
      - deb
      - rpm

# ============= 资源文件 =============
resources:
  data_files:                # 额外的数据文件
    - src: resources/config.json
      dest: config
    - src: resources/images
      dest: images
  hidden_imports:            # 隐藏导入
    - pkg_resources
    - sqlalchemy.dialects

# ============= 高级选项 =============
advanced:
  runtime_hooks: []          # 运行时钩子文件
  bootloader_ignore_signals: false
  debug: false               # 调试模式

# ============= 元数据（自动生成）=============
metadata:
  created_at: "2024-01-15T10:30:00"
  updated_at: "2024-01-20T15:45:00"
  last_build_tool: pybuild-tui
  config_version: "1.0"
```

### 简单 GUI 应用配置示例
```yaml
# simple_gui.yaml - GUI 应用配置

project:
  name: SimpleGUI
  version: 1.0.0
  description: 简单的 GUI 应用

paths:
  project_dir: ./simple_gui
  entry_file: main.py
  icon_file: icon.ico
  output_dir: dist

build:
  tool: pyinstaller

package:
  standalone: true
  onefile: true
  console: false

plugins:
  enabled:
    - pyqt5

optimization:
  jobs: 4

platform:
  windows:
    company_name: MyCompany
    file_version: 1.0.0.0
```

### 科学计算应用配置示例
```yaml
# scientific_app.yaml - 科学计算应用配置

project:
  name: DataAnalyzer
  version: 2.0.0
  description: 数据分析工具

paths:
  project_dir: ./data_analyzer
  entry_file: app.py
  output_dir: dist

build:
  tool: pyinstaller

package:
  standalone: true
  onefile: false
  console: true

plugins:
  enabled:
    - numpy
    - scipy
    - pandas
    - matplotlib
  excluded_packages:
    - pytest
    - sphinx
    - jupyter

optimization:
  jobs: 6
  optimize: 2

resources:
  hidden_imports:
    - scipy.special.cython_special
    - pandas.plotting._matplotlib
```

---

## 🚀 运行和部署

### 开发模式
```bash
# 安装依赖
pip install -e ".[dev]"

# 运行应用
textual run --dev src/app.py

# 运行测试
pytest

# 代码检查
ruff check .
black --check .

# 类型检查
mypy src
```

### 生产部署
```bash
# 构建包
python -m build

# 安装
pip install dist/src-1.0.0-py3-none-any.whl

# 运行
pybuild-tui
```

### 从 YAML 生成 build.py
```bash
# 使用命令行工具
pybuild-tui generate build_config.yaml

# 指定输出文件
pybuild-tui generate build_config.yaml -o build.py

# Python 脚本调用
from src.core.config_loader import ConfigLoader
from src.core.generator import BuildScriptGenerator
from datetime import datetime

# 加载 YAML 配置
loader = ConfigLoader()
config = loader.load_config("build_config.yaml")

# 生成 build.py
generator = BuildScriptGenerator()
generator.generate_from_yaml("build_config.yaml", "build.py")

# 更新元数据
config.metadata.updated_at = datetime.now().isoformat()
loader.save_yaml(config, "build_config.yaml")
```

### 工作流程
```bash
# ========== 首次使用：生成配置和脚本 ==========
pybuild-tui
# 1. 选择项目目录（例如：/home/user/my_project）
# 2. 通过 TUI 界面配置所有选项：
#    - 入口文件：main.py
#    - 构建工具：pyinstaller
#    - 插件选择：pyqt5, numpy
#    - 优化选项等...
# 3. 保存后生成两个文件：
#    ✅ /home/user/my_project/build_config.yaml  # 配置文件
#    ✅ /home/user/my_project/build.py           # 构建脚本

# ========== 再次使用：自动加载配置 ==========
cd /home/user/my_project
pybuild-tui
# 1. 自动检测 build_config.yaml
# 2. 加载所有配置到 TUI 界面
# 3. 修改任意配置（例如：添加插件、修改输出目录）
# 4. 保存后更新两个文件：
#    🔄 build_config.yaml  # 更新配置
#    🔄 build.py           # 重新生成脚本

# ========== 命令行模式：直接从 YAML 生成 ==========
pybuild-tui generate build_config.yaml
# 直接从配置文件生成 build.py，无需 TUI 交互

# ========== 执行构建 ==========
python build.py
# 运行生成的构建脚本，开始编译/打包
```

## 项目目录结构

### 使用前（用户项目）
```
my_project/
├── src/
│   └── __init__.py
├── main.py              # 项目入口
├── requirements.txt
└── README.md
```

### 使用后（仅新增 2 个文件）
```
my_project/
├── src/
│   └── __init__.py
├── main.py
├── requirements.txt
├── README.md
├── build_config.yaml    # ✅ 新增：构建配置文件
└── build.py             # ✅ 新增：构建脚本
```

### 构建后（生成输出目录）
```
my_project/
├── src/
├── main.py
├── build_config.yaml
├── build.py
└── dist/                # 构建输出目录
    └── MyApp.exe        # 编译后的可执行文件
```

### 打包分发
```bash
# 使用 PyInstaller
pyinstaller --onefile --name pybuild-tui src/__main__.py

# 使用 Nuitka
nuitka --standalone --onefile \
  --output-filename=pybuild-tui \
  src/__main__.py
```

---

## 📊 项目里程碑

### Milestone 1: MVP (Week 1-4)
- ✅ 基础框架搭建
- ✅ 核心屏幕开发
- ✅ 基本脚本生成功能
- 🎯 目标：可运行的最小可用产品

### Milestone 2: Feature Complete (Week 5-7)
- ✅ 所有核心功能实现
- ✅ 配置管理完善
- ✅ 用户体验优化
- 🎯 目标：功能完整的应用

### Milestone 3: Production Ready (Week 8-10)
- ✅ 完整测试覆盖
- ✅ 文档完善
- ✅ 性能优化
- ✅ 发布准备
- 🎯 目标：生产就绪版本

---

## 🎯 成功指标

### 性能指标
- 启动时间 < 1 秒
- 屏幕切换延迟 < 100ms
- 内存占用 < 50MB
- CPU 占用 < 5%（空闲时）

### 质量指标
- 代码覆盖率 > 80%
- 无严重 Bug
- 跨平台兼容性 100%
- 用户满意度 > 4.5/5

### 功能指标
- 支持 2 种构建工具
- 支持 4+ 种编译器
- 支持 14+ 种插件
- 支持 3 种运行模式

---

## 🤝 贡献指南

### 开发流程
1. Fork 项目
2. 创建特性分支
3. 提交代码
4. 通过测试
5. 创建 Pull Request

### 代码规范
- 使用 Black 格式化
- 使用 Ruff 检查
- 使用 MyPy 类型检查
- 遵循 PEP 8

### 提交规范
```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：
- feat: 新功能
- fix: Bug 修复
- docs: 文档
- style: 格式
- refactor: 重构
- test: 测试
- chore: 构建

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- Textual - 优秀的 TUI 框架
- Rich - 强大的终端渲染库
- Pydantic - 数据验证
- 原始 CLI 版本的作者

---

**让我们一起打造最优秀的 Python 构建脚本生成器！** 🚀
