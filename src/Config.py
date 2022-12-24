import configparser
import os

def CheckFileExistence():
    if os.path.exists("config.ini"):
        return True
    else:
        return False

def CreateConfigFile():
    config = configparser.ConfigParser(allow_no_value=True)
    config["Updates"] = {}
    config["Updates"]["check-for-updates"] = None
    with open("config.ini", "w") as f:
        config.write(f)
    return None

def Getconfig(group: str, var: str):
    config = configparser.ConfigParser(allow_no_value=True)
    config.sections()
    config.read("config.ini")
    return config[group][var]

def Setconfig(group: str, var: str, data):
    config = configparser.ConfigParser(allow_no_value=True)
    config.sections()
    config.read("config.ini")
    config[group][var] = data
    with open("config.ini", "w") as f:
        config.write(f)
    return None