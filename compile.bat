@echo off
title Nuitka Compiler - Rumix Tools
echo Memulai proses kompilasi gtb-renamer.py...
echo Harap tunggu, proses ini memakan waktu beberapa menit.
echo.

python -m nuitka ^
    --standalone ^
    --onefile ^
    --enable-plugin=tk-inter ^
    --enable-plugin=upx ^
    --upx-binary="%CD%\upx\upx.exe" ^
    --windows-icon-from-ico="icon.ico" ^
    --windows-company-name="Rumix Tools" ^
    --windows-file-description="Go To BAK File Utility" ^
    --windows-file-version="1.0.0" ^
    --windows-product-name="Extension Utility" ^
    --windows-product-version="1.0.0" ^
    --remove-output ^
    --assume-yes-for-downloads ^
    gtb-renamer.py

echo.
echo Kompilasi Selesai! Cek file gtb-renamer.exe
pause