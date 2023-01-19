print("[DM] Loading....")

import utility
import sqlite3
import os
import dbmanage
import time
import MetaData
import Config
import version
import colors

if not Config.CheckFileExistence():
    Config.CreateConfigFile()

os.system(f"title DB MANAGER {version.version}")

utility.clear()
utility.Title()

try:
    import requests

    DoWeCheckUpdates = Config.Getconfig("Updates", "check-for-updates")

    if DoWeCheckUpdates == None:
        InSettingCheckUpdateConfig = True
        while InSettingCheckUpdateConfig:
            print()
            print(f"{colors.fcolor(255, 255, 255)}[!] Do you want to check for updates everytime you run this software?")
            print("[!] Accepted answers: yes, y, no, n")
            ShouldWeCheckForUpdates = input(f"> {colors.fcolor(0, 255, 0)}")
            if ShouldWeCheckForUpdates.lower().replace(" ", "") in ["yes", "y"]:
                Config.Setconfig("Updates", "check-for-updates", str(True))
                DoWeCheckUpdates = True
                InSettingCheckUpdateConfig = False
            elif ShouldWeCheckForUpdates.lower().replace(" ", "") in ["no", "n"]:
                Config.Setconfig("Updates", "check-for-updates", str(False))
                DoWeCheckUpdates = False
                InSettingCheckUpdateConfig = False
            else:
                print(f"{colors.fcolor(255, 0, 0)}[!] Invalid option.")
        utility.clear()
        utility.Title()
    if bool(DoWeCheckUpdates) == True:
        try:
            LatestReleaseData = requests.get(f"https://api.github.com/repos/yasserprogamer/DBManager/releases/latest").json()
            if LatestReleaseData["tag_name"] > version.version:
                print(f"{colors.fcolor(255, 255, 0)}[!] New {LatestReleaseData['tag_name']} update! Download now: {LatestReleaseData['html_url']}")
                print("")
                input(f"{colors.fcolor(255, 255, 255)}Press ENTER to continue ")
                utility.clear()
                utility.Title()
        except requests.exceptions.ConnectionError:
            pass
    else:
        pass
except ImportError:
    print("[!] Missing python module: requests. You won't receive any updates anymore.")

DB = None
Menu = True

print("")
print(f'{colors.fcolor(210, 210, 210)}Current directory: {colors.fcolor(175, 175, 180)}{os.getcwd()}')
print()
print(f'{colors.fcolor(100, 100, 100)}[!] You can skip this by typing "MENU" or "SKIP".')
print(f'{colors.fcolor(100, 100, 100)}[!] Skipping this part may cause errors and crashes.')
print()

while not DB:
    print(f"{colors.fcolor(255, 255, 255)}Input DB file location.")
    DBFileLocation = input(f"> {colors.fcolor(0, 255, 0)}")
    if DBFileLocation.replace(" ", "") == "":
        pass
    elif DBFileLocation.lower() in ["menu", "skip"]:
        DB = "skipped"
    elif DBFileLocation.lower() in ["exit", "leave"]:
        exit(0)
    elif not DBFileLocation.lower().endswith(".db"):
        print(f"{colors.fcolor(255, 0, 0)}[!] File extension must be a database file (.db)")
    elif not os.path.exists(DBFileLocation):
        print(f"{colors.fcolor(255, 0, 0)}[!] Invalid file location.")
    else:
        MetaData.FileLocation = DBFileLocation
        SplitFileLocation = "\\".join(DBFileLocation.split("/")).split("\\")
        MetaData.Filename = SplitFileLocation[len(SplitFileLocation)-1]
        DB = sqlite3.connect(DBFileLocation)
    print()

while Menu:
    utility.clear()
    utility.Title()
    print(f"{colors.fcolor(255, 255, 255)}", end="")
    print(f"Filename: {MetaData.Filename}")
    print()
    print("[1] Create table    [4] Show table         [7] Delete all rows   [10] DB to CSV")
    print("[2] List tables     [5] Add a new column   [8] Delete a row      [0] Close     ")
    print("[3] Delete table    [6] Delete a column    [9] Insert a row                    ")
    print()
    print("What do you wish to do?")
    Option = input(f"> {colors.fcolor(0, 255, 0)}")
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
        elif Option == "10":
            dbmanage.DBToCSV(DB.cursor())
        else:
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid option.")
            print()
            time.sleep(3.0)
    else:
        print(f"{colors.fcolor(255, 0, 0)}[!] You need to reopen software again and set file location.")
        print()
        time.sleep(3.0)
input()