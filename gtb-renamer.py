import os
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict
import json  # Tambahan untuk menangani file history

GREEN = "\033[92m"
RED = "\033[91m"
REDF = "\033[101m"
RESET = "\033[0m"
YELLOW = "\033[93m"

# File untuk menyimpan riwayat
HISTORY_FILE = "history.json"

# =========================
# HISTORY UTILITIES
# =========================

def save_history(data, new_ext):
    """Menyimpan map ekstensi ke file JSON"""
    history = {
        "extension_map": data,
        "last_new_extension": new_ext
    }
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def load_history():
    """Memuat riwayat dari file JSON jika ada"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
                return history.get("extension_map", {}), history.get("last_new_extension", "")
        except:
            return {}, ""
    return {}, ""

# =========================
# GLOBAL STORAGE (LOAD FROM HISTORY)
# =========================

# Mengisi data global saat program dijalankan
last_extension_map, last_new_extension = load_history()

# =========================
# UI UTILITIES (TETAP SAMA)
# =========================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(r"""
  ____         _            _           _    
 / ___| ___   | |_ ___     | |__   __ _| | __
| |  _ / _ \  | __/ _ \    | '_ \ / _` | |/ /
| |_| | (_) | | || (_) |  _| |_) | (_| |   < 
 \____|\___/   \__\___/  (_)_.__/ \__,_|_|\_\

     Go To .BAK File Utility by Rumix-id
----------------------------------------------
    Change & Restore Multi Extension Files
    """)

# ... (Fungsi print_total_folder_summary, menu, advanced_menu, pick_folder, scan_files tetap sama) ...

def print_total_folder_summary(root_path):
    counter = defaultdict(int)
    total_files = 0
    for root, dirs, files in os.walk(root_path):
        for file in files:
            total_files += 1
            if "." in file:
                ext = file.rsplit(".", 1)[-1].lower()
            else:
                ext = "no_extension"
            counter[ext] += 1
    print(f"Total Files: {total_files}")
    print("\n===========================================")
    print("Total File In Folder")
    print("===========================================")
    print(f"{'No':<5}| {'Extensions':<20}| {'Count'}")
    print("===========================================")
    for i, (ext, count) in enumerate(sorted(counter.items()), start=1):
        print(f"{i:<5}| {ext:<20}| {count}")

def menu():
    clear()
    banner()
    print("1. Change Extensions to .bak")
    print("2. Restore .bak to Original")
    print("3. Advanced Menu\n")
    print("00. Exit\n")
    while True:
        choice = input("Select options (1/2/3/00): ").strip()
        if choice in ["1", "2", "3"]:
            return int(choice)
        elif choice == "00":
            return 0
        else:
            print(f"{REDF}Input not valid.{RESET}")

def advanced_menu():
    clear()
    banner()
    print("#ADVANCED MENU")
    print("1. Change Any Extension")
    print("2. Restore Custom Extension (Auto)")
    print("00. Back to Main Menu\n")
    while True:
        choice = input("Select options (1/2/00): ").strip()
        if choice in ["1", "2"]:
            return int(choice)
        elif choice == "00":
            return 0
        else:
            print(f"{REDF}Input not valid.{RESET}")

def pick_folder():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder = filedialog.askdirectory(title="Select Folder Target")
    root.destroy()
    return folder

def scan_files(root_path, extensions):
    matched = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if "." in file:
                ext = file.rsplit(".", 1)[-1].lower()
                if ext in extensions:
                    matched.append(os.path.join(root, file))
    return matched

# =========================
# ADVANCED LOGIC (MODIFIED TO SAVE HISTORY)
# =========================

def advanced():
    global last_extension_map, last_new_extension
    choice = advanced_menu()
    if choice == 0: return

    print("Open file explorer - wait...")
    folder = pick_folder()
    if not folder:
        print("Folder not select.")
        input("Press Enter to return...")
        advanced()
        return

    print_total_folder_summary(folder)
    print(f"\nTarget Folder:\n{YELLOW}{folder}{RESET}\n")

    if choice == 1:
        old_ext = input("Enter extensions single or multi to changes (example: dll txt dat): ").strip()
        extensions = [e.lower().replace(".", "") for e in old_ext.replace(",", " ").split()]
        new_ext = input("Enter new extension (without dot): ").strip().replace(".", "")
        files = scan_files(folder, extensions)

        if not files:
            print(f"{RED}Extensions not found.{RESET}")
        else:
            print("\nScanning extensions - wait...\nProcessing...")
            total = 0
            changed_ext = set()
            last_extension_map = {}

            for file in files:
                old_extension = file.rsplit(".", 1)[-1].lower()
                base = file.rsplit(".", 1)[0]
                new_file = base + "." + new_ext
                os.rename(file, new_file)
                last_extension_map[new_file] = old_extension
                changed_ext.add(old_extension)
                total += 1

            last_new_extension = new_ext
            # Simpan ke file agar tidak hilang saat aplikasi ditutup
            save_history(last_extension_map, last_new_extension)

            print("Done.\n")
            print(f"Total files changes: {total}")
            for ext in sorted(changed_ext):
                print(f"Changed {GREEN}[.{ext}]{RESET} to {GREEN}[.{new_ext}]{RESET}")
            print(f"\nStatus: {GREEN}CHANGE SUCCESS{RESET}")

    elif choice == 2:
        if not last_extension_map:
            print(f"{RED}Data not found to restore.{RESET}")
        else:
            print("\nScanning extensions - wait...\nProcessing...")
            total = 0
            restored_ext = set()
            for file_path, original_ext in last_extension_map.items():
                if os.path.exists(file_path):
                    base = file_path.rsplit(".", 1)[0]
                    restored_file = base + "." + original_ext
                    os.rename(file_path, restored_file)
                    restored_ext.add(original_ext)
                    total += 1

            print("Done.\n")
            print(f"Total files changes: {total}")
            for ext in sorted(restored_ext):
                print(f"Restored {GREEN}[.{last_new_extension}]{RESET} to {GREEN}[.{ext}]{RESET}")
            print(f"\nStatus: {GREEN}RESTORE SUCCESS{RESET}")
            
            # Hapus history setelah berhasil restore
            last_extension_map.clear()
            if os.path.exists(HISTORY_FILE): os.remove(HISTORY_FILE)

    input("\nPress Enter to return to Advanced Menu...")
    advanced()

# ... (Fungsi main tetap sama) ...

def main():
    choice = menu()
    if choice == 0: return
    if choice == 3:
        advanced()
        main()
        return

    print("\nOpen file explorer - wait...")
    folder = pick_folder()
    if not folder:
        print(f"{RED}Folder not select.{RESET}")
        input("Press Enter to return to menu...")
        main()
        return

    print_total_folder_summary(folder)
    print(f"\nTarget Folder:\n{YELLOW}{folder}{RESET}\n")

    if choice == 1:
        ext_input = input("Enter extensions single or multi to changes (example: dll txt dat): ").strip()
        extensions = [e.lower().replace(".", "") for e in ext_input.replace(",", " ").split()]
        files = scan_files(folder, extensions)
        if not files:
            print(f"{RED}Extensions not found.{RESET}")
        else:
            print("\nScanning extensions - wait...\nProcessing...")
            total = 0
            changed_ext = set()
            for file in files:
                ext = file.rsplit(".", 1)[-1].lower()
                os.rename(file, file + ".bak")
                changed_ext.add(ext)
                total += 1
            print("Done.\n")
            print(f"Total files changes: {total}")
            for ext in sorted(changed_ext):
                print(f"Changed {GREEN}[.{ext}]{RESET} to {GREEN}[.bak]{RESET}")
            print(f"\nStatus: {GREEN}CHANGE SUCCESS{RESET}")

    elif choice == 2:
        print("\nScanning extensions - wait...\nProcessing...")
        total = 0
        restored_ext = set()
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".bak"):
                    full = os.path.join(root, file)
                    original = file[:-4]
                    if "." in original:
                        ext = original.rsplit(".", 1)[-1].lower()
                        restored_ext.add(ext)
                    os.rename(full, os.path.join(root, original))
                    total += 1
        print("Done.\n")
        print(f"Total files changes: {total}")
        for ext in sorted(restored_ext):
            print(f"Restored {GREEN}[.bak]{RESET} to {GREEN}[.{ext}]{RESET}")
        print(f"\nStatus: {GREEN}RESTORE SUCCESS{RESET}")

    input("\nPress Enter to return to menu...")
    main()

if __name__ == "__main__":
    main()