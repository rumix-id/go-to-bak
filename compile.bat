@echo off
title Nuitka Compiler - Rumix Tools
echo Starting the compilation process for gtb-renamer.py...
echo Please wait, this process may take a few minutes.
echo

python -m nuitka ^
    --standalone ^
    --onefile ^
    --enable-plugin=tk-inter ^
    --enable-plugin=upx ^
    --upx-binary="%CD%\upx\upx.exe" ^
    --windows-icon-from-ico="icon.ico" ^
    --windows-company-name="Rumix Tools" ^
    --windows-file-description="Go To BAK File Utility" ^
    --windows-file-version="2.0.0" ^
    --windows-product-name="Extension Utility" ^
    --windows-product-version="2.0.0" ^
    --remove-output ^
    --assume-yes-for-downloads ^
    gtb-renamer.py

echo.
echo Compilation Complete! Check the gtb-renamer.exe file.
pause