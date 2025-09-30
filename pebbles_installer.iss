[Setup]
AppName=Pebbles
AppVersion=1.0
DefaultDirName=C:\Pebbles
UninstallDisplayIcon={app}\pebbles.exe
OutputDir=output
OutputBaseFilename=pebbles_installer
PrivilegesRequired=admin

[Files]
Source: "dist\pebbles.exe"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "{app}\pebbles.exe"; Description: "Run Pebbles"; Flags: nowait postinstall skipifsilent

[Registry]
[Registry]
; Add install folder (C:\Pebbles) to PATH
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};C:\Pebbles"; Flags: preservestringtype

; Set MAIN_PEBBLES_PATH environment variable
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "MAIN_PEBBLES_PATH"; ValueData: "C:\Pebbles"; Flags: preservestringtype
