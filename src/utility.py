import os

def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")
    return

def Title():
    print('\033[31;22m')
    print()
    print(' ██████╗ ██████╗     ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗  ')
    print(' ██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗ ')
    print(' ██║  ██║██████╔╝    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝ ')
    print(' ██║  ██║██╔══██╗    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗ ')
    print(' ██████╔╝██████╔╝    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║ ')
    print(' ╚═════╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝ ')                                                                           
    print('\033[38;2;0;255;255m')
    print('                              Created by yasserprogamer                             ')
    print('\033[38;2;255;215;0m                                     Version 1.1                                    ')
    print()
    print()
    return

def Fill(text: str, length: int) -> str:
    FillLength = length - len(text)
    if FillLength >= 0:
        Result = text + " " * FillLength
    else:
        if length > 3:
            Result = text[:length-3]+"..."
        else:
            Result = text[:length]
    return Result