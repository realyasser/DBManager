import os
import colors

def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")
    return

def Title():
    print(f'{colors.fcolor(255, 0, 0)}')
    print()
    print('██████╗ ██████╗    ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ █████╗██████╗ ')
    print('██╔══██╗██╔══██╗   ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔══╝██╔══██╗')
    print('██║  ██║██████╔╝   ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗██████╔╝')
    print('██║  ██║██╔══██╗   ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝██╔══██╗')
    print('██████╔╝██████╔╝   ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝█████╗██║  ██║')
    print('╚═════╝ ╚═════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚════╝╚═╝  ╚═╝')                                                                           
    print(f'{colors.fcolor(0, 255, 255)}')
    print('                            Created by yasserprogamer                        ')
    print(f'{colors.fcolor(255, 215, 0)}                                   Version 1.2                           ')
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