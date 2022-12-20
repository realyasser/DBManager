import sqlite3
import utility

def CreateTable(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    InSettingNewTableName = True
    while InSettingNewTableName:
        print()
        print("\033[38;2;255;255;255mSet a name for the new table.")
        NewTableName = input("> \033[38;2;0;255;0m")
        TableInfo = cursor.execute(f"PRAGMA table_info({NewTableName});").fetchall()
        if NewTableName.replace(" ", "") == "":
            print("\033[38;2;255;0;0m[!] Invalid table name.")
        elif len(TableInfo) > 0:
            print("\033[38;2;255;0;0m[!] Table already exists.")
        else:
            InSettingNewTableName = False
    InSettingColumnsNumber = True
    while InSettingColumnsNumber:
        print()
        print("\033[38;2;255;255;255mHow many columns do you want?")
        NumberOfColumns = input("> \033[38;2;0;255;0m")
        IsInteger = False
        try:
            if int(NumberOfColumns):
                IsInteger = True
        except:
            IsInteger = False
        if NumberOfColumns.replace(" ", "") == "":
            print("\033[38;2;255;0;0m[!] Please input an integer.")
        elif not IsInteger:
            print("\033[38;2;255;0;0m[!] Invalid integer.")
        else:
            InSettingColumnsNumber = False
    NumberOfColumns = int(NumberOfColumns)
    Types = ["int", "string", "date"]
    print()
    print("\033[38;2;211;211;211mAvailable data types:")
    print(", ".join(Types))
    ColumnsList = []
    for n in range(NumberOfColumns):
        InAddingNewColumnName = True
        while InAddingNewColumnName:
            print()
            print(f"\033[38;2;255;255;255m{n+1} | Column name:")
            ColumnName = input("> \033[38;2;0;255;0m")
            if ColumnName.replace(" ", "") == "":
                print("\033[38;2;255;0;0m[!] Empty column name.")
            else:
                InAddingNewColumnName = False
        InSettingColumnType = True
        while InSettingColumnType:
            print()
            print(f"\033[38;2;255;255;255m{n+1} | Column data type:")
            ColumnType = input("> \033[38;2;0;255;0m")
            if ColumnType.replace(" ", "") == "":
                print("\033[38;2;255;0;0m[!] Invalid data type.")
            elif not ColumnType.lower().replace(" ", "") in Types:
                print("\033[38;2;255;0;0m[!] Invalid data type.")
            else:
                InSettingColumnType = False
        ColumnsList.append(f"{ColumnName} {ColumnType}")
    cursor.execute(f"CREATE TABLE {NewTableName} ({', '.join(ColumnsList)});")
    print()
    print(f"\033[38;2;0;255;0m[+] Created a new table with name \"{NewTableName}\" successfully.")
    print()
    input("\033[37;1mPress ENTER to back to the menu ")
    return

def ShowTables(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    Results = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;")
    TablesList = Results.fetchall()
    Length = len(TablesList)
    if Length != 0:
        print("\033[38;2;255;255;255mTables that are in this database file:\n\033[38;2;0;255;0m")
        for Table in TablesList:
            print(f"[+] {Table[0]}")
    else:
        print("\033[37;1mNo tables are in this database file.")
    print()
    input("\033[37;1mPress ENTER to back to the menu ")
    return

def ListTables(cursor: sqlite3.Cursor):
    Results = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;")
    TablesList = Results.fetchall()
    if len(TablesList) == 0:
        print()
        print("\033[38;2;218;218;218mThere are no tables in this database file.")
    else:
        print("\033[38;2;218;218;218m")
        print("Available tables:")
        tables = ""
        for table in TablesList:
            tables += f"{table[0]}, "
        print(tables)
    return

def InsertRow(cursor: sqlite3.Cursor, DB: sqlite3.Connection):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InSelectingTable = True
    while InSelectingTable:
        print()
        print("\033[38;2;255;255;255mSelect a table.")
        TableName = input("> \033[38;2;0;255;0m")
        try:
            TableInfo = cursor.execute(f"PRAGMA table_info({TableName});").fetchall()
        except:
            TableInfo = []
        Size = len(TableInfo)
        if TableName.replace(" ", "") == "":
            print("\033[38;2;255;0;0m[!] Invalid table name.")
        elif Size == 0:
            print("\033[38;2;255;0;0m[!] Invalid table.")
        else:
            InSelectingTable = False
    ValuesQuestionMark = []
    Values = []
    for n in range(Size):
        ValuesQuestionMark.append("?")
        InInsertingValue = True
        while InInsertingValue:
            Pass = False
            print()
            TheValue = input(f"\033[38;2;255;255;255m[Type: {TableInfo[n][2]}] {TableInfo[n][1]}: \033[38;2;0;255;0m")
            if str(TableInfo[n][2]).lower() != "int":
                Pass = True
            else:
                try:
                    if int(TheValue):
                        TheValue = int(TheValue)
                        Pass = True
                except:
                    print("\033[38;2;255;0;0m[!] Invalid integer.")
                    Pass = False
            if Pass:
                Values.append(TheValue)
                InInsertingValue = False
    cursor.execute(f"INSERT INTO {TableName} VALUES ({', '.join(ValuesQuestionMark)});", tuple(Values))
    DB.commit()
    print()
    print(f'\033[38;2;0;255;0m[+] Added a new row to table "{TableName}" successfully!')
    print()
    input("\033[37;1mPress ENTER to back to the menu ")
    return

def DeleteRow(cursor: sqlite3.Cursor, DB: sqlite3.Connection):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InSelectingTable = True
    while InSelectingTable:
        print()
        print("\033[38;2;255;255;255mSelect a table.")
        TableName = input("> \033[38;2;0;255;0m")
        if TableName.replace(" ", "") == "":
            print("\033[38;2;255;0;0m[!] Invalid table name.")
        else:
            InSelectingTable = False
    print()
    print("\033[38;2;255;255;255m[!] This option is not programmed or designed to manage file automatically. You will manually search to delete.")
    print()
    print("Search using: Column1=\"Data\" AND Column2=5")
    print()
    print("Please learn more about sql if you don't know it well.")
    print()
    SearchCodes = input("> \033[38;2;0;255;0m")
    try:
        print()
        cursor.execute(f"DELETE FROM {TableName} WHERE {SearchCodes}")
        DB.commit()
        print("\033[38;2;0;255;0m[+] Deleted rows successfully.")
    except:
        print()
        print("\033[38;2;255;0;0m[-] An error occured.")
    print()
    input("\033[37;1mPress ENTER to back to the menu ")
    return

def DeleteTable(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    print()
    print("\033[37;1mREMEMBER! Tables are case-sensitive and this will literally delete it.")
    InSelectingTable = True
    while InSelectingTable:
        print()
        print("\033[38;2;255;255;255mWhich table do you want to delete? [Insert table name]")
        TableName = input("> \033[38;2;0;255;0m")
        if TableName.replace(" ", "") == "":
            print("\033[38;2;255;0;0m[!] Invalid table name.")
        else:
            InSelectingTable = False
    try:
        cursor.execute(f"DROP TABLE {TableName};")
        print()
        print(f'\033[38;2;0;255;0m[+] Deleted table "{TableName}" successfully!')
    except:
        print()
        print("\033[38;2;255;0;0m[-] An error occured.")
    print()
    input("\033[37;1mPress ENTER to back to the menu ")
    return

def AddColumn(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InInsertingTableName = True
    while InInsertingTableName:
        print()
        print("\033[38;2;255;255;255mWhich table do you want to add a new column to?")
        TableName = input("> \033[38;2;0;255;0m")
        try:
            TableInfo = cursor.execute(f"PRAGMA table_info({TableName});").fetchall()
        except:
            TableInfo = []
        if TableName.replace(" ", "") == "":
            print("\033[38;2;255;0;0m[!] Invalid table name.")
        elif len(TableInfo) == 0:
            print("\033[38;2;255;0;0m[!] Invalid table.")
        else:
            InInsertingTableName = False
    InInsertingName = True
    InInsertingType = True
    Columns = []
    for info in TableInfo:
        Columns.append(str(info[1]).lower())
    while InInsertingName:
        print()
        print("\033[38;2;255;255;255mInsert new column name.")
        ColumnName = input("> \033[38;2;0;255;0m")
        if ColumnName.replace(" ", "") == "":
            print("\033[38;2;255;0;0m[!] Column name must not be empty.")
        elif ColumnName.lower() in Columns:
            print("\033[38;2;255;0;0m[!] Column already exists.")
        else:
            InInsertingName = False
    Types = ["int", "string", "date"]
    print()
    print("\033[38;2;211;211;211mAvailable data types:")
    print(", ".join(Types))
    while InInsertingType:
        print()
        print("\033[38;2;255;255;255mSet type of column (Must be in the list).")
        ColumnType = input("> \033[38;2;0;255;0m")
        if not ColumnType.lower().replace(" ", "") in Types:
            print("\033[38;2;255;0;0m[!] Invalid data type.")
        else:
            InInsertingType = False
    try:
        cursor.execute(f"ALTER TABLE {TableName} ADD {ColumnName} {ColumnType};")
        print()
        print(f'\033[38;2;0;255;0m[+] Added a new column to table with name "{ColumnName}" successfully.')
    except:
        print()
        print("\033[38;2;255;0;0m[-] An error occured.")
    print()
    input("\033[37;1mPress ENTER to back to the menu ")
    return

def DropColumn(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InInsertingTableName = True
    while InInsertingTableName:
        print()
        print("\033[38;2;255;255;255mWhich table do you want to drop/delete a column on?")
        TableName = input("> \033[38;2;0;255;0m")
        try:
            TableInfo = cursor.execute(f"PRAGMA table_info({TableName});").fetchall()
        except:
            TableInfo = []
        if TableName.replace(" ", "") == "":
            print("\033[38;2;255;0;0m[!] Invalid table.")
        elif len(TableInfo) == 0:
            print("\033[38;2;255;0;0m[!] Invalid table.")
        else:
            InInsertingTableName = False
    InInsertingName = True
    Columns = []
    for info in TableInfo:
        Columns.append(str(info[1]).lower())
    while InInsertingName:
        print()
        print("\033[38;2;255;255;255mInsert column name.")
        ColumnName = input("> \033[38;2;0;255;0m")
        if ColumnName.replace(" ", "") == "":
            print("\033[38;2;255;0;0m[!] Column name must not be empty.")
        elif not ColumnName.lower() in Columns:
            print("\033[38;2;255;0;0m[!] Column doesn't exist.")
        else:
            InInsertingName = False
    try:
        cursor.execute(f"ALTER TABLE {TableName} DROP COLUMN {ColumnName};")
        print()
        print(f'\033[38;2;0;255;0m[+] Dropped column "{ColumnName}" successfully.')
    except:
        print()
        print("\033[38;2;255;0;0m[-] An error occured.")
    print()
    input("\033[37;1mPress ENTER to back to the menu ")
    return

def DeleteAllRows(cursor: sqlite3.Cursor, DB: sqlite3.Connection):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InSelectTableState = True
    while InSelectTableState:
        print()
        print("\033[38;2;255;255;255mSelect a table.")
        TableName = input("> \033[38;2;0;255;0m")
        try:
            TableInfo = cursor.execute(f"PRAGMA table_info({TableName});").fetchall()
        except:
            TableInfo = []
        if TableName.replace(" ", "") == "":
            print("\033[38;2;255;0;0m[!] Invalid table.")
        elif len(TableInfo) == 0:
            print("\033[38;2;255;0;0m[!] Invalid table.")
        else:
            InSelectTableState = False
    InConfirming = True
    IsConfirmed = False
    while InConfirming:
        print()
        print("\033[38;2;255;223;0m-> Are you sure about deleting all rows that are in this table? This action cannot be undone. (\033[38;2;255;0;0mY\033[38;2;255;223;0m/\033[38;2;0;255;0mN\033[38;2;255;223;0m)\033[38;2;255;255;255m")
        Confirm = input("> \033[38;2;0;255;0m")
        if Confirm.replace(" ", "").lower() in ["yes", "y", "ye"]:
            InConfirming = False
            IsConfirmed = True
        elif Confirm.replace(" ", "").lower() in ["no", "n"]:
            InConfirming = False
        else:
            print("\033[38;2;255;0;0m[!] Invalid option.")
    if IsConfirmed:
        try:
            cursor.execute(f"DELETE FROM {TableName};")
            DB.commit()
            print()
            print("\033[38;2;0;255;0m[+] Deleted all rows that were saved in the table successfully.")
        except:
            print()
            print("\033[38;2;255;0;0m[-] An error occured.")
    else:
        print()
        print("\033[38;2;0;255;0m[+] Canceled deleting rows operation successfully.")
    print()
    input("\033[37;1mPress ENTER to back to the menu ")
    return

def ShowTableContent(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InSelectingTable = True
    while InSelectingTable:
        print()
        print("\033[38;2;255;255;255mWhich table do you want to show?")
        TableName = input("> \033[38;2;0;255;0m")
        Results = cursor.execute(f"PRAGMA table_info({TableName})")
        ColumnNames = Results.fetchall()
        if TableName.replace(" ", "") == "":
            print("\033[38;2;255;0;0m[!] Invalid table name.")
        elif len(ColumnNames) == 0:
            print("\033[38;2;255;0;0m[!] Invalid table.")
        else:
            InSelectingTable = False
    Columns = "║   ║"
    lengthList = []
    for name in ColumnNames:
        lengthList.append(len(name[1])+2)
        Columns += f" {name[1]} ║"
    FirstLineOfTable = "╔═══╦"
    SecondLineOfTable = "╠═══╪"
    InsideLine = "╟───┼"
    LastLine = "╚═══╧"
    for LengthOfLine in lengthList:
        FirstLineOfTable += "═" * LengthOfLine
        SecondLineOfTable += "═" * LengthOfLine
        InsideLine += "─" * LengthOfLine
        LastLine += "═" * LengthOfLine
        if LengthOfLine != lengthList[len(lengthList)-1]:
            FirstLineOfTable += "╦"
            SecondLineOfTable += "╪"
            InsideLine += "┼"
            LastLine += "╧"
        else:
            FirstLineOfTable += "╗"
            SecondLineOfTable += "╣"
            InsideLine += "╢"
            LastLine += "╝"
    print("\033[38;2;255;255;255m")
    print(FirstLineOfTable)
    print(Columns)
    print(SecondLineOfTable)
    Results = cursor.execute(f"SELECT * FROM {TableName};")
    Rows = Results.fetchall()
    LengthOfRows = len(Rows)
    i = 0
    for row in Rows:
        RowLength = len(row)
        RowLine = f"║{utility.Fill(f'{i}.', 3)}"
        for c in range(RowLength):
            RowLine += f"│{utility.Fill(f'{row[c]}', lengthList[c])}"
        RowLine += "║"
        print(RowLine)
        if row != Rows[LengthOfRows-1]:
            print(InsideLine)
        else:
            print(LastLine)
        i += 1
    print()
    ShowContentsState = True
    while ShowContentsState:
        print("\033[37;1mInput number of row to display its data. Keep it blank to leave.")
        TheInput = input("> \033[38;2;0;255;0m")
        if TheInput == "":
            ShowContentsState = False
            break
        RowNumber = int(TheInput)
        AllDatasLength = []
        RowsData = []
        for data in Rows[RowNumber]:
            RowsData.append(data)
            AllDatasLength.append(len(str(data))+2)
        ColLength = max(lengthList)
        RowTableLength = max(AllDatasLength)
        FirstLineOfTable = "╔" + "═" * ColLength + "╤" + "═" * 6 + "╤" + "═" * RowTableLength + "╗"
        SecondLineOfTable = "╠" + "═" * ColLength + "╪" + "═" * 6 + "╪" + "═" * RowTableLength + "╣"
        LastLine = "╚" + "═" * ColLength + "╧" + "═" * 6 + "╧" + "═" * RowTableLength + "╝"
        print("\033[38;2;255;255;255m")
        print(FirstLineOfTable)
        print(f'║{utility.Fill(" Columns", ColLength)}│ Type │{utility.Fill(" Row", RowTableLength)}║')
        print(SecondLineOfTable)
        i = 0
        for col in ColumnNames:
            print(f'║{utility.Fill(f" {col[1]}", ColLength)}│{utility.Fill(f"{str(col[2]).upper()}", 6)}│{utility.Fill(f" {RowsData[i]}", RowTableLength)}║')
            if col != ColumnNames[len(ColumnNames)-1]:
                print("║" + "─" * ColLength + "┼" + "─" * 6 + "┼" + "─" * RowTableLength + "║")
            i += 1
        print(LastLine)
        print()
    input("\033[37;1mPress ENTER to back to the menu ")
    return