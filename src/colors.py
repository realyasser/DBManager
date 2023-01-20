import Config

def fcolor(r:int, g:int, b:int) -> str:
    if str(Config.Getconfig("Settings", "Use-Colors")).lower().replace(" ", "") != "true":
        return ""
    return f"\033[38;2;{r};{g};{b}m"