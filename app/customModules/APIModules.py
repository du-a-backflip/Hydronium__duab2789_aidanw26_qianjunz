from pathlib import Path

def getKey(apiFile):
    folder = Path("../keys/")
    keyFile = folder / apiFile
    with open(keyFile, "r") as keyFile:
        api_key = keyFile.read().strip()
        if api_key == None:
            return "KEY NOT FOUND"
        return api_key


############################# Calendarific #############################
