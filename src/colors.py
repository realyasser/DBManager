import Config

def fcolor(r:int, g:int, b:int) -> str:
    if not bool(Config.Getconfig("Settings", "Use-Colors")):
        return ""
    return f"\033[38;2;{r};{g};{b}m"