import urllib.request, json
from urllib.parse import urlencode
import calendar

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
    headers = {'User-Agent': 'Mozilla/5.0'} 
    request = urllib.request.Request(url, headers=headers)

    holidaysList = []
    
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode('utf-8'))
            holidays = data.get('response', {}).get('holidays', [])
            
            existingNames = set()

            for holiday in holidays:
                name = holiday.get("name")
                if name not in existingNames:
                    holidaysList.append({
                        "name": holiday.get("name"),
                        "date": holiday.get("date", {}).get("iso"),
                        "description": holiday.get("description"),
                        "type": holiday.get("type", [])
                    })
                    existingNames.add(name)
        return holidaysList
    
    except Exception as e:
        print(f"Exception occurred: {e}")
        return 403


############################# GiphyAPI #############################

def getGif(tag):

    APIKEY = getKey("giphy")

    if APIKEY == "KEY NOT FOUND": # Easy error handling if needed
        return 404
    if APIKEY == "INVALID API NAME":
        return 405
    
    params = {
        "api_key": APIKEY,
        "tag": tag,
        "number": 30
    }

    paramString = urlencode(params)
    url = f"https://api.giphy.com/v1/gifs/random?{paramString}"
    headers = {'User-Agent': 'Mozilla/5.0'} 
    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode('utf-8'))
            if 'data' in data and data['data']:
                return {"link": data['data']['images']["original"]["url"], "title": data['data']['title']}
            else:
                return "No gif found"
    
    except Exception as e:
        print(f"Exception occurred: {e}")
        return 403

############################# SearchAPI #############################

def getFirstLink(query, engine="google"):

    APIKEY = getKey("search")

    if APIKEY == "KEY NOT FOUND": # Easy error handling if needed
        return 404
    if APIKEY == "INVALID API NAME":
        return 405
    
    params = {
        "api_key": APIKEY,
        "engine": engine,
        "q": query
    }

    paramString = urlencode(params)
    url = f"https://www.searchapi.io/api/v1/search?{paramString}"
    headers = {'User-Agent': 'Mozilla/5.0'} 
    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode('utf-8'))
            result = data.get("organic_results", [])[0]["link"]

            return result
    
    except Exception as e:
        print(f"Exception occurred: {e}")
        return 403

# print(getFirstLink("鸡肉盖饭", "baidu"))


############################# Spoonacular #############################

def getRecipes(query, minCarbs=0, maxCarbs=100000, minProtein=10, maxProtein=100000, minCalories=0, maxCalories=100000, minFat=0, maxFat=100000):

    APIKEY = getKey("spoonacular")

    if APIKEY == "KEY NOT FOUND": # Easy error handling if needed
        return 404
    if APIKEY == "INVALID API NAME":
        return 405
    
    ingredients = "+".join(query.split())  # Convert spaces to '+'
    ingredients_param = ingredients.replace("+", ",+")  # Add ',+' between words
    
    params = {
        "apiKey": APIKEY,
        "query": query,
        "includeIngredients": ingredients_param,
        "minCarbs": minCarbs,
        "maxCarbs": maxCarbs,
        "minProtein": minProtein,
        "maxProtein": maxProtein,
        "minCalories": minCalories,
        "maxCalories": maxCalories,
        "minFat": minFat,
        "maxFat": maxFat,
        "number": 100
    }

    paramString = urlencode(params)
    url = f"https://api.spoonacular.com/recipes/complexSearch?{paramString}"
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0'} 
    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode('utf-8'))
                results = data.get("results", [])

                fullList = [
                    {"id": item["id"], "title": item["title"], "image": item["image"]}
                    for item in results
                ]
                return fullList
            else:
                return "RATE-LIMITED"
    
    except Exception as e:
        print(f"Exception occurred: {e}")
        return 403

def getRecipeInformation(id):

    APIKEY = getKey("spoonacular")

    if APIKEY == "KEY NOT FOUND": # Easy error handling if needed
        return 404
    if APIKEY == "INVALID API NAME":
        return 405
    
    params = {
        "apiKey": APIKEY,
        "id": id,
        "includeNutrition": True,
    }

    paramString = urlencode(params)
    url = f"https://api.spoonacular.com/recipes/{id}/information?{paramString}"
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0'} 
    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode('utf-8'))

                fullList = []

                baseInformation = {
                    "title": data["title"],
                    "servings": data["servings"],
                    "readyInMinutes": data["readyInMinutes"],
                    "healthScore": data["healthScore"],
                    "creditsText": data["creditsText"],
                    "dishTypes": data["dishTypes"],
                    "summary": data["summary"]
                }

                nutrition = data["nutrition"]["nutrients"]
                ingredients = data["nutrition"]["ingredients"]
                breakdown = data["nutrition"]["caloricBreakdown"]
                steps = data["analyzedInstructions"][0]["steps"]
                

                fullList.append(baseInformation)
                fullList.append(nutrition)
                fullList.append(ingredients)
                fullList.append(breakdown)
                print(breakdown)
                fullList.append(steps)

                return fullList
            else:
                return "RATE-LIMITED"
    
    except Exception as e:
        print(f"Exception occurred: {e}")
        return 403

############################# Calendar #############################

def fullCalendar(year, month, data):
    cal = calendar.monthcalendar(year, month)
    for i in range(len(cal)):
        for j in range(len(cal[i])):
            cal[i][j] = [cal[i][j]]
            for k in range(len(data)):
                holidate = data[k]['date'].split("-")
                #print(cal[i][j])
                if (int(holidate[1]) == month and int(holidate[2][:2]) == cal[i][j][0]):
                    if (data[k]['name'] not in cal[i][j]):
                        cal[i][j].append(data[k])
                        #print(cal[i][j])
    return cal