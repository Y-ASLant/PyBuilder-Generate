"""
安装包脚本生成器模块
生成 Inno Setup (.iss) 和 nfpm 配置文件
"""

import re
import uuid
from pathlib import Path
from typing import Dict, Any, List

# 预编译正则表达式
_SPLIT_PATTERN = re.compile(r"[,\s，]+")


def _split_items(text: str) -> List[str]:
    """分割字符串，支持空格、英文逗号、中文逗号"""
    return [s.strip() for s in _SPLIT_PATTERN.split(text) if s.strip()]


def generate_inno_setup_script(config: Dict[str, Any], project_dir: Path) -> str:
    """生成 Inno Setup 脚本 (.iss)"""
    lines = []

    # 获取配置值
    app_name = config.get("installer_app_name", config.get("project_name", "MyApp"))
    version = config.get("installer_version", config.get("version", "1.0.0"))
    publisher = config.get("installer_publisher", config.get("company_name", ""))
    app_url = config.get("installer_url", "")
    exe_name = config.get("installer_exe_name", f"{app_name}.exe")
    source_dir = config.get("installer_source_dir", config.get("output_dir", "build"))
    output_dir = config.get("installer_output_dir", "dist/installer")
    icon_file = config.get("installer_icon", config.get("icon_file", ""))

    # 安装目录
    install_dir = config.get("installer_install_dir", "").strip()
    if not install_dir:
        install_dir = "{autopf}\\{#MyAppName}"

    # 安装选项
    desktop_icon = config.get("installer_desktop_icon", True)
    start_menu = config.get("installer_start_menu", True)
    add_path = config.get("installer_add_path", False)
    path_scope = config.get("installer_path_scope", "user")  # user 或 system
    run_after = config.get("installer_run_after", True)
    uninstall_old = config.get("installer_uninstall_old", True)
    privileges = config.get("installer_privileges", "lowest")
    compression = config.get("installer_compression", "lzma2/ultra64")
    file_assoc = config.get("installer_file_assoc", "").strip()
    extra_shortcuts = config.get("installer_extra_shortcuts", "").strip()

    # 可选文件
    license_file = config.get("installer_license", "")
    readme_file = config.get("installer_readme", "")

    # 自定义后缀（用于安装包文件名）
    custom_suffix = config.get("installer_custom_suffix", "").strip()

    # AppId（不带花括号存储）
    app_id = config.get("installer_appid", "").strip().strip("{}")
    if not app_id:
        app_id = str(uuid.uuid4()).upper()

    # 脚本头部 - 定义常量
    lines.append("; Inno Setup Script")
    lines.append(f"; Generated for {app_name}")
    lines.append("; https://jrsoftware.org/isinfo.php")
    lines.append("")
    lines.append(f'#define MyAppName "{app_name}"')
    lines.append(f'#define MyAppVersion "{version}"')
    if publisher:
        lines.append(f'#define MyAppPublisher "{publisher}"')
    if app_url:
        lines.append(f'#define MyAppURL "{app_url}"')
    lines.append(f'#define MyAppExeName "{exe_name}"')
    lines.append("")

    # [Setup] 部分
    lines.append("[Setup]")
    lines.append("; 应用程序唯一标识 (升级时保持一致)")
    lines.append(f"AppId={{{{{app_id}}}")
    lines.append("AppName={#MyAppName}")
    lines.append("AppVersion={#MyAppVersion}")
    lines.append("AppVerName={#MyAppName} {#MyAppVersion}")
    if publisher:
        lines.append("AppPublisher={#MyAppPublisher}")
        if app_url:
            lines.append("AppPublisherURL={#MyAppURL}")
            lines.append("AppSupportURL={#MyAppURL}")
            lines.append("AppUpdatesURL={#MyAppURL}")
    lines.append("")

    # 安装目录
    lines.append("; 安装目录")
    lines.append(f"DefaultDirName={install_dir}")
    if start_menu:
        lines.append("DefaultGroupName={#MyAppName}")
    else:
        lines.append("DisableProgramGroupPage=yes")
    lines.append("CreateAppDir=yes")
    lines.append("")

    # 输出设置
    lines.append("; 输出设置")
    lines.append(f"OutputDir={output_dir}")
    # 构建输出文件名：支持自定义后缀
    output_filename = f"{{#MyAppName}}_V{{#MyAppVersion}}_Setup{custom_suffix}"
    lines.append(f"OutputBaseFilename={output_filename}")
    if icon_file:
        lines.append(f"SetupIconFile={icon_file}")
    lines.append("")

    # 卸载设置
    lines.append("; 卸载设置")
    lines.append("UninstallDisplayIcon={app}\\{#MyAppExeName}")
    lines.append("UninstallDisplayName={#MyAppName}")
    lines.append("CloseApplications=yes")
    lines.append("RestartApplications=no")
    lines.append("")

    # 压缩设置
    lines.append("; 压缩设置")
    lines.append(f"Compression={compression}")
    lines.append("SolidCompression=yes")
    if "lzma" in compression:
        lines.append("LZMAUseSeparateProcess=yes")
        lines.append("InternalCompressLevel=max")
    lines.append("")

    # 安装权限
    lines.append("; 安装权限")
    if privileges == "dialog":
        lines.append("PrivilegesRequired=lowest")
        lines.append("PrivilegesRequiredOverridesAllowed=commandline dialog")
    elif privileges == "admin":
        lines.append("PrivilegesRequired=admin")
        lines.append("PrivilegesRequiredOverridesAllowed=commandline dialog")
    else:
        lines.append("PrivilegesRequired=lowest")
    lines.append("")

    # 界面设置
    lines.append("; 界面设置")
    lines.append("WizardStyle=modern")
    lines.append("WizardSizePercent=100")
    lines.append("")

    # 版本信息
    lines.append("; 版本信息")
    lines.append("VersionInfoVersion={#MyAppVersion}")
    if publisher:
        lines.append("VersionInfoCompany={#MyAppPublisher}")
    lines.append("VersionInfoProductName={#MyAppName}")
    lines.append("VersionInfoProductVersion={#MyAppVersion}")
    lines.append("VersionInfoDescription={#MyAppName} Setup")
    if publisher:
        lines.append(f"VersionInfoCopyright=Copyright (C) {publisher}")
    lines.append("")

    # 许可协议和自述文件
    if license_file:
        lines.append(f"LicenseFile={license_file}")
    if readme_file:
        lines.append(f"InfoBeforeFile={readme_file}")
    if license_file or readme_file:
        lines.append("")

    # [Languages] 部分
    lines.append("[Languages]")
    lines.append('Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"')
    lines.append("")

    # [Tasks] 部分
    lines.append("[Tasks]")
    if desktop_icon:
        lines.append(
            'Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked'
        )
    if add_path:
        if path_scope == "system":
            lines.append(
                'Name: "addtopath"; Description: "添加到系统 PATH 环境变量"; GroupDescription: "其他选项:"'
            )
        else:
            lines.append(
                'Name: "addtopath"; Description: "添加到用户 PATH 环境变量"; GroupDescription: "其他选项:"'
            )
    if not desktop_icon and not add_path:
        lines.append("; 无额外任务")
    lines.append("")

    # [Files] 部分
    lines.append("[Files]")
    lines.append(
        f'Source: "{source_dir}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs'
    )
    lines.append("")

    # [Icons] 部分
    lines.append("[Icons]")
    if start_menu:
        lines.append(
            'Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"'
        )
        lines.append(
            'Name: "{group}\\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"'
        )
    if desktop_icon:
        lines.append(
            'Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon'
        )

    # 额外快捷方式
    if extra_shortcuts:
        for shortcut in _split_items(extra_shortcuts):
            if ";" in shortcut:
                name, exe = shortcut.split(";", 1)
                name, exe = name.strip(), exe.strip()
                if name and exe:
                    if start_menu:
                        lines.append(
                            f'Name: "{{group}}\\{name}"; Filename: "{{app}}\\{exe}"'
                        )
                    if desktop_icon:
                        lines.append(
                            f'Name: "{{autodesktop}}\\{name}"; Filename: "{{app}}\\{exe}"; Tasks: desktopicon'
                        )

    if not start_menu and not desktop_icon and not extra_shortcuts:
        lines.append("; 不创建快捷方式")
    lines.append("")

    # [Run] 部分
    if run_after:
        lines.append("[Run]")
        lines.append(
            "Filename: \"{app}\\{#MyAppExeName}\"; Description: \"{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}\"; Flags: nowait postinstall skipifsilent shellexec"
        )
        lines.append("")

    # [Registry] 部分 - PATH 环境变量和文件关联
    has_registry = add_path or file_assoc
    if has_registry:
        lines.append("[Registry]")

        # PATH 环境变量
        if add_path:
            if path_scope == "system":
                lines.append("; 添加到系统 PATH (需要管理员权限)")
                lines.append(
                    'Root: HKLM; Subkey: "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Tasks: addtopath; Check: NeedsAddPath(\'{app}\')'
                )
            else:
                lines.append("; 添加到用户 PATH")
                lines.append(
                    'Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Tasks: addtopath; Check: NeedsAddPath(\'{app}\')'
                )

        # 文件关联
        if file_assoc:
            lines.append("; 文件类型关联")
            for ext in _split_items(file_assoc):
                ext_lower = ext.lstrip(".").lower()
                if not ext_lower:
                    continue
                lines.append(f"; .{ext_lower} 文件关联")
                lines.append(
                    f'Root: HKA; Subkey: "Software\\Classes\\.{ext_lower}"; ValueType: string; ValueName: ""; ValueData: "{{#MyAppName}}.{ext_lower}"; Flags: uninsdeletevalue'
                )
                lines.append(
                    f'Root: HKA; Subkey: "Software\\Classes\\{{#MyAppName}}.{ext_lower}"; ValueType: string; ValueName: ""; ValueData: "{{#MyAppName}} {ext_lower.upper()} File"; Flags: uninsdeletekey'
                )
                lines.append(
                    f'Root: HKA; Subkey: "Software\\Classes\\{{#MyAppName}}.{ext_lower}\\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{{app}}\\{{#MyAppExeName}},0"'
                )
                lines.append(
                    f'Root: HKA; Subkey: "Software\\Classes\\{{#MyAppName}}.{ext_lower}\\shell\\open\\command"; ValueType: string; ValueName: ""; ValueData: """{{app}}\\{{#MyAppExeName}}"" ""%1"""'
                )

        lines.append("")

    # [Code] 部分
    lines.append("[Code]")

    # 卸载旧版本函数
    if uninstall_old:
        lines.append("// 获取旧版本卸载程序路径")
        lines.append("function GetUninstallString(): String;")
        lines.append("var")
        lines.append("  sUnInstPath: String;")
        lines.append("  sUnInstallString: String;")
        lines.append("begin")
        lines.append(
            "  sUnInstPath := ExpandConstant('Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{#emit SetupSetting(\"AppId\")}_is1');"
        )
        lines.append("  sUnInstallString := '';")
        lines.append(
            "  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then"
        )
        lines.append(
            "    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);"
        )
        lines.append("  Result := sUnInstallString;")
        lines.append("end;")
        lines.append("")
        lines.append("// 检查是否已安装旧版本")
        lines.append("function IsUpgrade(): Boolean;")
        lines.append("begin")
        lines.append("  Result := (GetUninstallString() <> '');")
        lines.append("end;")
        lines.append("")
        lines.append("// 卸载旧版本")
        lines.append("function UnInstallOldVersion(): Integer;")
        lines.append("var")
        lines.append("  sUnInstallString: String;")
        lines.append("  iResultCode: Integer;")
        lines.append("begin")
        lines.append("  Result := 0;")
        lines.append("  sUnInstallString := GetUninstallString();")
        lines.append("  if sUnInstallString <> '' then begin")
        lines.append("    sUnInstallString := RemoveQuotes(sUnInstallString);")
        lines.append(
            "    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES', '', SW_HIDE, ewWaitUntilTerminated, iResultCode) then"
        )
        lines.append("      Result := 3")
        lines.append("    else")
        lines.append("      Result := 2;")
        lines.append("  end else")
        lines.append("    Result := 1;")
        lines.append("end;")
        lines.append("")
        lines.append("// 安装前检查并卸载旧版本")
        lines.append("procedure CurStepChanged(CurStep: TSetupStep);")
        lines.append("begin")
        lines.append("  if (CurStep = ssInstall) then")
        lines.append("  begin")
        lines.append("    if (IsUpgrade()) then")
        lines.append("      UnInstallOldVersion();")
        lines.append("  end;")
        lines.append("end;")
        lines.append("")

    # PATH 检查函数
    if add_path:
        lines.append("// 检查路径是否已在 PATH 中")
        lines.append("function NeedsAddPath(Param: string): boolean;")
        lines.append("var")
        lines.append("  OrigPath: string;")
        lines.append("begin")
        if path_scope == "system":
            lines.append(
                "  if not RegQueryStringValue(HKLM, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment', 'Path', OrigPath) then"
            )
        else:
            lines.append(
                "  if not RegQueryStringValue(HKCU, 'Environment', 'Path', OrigPath) then"
            )
        lines.append("  begin")
        lines.append("    Result := True;")
        lines.append("    exit;")
        lines.append("  end;")
        lines.append("  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;")
        lines.append("end;")
        lines.append("")

        # 卸载时清理 PATH
        lines.append("// 卸载时从 PATH 中移除")
        lines.append(
            "procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);"
        )
        lines.append("var")
        lines.append("  OrigPath, NewPath, AppPath: string;")
        lines.append("  P: Integer;")
        lines.append("begin")
        lines.append("  if CurUninstallStep = usUninstall then")
        lines.append("  begin")
        if path_scope == "system":
            lines.append(
                "    if RegQueryStringValue(HKLM, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment', 'Path', OrigPath) then"
            )
        else:
            lines.append(
                "    if RegQueryStringValue(HKCU, 'Environment', 'Path', OrigPath) then"
            )
        lines.append("    begin")
        lines.append("      AppPath := ExpandConstant('{app}');")
        lines.append("      NewPath := OrigPath;")
        lines.append("      P := Pos(';' + AppPath, NewPath);")
        lines.append("      if P > 0 then")
        lines.append("      begin")
        lines.append("        Delete(NewPath, P, Length(AppPath) + 1);")
        if path_scope == "system":
            lines.append(
                "        RegWriteStringValue(HKLM, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment', 'Path', NewPath);"
            )
        else:
            lines.append(
                "        RegWriteStringValue(HKCU, 'Environment', 'Path', NewPath);"
            )
        lines.append("      end;")
        lines.append("    end;")
        lines.append("  end;")
        lines.append("end;")
        lines.append("")
    else:
        lines.append("// 无额外代码")
        lines.append("")

    # [UninstallDelete] 部分
    lines.append("[UninstallDelete]")
    lines.append('Type: filesandordirs; Name: "{app}"')
    lines.append("")

    return "\n".join(lines)


def generate_installer_script(
    config: Dict[str, Any], project_dir: Path
) -> tuple[bool, str]:
    """
    生成安装包脚本
    返回 (是否成功, 消息)
    """
    try:
        # 处理 AppId：如果没有则生成（不带花括号存储）
        app_id = config.get("installer_appid", "").strip().strip("{}")
        if not app_id:
            app_id = str(uuid.uuid4()).upper()
            config["installer_appid"] = app_id
            # 立即保存 AppId 到配置文件
            from src.utils import save_build_config

            save_build_config(project_dir, config)

        # 目前只支持 Inno Setup
        script_content = generate_inno_setup_script(config, project_dir)

        app_name = config.get("installer_app_name", config.get("project_name", "MyApp"))
        script_name = f"{app_name}_setup.iss"

        # 保存脚本
        script_path = project_dir / script_name
        script_path.write_text(script_content, encoding="utf-8")

        # 生成使用说明
        usage_msg = f"""脚本已生成: {script_name}

AppId: {app_id}
(已保存到 build_config.yaml，后续版本请保持一致)

使用方法:
1. 安装 Inno Setup 6: https://jrsoftware.org/isinfo.php
2. 确保已编译好可执行文件到 {config.get("installer_source_dir", "build")} 目录
3. 使用 Inno Setup 编译器打开 {script_name}
4. 点击 Build -> Compile 生成安装包

或使用命令行:
iscc {script_name}"""

        return True, usage_msg

    except Exception as e:
        return False, f"生成脚本失败: {e}"
