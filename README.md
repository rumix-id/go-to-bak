# GTB Renamer - Extension Utility

GTB Renamer is a CLI (Command Line Interface)-based tool designed to easily change file extensions and restore them to their original format. This tool is especially useful for developers or users who frequently require the protection of temporary files using the `.bak` extension.

## ⚙️ Key Features

* **Bulk Change to .bak**: Converts all files with a specific extension to `.bak` in a folder (including subfolders).
* **Auto Restore .bak**: Automatically restores `.bak` files to their original extensions.
* **Advanced Menu**: Custom feature to change any extension to another extension of your choice.
* **Persistent History**: Remembers the history of recent changes using the `history.json` file so you can restore even after the application has been closed.
* **Folder Summary**: Displays a summary of the number and type of file extensions contained in a folder before processing.

## 🚀 Line Method (Source Code)

1. Make sure you have Python 3.x installed.
2. Run the following command to run the script:
``` bash
python gtb-renamer.py
