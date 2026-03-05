import os
import json
from collections import defaultdict
from pathlib import Path
import win32com.client  # Library native Windows untuk explorer yang lebih ringan

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
    try:
        history = {
            "extension_map": data,
            "last_new_extension": new_ext
        }
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f)
    except Exception:
        pass

def load_history():
    """Memuat riwayat dari file JSON jika ada"""
    h_path = Path(HISTORY_FILE)
    if h_path.exists():
        try:
            with open(h_path, "r") as f:
                history = json.load(f)
                return history.get("extension_map", {}), history.get("last_new_extension", "")
        except (json.JSONDecodeError, IOError):
            return {}, ""
    return {}, ""

# =========================
# GLOBAL STORAGE (LOAD FROM HISTORY)
# =========================

last_extension_map, last_new_extension = load_history()

# =========================
# UI UTILITIES
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

def print_total_folder_summary(root_path):
    """Menghitung total file berdasarkan ekstensi secara efisien"""
    counter = defaultdict(int)
    total_files = 0
    # Menggunakan rglob agar pemindaian lebih cepat dan modern
    for p in Path(root_path).rglob('*'):
        if p.is_file():
            total_files += 1
            ext = p.suffix.lower().replace(".", "") if p.suffix else "no_extension"
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
    """Membuka folder explorer menggunakan Windows Shell (Native & Ringan)"""
    print("Open file explorer - wait...")
    try:
        shell = win32com.client.Dispatch("Shell.Application")
        # Parameter: (Hwnd, Title, Options, RootFolder)
        folder = shell.BrowseForFolder(0, "Select Folder Target", 0, 0)
        if folder:
            return folder.Self.Path
        return None
    except Exception:
        # Jika win32com gagal, fallback ke input manual agar program tidak mati
        path_input = input(f"\n{YELLOW}Paste folder path manual:{RESET} ").strip().strip('"')
        return path_input if os.path.isdir(path_input) else None

def scan_files(root_path, extensions):
    """Mencari file berdasarkan list ekstensi"""
    root = Path(root_path)
    matched = []
    for ext in extensions:
        # Scan hanya file dengan ekstensi yang diminta
        matched.extend(root.rglob(f"*.{ext}"))
    return matched

# =========================
# ADVANCED LOGIC
# =========================

def advanced():
    global last_extension_map, last_new_extension
    choice = advanced_menu()
    if choice == 0: return

    folder_str = pick_folder()
    if not folder_str:
        print("Folder not select.")
        input("Press Enter to return...")
        advanced()
        return

    print_total_folder_summary(folder_str)
    print(f"\nTarget Folder:\n{YELLOW}{folder_str}{RESET}\n")

    if choice == 1:
        old_ext = input("Enter extensions single or multi to changes (example: dll txt dat): ").strip()
        # Membersihkan input ekstensi
        extensions = [e.lower().replace(".", "") for e in old_ext.replace(",", " ").split()]
        new_ext = input("Enter new extension (without dot): ").strip().replace(".", "")
        
        files = scan_files(folder_str, extensions)

        if not files:
            print(f"{RED}Extensions not found.{RESET}")
        else:
            print("\nScanning extensions - wait...\nProcessing...")
            total = 0
            changed_ext = set()
            last_extension_map = {}

            for file_path in files:
                try:
                    new_file = file_path.with_suffix(f".{new_ext}")
                    # Cek agar tidak menimpa file yang sudah ada
                    if not new_file.exists():
                        old_extension_clean = file_path.suffix.lower().replace(".", "")
                        file_path.rename(new_file)
                        last_extension_map[str(new_file)] = old_extension_clean
                        changed_ext.add(old_extension_clean)
                        total += 1
                except Exception:
                    continue

            last_new_extension = new_ext
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
            for file_str, original_ext in last_extension_map.items():
                file_path = Path(file_str)
                if file_path.exists():
                    try:
                        restored_file = file_path.with_suffix(f".{original_ext}")
                        if not restored_file.exists():
                            file_path.rename(restored_file)
                            restored_ext.add(original_ext)
                            total += 1
                    except Exception:
                        continue

            print("Done.\n")
            print(f"Total files changes: {total}")
            for ext in sorted(restored_ext):
                print(f"Restored {GREEN}[.{last_new_extension}]{RESET} to {GREEN}[.{ext}]{RESET}")
            print(f"\nStatus: {GREEN}RESTORE SUCCESS{RESET}")
            
            # Reset history setelah restore berhasil
            last_extension_map.clear()
            h_file = Path(HISTORY_FILE)
            if h_file.exists():
                try: h_file.unlink()
                except: pass

    input("\nPress Enter to return to Advanced Menu...")
    advanced()

# =========================
# MAIN LOGIC
# =========================

def main():
    choice = menu()
    if choice == 0: return
    if choice == 3:
        advanced()
        main()
        return

    folder_str = pick_folder()
    if not folder_str:
        print(f"{RED}Folder not select.{RESET}")
        input("Press Enter to return to menu...")
        main()
        return

    print_total_folder_summary(folder_str)
    print(f"\nTarget Folder:\n{YELLOW}{folder_str}{RESET}\n")

    if choice == 1:
        ext_input = input("Enter extensions single or multi to changes (example: dll txt dat): ").strip()
        extensions = [e.lower().replace(".", "") for e in ext_input.replace(",", " ").split()]
        files = scan_files(folder_str, extensions)
        
        if not files:
            print(f"{RED}Extensions not found.{RESET}")
        else:
            print("\nScanning extensions - wait...\nProcessing...")
            total = 0
            changed_ext = set()
            for file_path in files:
                try:
                    new_path = Path(str(file_path) + ".bak")
                    if not new_path.exists():
                        ext = file_path.suffix.lower().replace(".", "")
                        file_path.rename(new_path)
                        changed_ext.add(ext)
                        total += 1
                except Exception:
                    continue
            print("Done.\n")
            print(f"Total files changes: {total}")
            for ext in sorted(changed_ext):
                print(f"Changed {GREEN}[.{ext}]{RESET} to {GREEN}[.bak]{RESET}")
            print(f"\nStatus: {GREEN}CHANGE SUCCESS{RESET}")

    elif choice == 2:
        print("\nScanning extensions - wait...\nProcessing...")
        total = 0
        restored_ext = set()
        # Scan khusus file .bak untuk efisiensi
        for bak_file in Path(folder_str).rglob("*.bak"):
            try:
                # Mengembalikan nama file sebelum .bak
                original_path = bak_file.with_name(bak_file.name[:-4])
                if not original_path.exists():
                    if original_path.suffix:
                        restored_ext.add(original_path.suffix.lower().replace(".", ""))
                    bak_file.rename(original_path)
                    total += 1
            except Exception:
                continue
                
        print("Done.\n")
        print(f"Total files changes: {total}")
        for ext in sorted(restored_ext):
            print(f"Restored {GREEN}[.bak]{RESET} to {GREEN}[.{ext}]{RESET}")
        print(f"\nStatus: {GREEN}RESTORE SUCCESS{RESET}")

    input("\nPress Enter to return to menu...")
    main()

if __name__ == "__main__":
    main()