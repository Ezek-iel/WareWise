import json

try:
    sampleFile = open("screens\\storage\\settings.json").close()
except FileNotFoundError as error:
    sampleFile = open("settings.json").close()


def getResourceTypes() -> list:
    
    try:
        jsonfile = open("screens\\storage\\settings.json")
    except FileNotFoundError as error:
        jsonfile = open("settings.json")
    
    jsonData = json.load(jsonfile)
    
    jsonfile.close()
    return jsonData["Resource Types"]

def getProductTypes() -> list:
    
    try:
     jsonfile = open("screens\\storage\\settings.json")
    except FileNotFoundError as error:
        jsonfile = open("settings.json")
    
    jsonData = json.load(jsonfile)
    
    jsonfile.close()
    return jsonData["Product Types"]


def addProductType(productType):
    initData = getProductTypes()
    if productType not in initData:
        initData.append(productType)
    
    try:
        jsonfile = open("screens\\storage\\settings.json", "r")
    except FileNotFoundError as error:
        jsonfile = open("settings.json", "r")
    
    jsondata = json.load(jsonfile)
    jsonfile.close()

    jsondata["Product Types"] = initData

    try:
        jsonfile = open("screens\\storage\\settings.json", "w")
    except FileNotFoundError as error:
        jsonfile = open("settings.json")
    
    json.dump(jsondata, jsonfile, indent=4)
    jsonfile.close()

def addResourceType(resourceType):
    initData = getResourceTypes()
    
    if resourceType not in initData:
        initData.append(resourceType)
    
    try:
        jsonfile = open("screens\\storage\\settings.json", "r")
    except FileNotFoundError as error:
        jsonfile = open("settings.json", "r")
    
    jsondata = json.load(jsonfile)
    jsonfile.close()

    jsondata["Resource Types"] = initData

    try:
        jsonfile = open("screens\\storage\\settings.json", "w")
    except FileNotFoundError as error:
        jsonfile = open("settings.json","w")
    
    json.dump(jsondata, jsonfile, indent=4)
    jsonfile.close()
