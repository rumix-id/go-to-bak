@echo off
Compile to Exe - Rumix Tools
echo Starting the compilation process for gtb-renamer.py...
echo Please wait, this process may take a few minutes.
echo

pyinstaller --noconfirm --onefile --console ^
    --upx-dir="%CD%\upx" ^
    --icon="icon.ico" ^
    --version-file="version.txt" ^
    --name "go-to-bak" ^
    --clean ^
    gtb-renamer.py

echo.
echo Compilation Complete! Check the gtb-renamer.exe file.
pause