import urllib.request, json
from urllib.parse import urlencode

def getKey(apiName):
    if apiName == "calendarific":
        apiFile = "key_calendarific.txt"
    elif apiName == "giphy":
        apiFile = "key_giphyapi.txt"
    elif apiName == "search":
        apiFile = "key_searchapi.txt"
    elif apiName == "spoonacular":
        apiFile = "key_spoonacular.txt"
    else:
        return "INVALID API NAME"

    keyFile = "keys/" + apiFile
    with open(keyFile, "r") as keyFile:
        api_key = keyFile.read().strip()
        if api_key == "":
            return "KEY NOT FOUND"
        return api_key

############################# Calendarific #############################

# Returns dictionary of header information, holidays, and their dates
def getHolidays(year, country="US"): # Default country to US if not given
    
    APIKEY = getKey("calendarific")

    if APIKEY == "KEY NOT FOUND": # Easy error handling if needed
        return 404
    if APIKEY == "INVALID API NAME":
        return 405
    
    params = {
        "api_key": APIKEY,
        "country": country,
        "year": year
    }

    paramString = urlencode(params)
    url = f"https://calendarific.com/api/v2/holidays?{paramString}"
    headers = {'User-Agent': 'Mozilla/5.0'} # 
    request = urllib.request.Request(url, headers=headers)

    holidaysList = []

    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode('utf-8'))
        holidays = data.get('response', {}).get('holidays', [])
        

        for holiday in holidays:
            holidaysList.append({
                "name": holiday.get("name"),
                "date": holiday.get("date", {}).get("iso"),
                "description": holiday.get("description"),
                "type": holiday.get("type", [])
            })
    
    return holidaysList

    
