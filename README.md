# 🛠️ GTB Renamer - Extension Utility

Go To Bak Renamer is a CLI (Command Line Interface)-based tool designed to quickly change file extensions and restore them to their original format. It's especially useful for temporary file management or securing data using the `.bak` extension.


## ✨ Key Features

* **Bulk Change to .bak**: Converts all files with a specific extension to `.bak` in a folder and subfolders.
* **Auto Restore .bak**: Automatically restores files ending in `.bak` to their original extensions.
* **Advanced Menu**: Custom feature to change any extension to another extension of your choice.
* **Persistent History**: Remembers the history of recent changes using the `history.json` file so you can restore them even after the application has been closed.
* **Folder Summary**: Displays a summary of the number and type of file extensions contained in a folder before processing.


## 🚀 Line Method (Source Code)

1. Make sure you have Python 3.x installed.
2. Run the following command in the terminal to run the script:

```bash
python gtb-renamer.py
```

## 🛠️ How to Compile to .exe (Nuitka)

If you want to create a single executable file that is small in size and has Windows metadata:

## 1. Install Nuitka
Open a terminal and run:
```python
pip install nuitka
```
## 2.Install Library
```python
pip install pywin32
```
## 3. Compiler Preparation
Make sure you have the MinGW64/GCC and UPX compilers installed on your system to minimize the maximum file size.
## 4. Download UPX
[Download upx](https://upx.github.io/), then create a folder according to the given structure with the name upx, not anything else.
## 5. Run the Compilation
Simply double-click the compile.bat file in this folder. The compiled file will appear as gtb-renamer.exe.

### 📂 Folder Structure

```text
.
├── icon.ico       # Application icon for .exe files
├── compile.bat    # Batch script for automatic compilation
├── gtb-renamer.py # Main application script
├── upx            # The upx folder should be placed here
├── version.txt    # Application metadata (Company, Version, etc.)
└── README.md      # Project documentation
