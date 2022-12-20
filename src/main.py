print("[DFM] Loading....")

import utility
import sqlite3
import os
import dbmanage
import time

os.system("title DB MANAGER v1.0")

utility.clear()
utility.Title()

DB = None
Menu = True

print(f'\033[38;2;210;210;210mCurrent directory: \033[38;2;175;175;180m{os.getcwd()}')
print()
print('\033[38;2;100;100;100m[!] You can skip this by typing "MENU" or "SKIP".')
print('\033[38;2;100;100;100m[!] Skipping this part may cause errors and crashes.')
print()

while not DB:
    print("\033[38;2;255;255;255mInput DB file location.")
    DBFileLocation = input("> \033[38;2;0;255;0m")
    if DBFileLocation.replace(" ", "") == "":
        pass
    elif DBFileLocation.lower() in ["menu", "skip"]:
        DB = "skipped"
    elif not DBFileLocation.lower().endswith(".db"):
        print("\033[38;2;255;0;0m[!] File extension must be a database file (.db)")
    elif not os.path.exists(DBFileLocation):
        print("\033[38;2;255;0;0m[!] Invalid file location.")
    else:
        DB = sqlite3.connect(DBFileLocation)
    print()

while Menu:
    utility.clear()
    utility.Title()
    print("\033[38;2;255;255;255m", end="")
    print(f"Filename: [Coming soon]")
    print()
    print("[1] Create table    [4] Show table         [7] Delete all rows            ")
    print("[2] List tables     [5] Add a new column   [8] Delete a row      [0] Close")
    print("[3] Delete table    [6] Delete a column    [9] Insert a row               ")
    print()
    print("What do you wish to do?")
    Option = input("> \033[38;2;0;255;0m")
    if Option == "0":
        exit(0)
    if DB != "skipped":
        if Option == "1":
            dbmanage.CreateTable(DB.cursor())
        elif Option == "2":
            dbmanage.ShowTables(DB.cursor())
        elif Option == "3":
            dbmanage.DeleteTable(DB.cursor())
        elif Option == "4":
            dbmanage.ShowTableContent(DB.cursor())
        elif Option == "5":
            dbmanage.AddColumn(DB.cursor())
        elif Option == "6":
            dbmanage.DropColumn(DB.cursor())
        elif Option == "7":
            dbmanage.DeleteAllRows(DB.cursor(), DB=DB)
        elif Option == "8":
            dbmanage.DeleteRow(DB.cursor(), DB=DB)
        elif Option == "9":
            dbmanage.InsertRow(DB.cursor(), DB=DB)
        else:
            print("\033[38;2;255;0;0m[!] Invalid option.")
            print()
            time.sleep(3.0)
    else:
        print("\033[38;2;255;0;0m[!] You need to reopen software again and set file location.")
        print()
        time.sleep(3.0)
input()