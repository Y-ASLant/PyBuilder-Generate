# GitHub Actions 工作流

## 触发方式

通过提交信息前缀触发构建：

| 前缀 | 工作流 | 输出目录 |
|------|--------|----------|
| `build:` | **同时触发两个** | 两个构建产物 |
| `build_0:` | 仅 PyInstaller | `build/PyBuilder/` |
| `build_1:` | 仅 Nuitka | `build/main.dist/` |

**示例**:
```bash
git commit -m "build: 发布新版本"        # 同时构建
git commit -m "build_0: 修复界面问题"    # 仅 PyInstaller
git commit -m "build_1: 性能优化"        # 仅 Nuitka
```

## 下载产物

Actions → 选择运行 → Artifacts 下载

## 注意事项

- 在 `main` 和 `dev` 分支触发
- 产物保留 7 天
- 其他提交不触发构建
