; Inno Setup Script
; Generated for PyBuilder
; https://jrsoftware.org/isinfo.php

#define MyAppName "PyBuilder"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "ASLant"
#define MyAppExeName "PyBuilder.exe"

[Setup]
; 应用程序唯一标识 (升级时保持一致)
AppId={{3570A6C9-D68D-41D0-A6A0-4C3E3E4F8ECF}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}

; 安装目录
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
CreateAppDir=yes

; 输出设置
OutputDir=dist/installer
OutputBaseFilename={#MyAppName}_V{#MyAppVersion}_Setup
SetupIconFile=assets/app.ico

; 卸载设置
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
CloseApplications=yes
RestartApplications=no

; 压缩设置
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
InternalCompressLevel=max

; 安装权限
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=commandline dialog

; 界面设置
WizardStyle=modern
WizardSizePercent=100

; 版本信息
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoDescription={#MyAppName} Setup
VersionInfoCopyright=Copyright (C) ASLant

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "build\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent shellexec

[Code]
// 无额外代码

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
