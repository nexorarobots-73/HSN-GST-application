[Setup]
AppName=HSN Tax Calculator
AppVersion=1.0
DefaultDirName={pf}\HSN Tax Calculator
DefaultGroupName=HSN Tax Calculator
OutputDir=output
OutputBaseFilename=HSN_Tax_Calculator_Setup

[Files]
Source: "dist\HSN_Tax_Calculator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\HSN Tax Calculator"; Filename: "{app}\HSN_Tax_Calculator.exe"
Name: "{commondesktop}\HSN Tax Calculator"; Filename: "{app}\HSN_Tax_Calculator.exe"