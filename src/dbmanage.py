import sqlite3
import utility
import os
import MetaData
import colors

def CreateTable(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    InSettingNewTableName = True
    while InSettingNewTableName:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Set a name for the new table.")
        NewTableName = input(f"> {colors.fcolor(0, 255, 0)}")
        try:
            TableInfo = cursor.execute(f"PRAGMA table_info({NewTableName});").fetchall()
            if NewTableName.replace(" ", "") == "":
                print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table name.")
            elif len(TableInfo) > 0:
                print(f"{colors.fcolor(255, 0, 0)}[!] Table already exists.")
            else:
                InSettingNewTableName = False
        except:
            print(f"{colors.fcolor(255, 0, 0)}[!] Unexpected error occurred.")
    InSettingColumnsNumber = True
    while InSettingColumnsNumber:
        print()
        print(f"{colors.fcolor(255, 255, 255)}How many columns do you want?")
        NumberOfColumns = input(f"> {colors.fcolor(0, 255, 0)}")
        IsInteger = False
        try:
            if int(NumberOfColumns):
                IsInteger = True
        except:
            IsInteger = False
        if NumberOfColumns.replace(" ", "") == "":
            print(f"{colors.fcolor(255, 0, 0)}[!] Please input an integer.")
        elif not IsInteger:
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid integer.")
        else:
            InSettingColumnsNumber = False
    NumberOfColumns = int(NumberOfColumns)
    Types = ["int", "string", "date"]
    print()
    print(f"{colors.fcolor(211, 211, 211)}Available data types:")
    print(", ".join(Types))
    ColumnsList = []
    for n in range(NumberOfColumns):
        InAddingNewColumnName = True
        while InAddingNewColumnName:
            print()
            print(f"{colors.fcolor(255, 255, 255)}{n+1} | Column name:")
            ColumnName = input(f"> {colors.fcolor(0, 255, 0)}")
            if ColumnName.replace(" ", "") == "":
                print(f"{colors.fcolor(255, 0, 0)}[!] Empty column name.")
            else:
                InAddingNewColumnName = False
        InSettingColumnType = True
        while InSettingColumnType:
            print()
            print(f"{colors.fcolor(255, 255, 255)}{n+1} | Column data type:")
            ColumnType = input(f"> {colors.fcolor(0, 255, 0)}")
            if ColumnType.replace(" ", "") == "":
                print(f"{colors.fcolor(255, 0, 0)}[!] Invalid data type.")
            elif not ColumnType.lower().replace(" ", "") in Types:
                print(f"{colors.fcolor(255, 0, 0)}[!] Invalid data type.")
            else:
                InSettingColumnType = False
        ColumnsList.append(f"{ColumnName} {ColumnType}")
    print()
    try:
        cursor.execute(f"CREATE TABLE {NewTableName} ({', '.join(ColumnsList)});")
        print(f"{colors.fcolor(0, 255, 0)}[+] Created a new table with name \"{NewTableName}\" successfully.")
    except:
        print(f"{colors.fcolor(255, 0, 0)}[-] An error occurred while trying to create a new table.")
    print()
    input(f"{colors.fcolor(255, 255, 255)}Press ENTER to back to the menu ")
    return

def ShowTables(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    try:
        Results = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;")
        TablesList = Results.fetchall()
        Length = len(TablesList)
        if Length != 0:
            print(f"{colors.fcolor(255, 255, 255)}Tables that are in this database file:\n{colors.fcolor(0, 255, 0)}")
            for Table in TablesList:
                print(f"[+] {Table[0]}")
        else:
            print(f"{colors.fcolor(255, 255, 255)}No tables are in this database file.")
    except:
        print(f"{colors.fcolor(255, 0, 0)}[-] An error occurred.")
    print()
    input(f"{colors.fcolor(255, 255, 255)}Press ENTER to back to the menu ")
    return

def ListTables(cursor: sqlite3.Cursor, lowercaseOutput = True) -> list | bool:
    try:
        Results = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;")
        TablesList = Results.fetchall()
        if len(TablesList) == 0:
            print()
            print(f"{colors.fcolor(218, 218, 218)}There are no tables in this database file.")
        else:
            print(f"{colors.fcolor(218, 218, 218)}")
            print("Available tables:")
            ListOfTables = []
            OutputList = []
            for table in TablesList:
                ListOfTables.append(table[0])
                if lowercaseOutput:
                    OutputList.append(table[0].lower())
            print(", ".join(ListOfTables))
            if not lowercaseOutput:
                OutputList = ListOfTables
    except:
        print(f"{colors.fcolor(255, 0, 0)}[!] Unexpected error occured while trying to fetch tables.")
        OutputList = False
    return OutputList

def InsertRow(cursor: sqlite3.Cursor, DB: sqlite3.Connection):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InSelectingTable = True
    while InSelectingTable:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Select a table.")
        TableName = input(f"> {colors.fcolor(0, 255, 0)}")
        try:
            TableInfo = cursor.execute(f"PRAGMA table_info({TableName});").fetchall()
        except:
            TableInfo = []
        Size = len(TableInfo)
        if TableName.replace(" ", "") == "":
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table name.")
        elif Size == 0:
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table.")
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
            TheValue = input(f"{colors.fcolor(255, 255, 255)}[Type: {TableInfo[n][2]}] {TableInfo[n][1]}: {colors.fcolor(0, 255, 0)}")
            if str(TableInfo[n][2]).lower() != "int":
                Pass = True
            else:
                try:
                    if int(TheValue):
                        TheValue = int(TheValue)
                        Pass = True
                except:
                    print(f"{colors.fcolor(255, 0, 0)}[!] Invalid integer.")
                    Pass = False
            if Pass:
                Values.append(TheValue)
                InInsertingValue = False
    print()
    try:
        cursor.execute(f"INSERT INTO {TableName} VALUES ({', '.join(ValuesQuestionMark)});", tuple(Values))
        DB.commit()
        print(f'{colors.fcolor(0, 255, 0)}[+] Added a new row to table "{TableName}" successfully!')
    except:
        print(f"{colors.fcolor(255, 0, 0)}[!] An error occurred while trying to add a new row to the table.")
    print()
    input(f"{colors.fcolor(255, 255, 255)}Press ENTER to back to the menu ")
    return

def DeleteRow(cursor: sqlite3.Cursor, DB: sqlite3.Connection):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InSelectingTable = True
    while InSelectingTable:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Select a table.")
        TableName = input(f"> {colors.fcolor(0, 255, 0)}")
        if TableName.replace(" ", "") == "":
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table name.")
        else:
            InSelectingTable = False
    print()
    print(f"{colors.fcolor(255, 255, 255)}[!] This option is not programmed or designed to manage file automatically. You will manually search to delete.")
    print()
    print("Search using: Column1=\"Data\" AND Column2=5")
    print()
    print("Please learn more about sql if you don't know it well.")
    print()
    SearchCodes = input(f"> {colors.fcolor(0, 255, 0)}")
    try:
        print()
        cursor.execute(f"DELETE FROM {TableName} WHERE {SearchCodes}")
        DB.commit()
        print(f"{colors.fcolor(0, 255, 0)}[+] Deleted rows successfully.")
    except:
        print()
        print(f"{colors.fcolor(255, 0, 0)}[-] An error occured.")
    print()
    input(f"{colors.fcolor(255, 255, 255)}Press ENTER to back to the menu ")
    return

def DeleteTable(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    print()
    print(f"{colors.fcolor(255, 255, 255)}REMEMBER! Tables are case-sensitive and this will literally delete it.")
    InSelectingTable = True
    while InSelectingTable:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Which table do you want to delete? [Insert table name]")
        TableName = input(f"> {colors.fcolor(0, 255, 0)}")
        if TableName.replace(" ", "") == "":
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table name.")
        else:
            InSelectingTable = False
    try:
        cursor.execute(f"DROP TABLE {TableName};")
        print()
        print(f'{colors.fcolor(0, 255, 0)}[+] Deleted table "{TableName}" successfully!')
    except:
        print()
        print(f"{colors.fcolor(255, 0, 0)}[-] An error occured.")
    print()
    input(f"{colors.fcolor(255, 255, 255)}Press ENTER to back to the menu ")
    return

def AddColumn(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InInsertingTableName = True
    while InInsertingTableName:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Which table do you want to add a new column to?")
        TableName = input(f"> {colors.fcolor(0, 255, 0)}")
        try:
            TableInfo = cursor.execute(f"PRAGMA table_info({TableName});").fetchall()
        except:
            TableInfo = []
        if TableName.replace(" ", "") == "":
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table name.")
        elif len(TableInfo) == 0:
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table.")
        else:
            InInsertingTableName = False
    InInsertingName = True
    InInsertingType = True
    Columns = []
    for info in TableInfo:
        Columns.append(str(info[1]).lower())
    while InInsertingName:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Insert new column name.")
        ColumnName = input(f"> {colors.fcolor(0, 255, 0)}")
        if ColumnName.replace(" ", "") == "":
            print(f"{colors.fcolor(255, 0, 0)}[!] Column name must not be empty.")
        elif ColumnName.lower() in Columns:
            print(f"{colors.fcolor(255, 0, 0)}[!] Column already exists.")
        else:
            InInsertingName = False
    Types = ["int", "string", "date"]
    print()
    print(f"{colors.fcolor(211, 211, 211)}Available data types:")
    print(", ".join(Types))
    while InInsertingType:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Set type of column (Must be in the list).")
        ColumnType = input(f"> {colors.fcolor(0, 255, 0)}")
        if not ColumnType.lower().replace(" ", "") in Types:
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid data type.")
        else:
            InInsertingType = False
    try:
        cursor.execute(f"ALTER TABLE {TableName} ADD {ColumnName} {ColumnType};")
        print()
        print(f'{colors.fcolor(0, 255, 0)}[+] Added a new column to table with name "{ColumnName}" successfully.')
    except:
        print()
        print(f"{colors.fcolor(255, 0, 0)}[-] An error occured.")
    print()
    input(f"{colors.fcolor(255, 255, 255)}Press ENTER to back to the menu ")
    return

def DropColumn(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InInsertingTableName = True
    while InInsertingTableName:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Which table do you want to drop/delete a column on?")
        TableName = input(f"> {colors.fcolor(0, 255, 0)}")
        try:
            TableInfo = cursor.execute(f"PRAGMA table_info({TableName});").fetchall()
        except:
            TableInfo = []
        if TableName.replace(" ", "") == "":
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table.")
        elif len(TableInfo) == 0:
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table.")
        else:
            InInsertingTableName = False
    InInsertingName = True
    Columns = []
    for info in TableInfo:
        Columns.append(str(info[1]).lower())
    while InInsertingName:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Insert column name.")
        ColumnName = input(f"> {colors.fcolor(0, 255, 0)}")
        if ColumnName.replace(" ", "") == "":
            print(f"{colors.fcolor(255, 0, 0)}[!] Column name must not be empty.")
        elif not ColumnName.lower() in Columns:
            print(f"{colors.fcolor(255, 0, 0)}[!] Column doesn't exist.")
        else:
            InInsertingName = False
    try:
        cursor.execute(f"ALTER TABLE {TableName} DROP COLUMN {ColumnName};")
        print()
        print(f'{colors.fcolor(0, 255, 0)}[+] Dropped column "{ColumnName}" successfully.')
    except:
        print()
        print(f"{colors.fcolor(255, 0, 0)}[-] An error occured.")
    print()
    input(f"{colors.fcolor(255, 255, 255)}Press ENTER to back to the menu ")
    return

def DeleteAllRows(cursor: sqlite3.Cursor, DB: sqlite3.Connection):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InSelectTableState = True
    while InSelectTableState:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Select a table.")
        TableName = input(f"> {colors.fcolor(0, 255, 0)}")
        try:
            TableInfo = cursor.execute(f"PRAGMA table_info({TableName});").fetchall()
        except:
            TableInfo = []
        if TableName.replace(" ", "") == "":
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table.")
        elif len(TableInfo) == 0:
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table.")
        else:
            InSelectTableState = False
    InConfirming = True
    IsConfirmed = False
    while InConfirming:
        print()
        print(f"{colors.fcolor(255, 223, 0)}-> Are you sure about deleting all rows that are in this table? This action cannot be undone. ({colors.fcolor(255, 0, 0)}Y{colors.fcolor(255, 223, 0)}/{colors.fcolor(0, 255, 0)}N{colors.fcolor(255, 223, 0)}){colors.fcolor(255, 255, 255)}")
        Confirm = input(f"> {colors.fcolor(0, 255, 0)}")
        if Confirm.replace(" ", "").lower() in ["yes", "y", "ye"]:
            InConfirming = False
            IsConfirmed = True
        elif Confirm.replace(" ", "").lower() in ["no", "n"]:
            InConfirming = False
        else:
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid option.")
    if IsConfirmed:
        try:
            cursor.execute(f"DELETE FROM {TableName};")
            DB.commit()
            print()
            print(f"{colors.fcolor(0, 255, 0)}[+] Deleted all rows that were saved in the table successfully.")
        except:
            print()
            print(f"{colors.fcolor(255, 0, 0)}[-] An error occured.")
    else:
        print()
        print(f"{colors.fcolor(0, 255, 0)}[+] Canceled deleting rows operation successfully.")
    print()
    input(f"{colors.fcolor(255, 255, 255)}Press ENTER to back to the menu ")
    return

def ShowTableContent(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    ListTables(cursor=cursor)
    InSelectingTable = True
    while InSelectingTable:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Which table do you want to show?")
        TableName = input(f"> {colors.fcolor(0, 255, 0)}")
        Results = cursor.execute(f"PRAGMA table_info({TableName})")
        ColumnNames = Results.fetchall()
        if TableName.replace(" ", "") == "":
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table name.")
        elif len(ColumnNames) == 0:
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table.")
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
    print(f"{colors.fcolor(255, 255, 255)}")
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
        print(f"{colors.fcolor(255, 255, 255)}Input number of row to display its data. Keep it blank to leave.")
        TheInput = input(f"> {colors.fcolor(0, 255, 0)}")
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
        print(f"{colors.fcolor(255, 255, 255)}")
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
    input(f"{colors.fcolor(255, 255, 255)}Press ENTER to back to the menu ")
    return

def DBToCSV(cursor: sqlite3.Cursor):
    utility.clear()
    utility.Title()
    TablesList = ListTables(cursor=cursor)
    InSelectingTable = True
    while InSelectingTable:
        print()
        print(f"{colors.fcolor(255, 255, 255)}Select a table.")
        TableSelection = input(f"> {colors.fcolor(0, 255, 0)}")
        if TableSelection.replace(" ", "") == "":
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table name.")
        elif not TableSelection.lower() in TablesList:
            print(f"{colors.fcolor(255, 0, 0)}[!] Invalid table.")
        else:
            InSelectingTable = False
    print()
    print(f"{colors.fcolor(255, 223, 0)}[+] Converting data to CSV file....")
    if not os.path.exists(f"./csv/{MetaData.Filename.replace('.', '_').replace(':', '_').replace('>', '-')}/"):
        os.makedirs(f"./csv/{MetaData.Filename.replace('.', '_').replace(':', '_').replace('>', '-')}/")
    try:
        file = open(f"./csv/{MetaData.Filename.replace('.', '_').replace(':', '_').replace('>', '-')}/{TableSelection}.csv", "w")
        ColNames = cursor.execute(f"PRAGMA table_info({TableSelection});").fetchall()
        Columns = []
        for Column in ColNames:
            Columns.append(f'"{Column[1]}"')
        file.write(f'{",".join(Columns)}\n')
        TableData = cursor.execute(f"SELECT * FROM {TableSelection};")
        Rows = []
        for data in TableData:
            DataWithQuotes = []
            for d in data:
                DataWithQuotes.append(f'"{d}"')
            Rows.append(",".join(DataWithQuotes))
        file.write("\n".join(Rows))
        file.close()
        print()
        print(f"{colors.fcolor(0, 255, 0)}[+] Done!")
        print(f"{colors.fcolor(255, 255, 255)}[>] Directory: {colors.fcolor(223, 223, 223)}{os.getcwd()}\\csv\\{MetaData.Filename.replace('.', '_')}\\{TableSelection}.csv")
    except:
        print()
        print(f"{colors.fcolor(255, 0, 0)}[!] An error occurred.")
    print()
    input(f"{colors.fcolor(255, 255, 255)}Press ENTER to back to the menu ")
    return
