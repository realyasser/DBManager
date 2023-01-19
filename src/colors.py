import sys
import os

def fcolor(r:int, g:int, b:int) -> str:
    if os.name == 'nt':
        if sys.getwindowsversion().major < 10:
            return ""
    return f"\033[38;2;{r};{g};{b}m"