@echo off
setlocal EnableExtensions

REM ==========================
REM Varroa Detector Installer
REM - Deletes previous conda env (if exists)
REM - Creates conda env from env.yaml
REM - Creates Desktop shortcut to launch the app
REM ==========================

set "SCRIPT_DIR=%~dp0"
set "ENV_FILE=%SCRIPT_DIR%env.yaml"

echo [INFO] Repository: %SCRIPT_DIR%
if not exist "%ENV_FILE%" (
  echo [ERR ] env.yaml not found at %ENV_FILE%
  goto :fail
)

REM ---- Locate conda ----
set "CONDA_BAT="
for /f "delims=" %%I in ('where conda 2^>nul') do (
  set "CONDA_BAT=%%~fI"
  goto :conda_found
)

set "c1=%USERPROFILE%\miniforge3\condabin\conda.bat"
set "c2=%USERPROFILE%\miniconda3\condabin\conda.bat"
set "c3=%USERPROFILE%\anaconda3\condabin\conda.bat"
set "c4=%ProgramData%\miniconda3\condabin\conda.bat"
set "c5=%ProgramData%\miniforge3\condabin\conda.bat"
for %%P in ("%c1%" "%c2%" "%c3%" "%c4%" "%c5%") do (
  if exist "%%~P" (
    set "CONDA_BAT=%%~P"
    goto :conda_found
  )
)

:conda_found
if not defined CONDA_BAT (
  echo [ERR ] Conda not found. Install Miniforge/Miniconda/Anaconda and add to PATH.
  goto :fail
)
echo [INFO] Using conda at: %CONDA_BAT%

REM ---- Extract env name from env.yaml (fallback varroa-env) ----
set "ENV_NAME="
for /f "usebackq delims=" %%E in (`powershell -NoProfile -Command "$yml = Get-Content -Raw -LiteralPath '%ENV_FILE%'; $m = [regex]::Match($yml, '(?m)^[\s-]*name\s*:\s*([^\r\n#]+)'); if($m.Success){ $m.Groups[1].Value.Trim() } else { 'varroa-env' }"`) do set "ENV_NAME=%%E"
if not defined ENV_NAME set "ENV_NAME=varroa-env"
echo [INFO] Target conda environment: %ENV_NAME%

REM ---- Delete previous environment (if exists) ----
echo [INFO] Removing previous environment (if any)...
powershell -NoProfile -Command "& { Start-Process -FilePath '%CONDA_BAT%' -ArgumentList @('env','remove','-n','%ENV_NAME%','--yes') -Wait }"

REM ---- Create new environment ----
echo [INFO] Creating environment from env.yaml...
powershell -NoProfile -Command "& { Start-Process -FilePath '%CONDA_BAT%' -ArgumentList @('env','create','-f','%ENV_FILE%') -Wait }"
if errorlevel 1 (
  echo [ERR ] Environment creation failed.
  goto :fail
)

REM ---- Choose app script ----
set "APP_SCRIPT="
if exist "%SCRIPT_DIR%modern_ui_app.py" set "APP_SCRIPT=%SCRIPT_DIR%modern_ui_app.py"
if not defined APP_SCRIPT if exist "%SCRIPT_DIR%modern_gui_app.py" set "APP_SCRIPT=%SCRIPT_DIR%modern_gui_app.py"
if not defined APP_SCRIPT (
  echo [ERR ] Neither modern_ui_app.py nor modern_gui_app.py found in repo root.
  goto :fail
)
echo [INFO] App script: %APP_SCRIPT%

REM ---- Resolve Desktop path ----
set "DESKTOP="
for /f "usebackq delims=" %%D in (`powershell -NoProfile -Command "[Environment]::GetFolderPath('Desktop')"`) do set "DESKTOP=%%D"
if not defined DESKTOP set "DESKTOP=%USERPROFILE%\Desktop"
if not exist "%DESKTOP%" (
  echo [ERR ] Desktop folder not found.
  goto :fail
)

set "SHORTCUT=%DESKTOP%\Varroa Detector.lnk"
set "ICON_PATH=%SCRIPT_DIR%app\icons\honeycomb_logo_transparent.ico"
echo [INFO] Creating desktop shortcut: %SHORTCUT%

REM ---- Create shortcut via VBScript ----
set "_VBS=%TEMP%\mk_varroa_link_%RANDOM%.vbs"
> "%_VBS%" echo Set oWS = CreateObject("WScript.Shell")
>>"%_VBS%" echo sLink = "%SHORTCUT%"
>>"%_VBS%" echo Set oLnk = oWS.CreateShortcut(sLink)
>>"%_VBS%" echo oLnk.TargetPath = "%CONDA_BAT%"
>>"%_VBS%" echo oLnk.Arguments = "run -n %ENV_NAME% pythonw ""%APP_SCRIPT%"""
>>"%_VBS%" echo oLnk.WorkingDirectory = "%SCRIPT_DIR%"
>>"%_VBS%" echo oLnk.WindowStyle = 7
>>"%_VBS%" echo oLnk.Description = "Launch Varroa Detector"
>>"%_VBS%" echo If CreateObject("Scripting.FileSystemObject").FileExists("%ICON_PATH%") Then
>>"%_VBS%" echo   oLnk.IconLocation = "%ICON_PATH%"
>>"%_VBS%" echo End If
>>"%_VBS%" echo oLnk.Save
cscript //nologo "%_VBS%"
del /q "%_VBS%" >nul 2>&1

echo.
echo [OK  ] Installation complete!
echo [OK  ] - Conda environment: %ENV_NAME%
echo [OK  ] - Shortcut created at: %SHORTCUT%
echo.
echo You can now double-click the desktop shortcut to start the app.
goto :eof

:fail
echo.
echo Installation failed. See messages above.
exit /b 1
