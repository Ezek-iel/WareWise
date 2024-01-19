import sqlite3
import time

def get_date():
    return time.strftime("%d %b %Y")

try:
    sampleConnection = sqlite3.connect("screens\\storage\\database.db")

except sqlite3.OperationalError as error:
    sampleConnection = sqlite3.connect("database.db")

sampleCursor = sampleConnection.cursor()

sampleConnection.commit()
sampleConnection.close()

def getallData(tablename):
    
    try:
        connection = sqlite3.connect("screens\\storage\\database.db")
    
    except sqlite3.OperationalError as error:
        connection = sqlite3.connect("database.db")
    
    cursor = connection.cursor()


    execString = "SELECT * FROM {0}".format(tablename)
    cursor.execute(execString)
    data = cursor.fetchall()
    return data

def addResource(supplier : int, product : int, pricePerUnit,quantity):
    
    try:
        connection = sqlite3.connect("screens\\storage\\database.db")
    
    except sqlite3.OperationalError as error:
        connection = sqlite3.connect("database.db")
    
    cursor = connection.cursor()

    
    tableLength = len(getallData("resources"))
    cursor.executemany("INSERT INTO resources values( ?, ?, ?, ?, ?)", [(supplier, product, get_date(), pricePerUnit, quantity)])
    connection.commit()
    connection.close()

def addSupplier(name : str, resource : int, address : str = " "):
    
    try:
        connection = sqlite3.connect("screens\\storage\\database.db")
    
    except sqlite3.OperationalError as error:
        connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    
    tableLength = len(getallData("screens\\suppliers"))
    cursor.executemany("INSERT INTO suppliers values(?, ?, ?)", [(name, address, resource)])
    connection.commit()
    connection.close()

def addProduct(productType : str, pricePerUnit : int, quantity : int):
    
    try:
        connection = sqlite3.connect("screens\\storage\\database.db")
    
    except sqlite3.OperationalError as error:
        connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    
    tableLength = len(getallData("products"))
    cursor.executemany("INSERT INTO products values(?, ?, ?, ?)", [(productType, get_date(), pricePerUnit, quantity)])
    connection.commit()
    connection.close()

def getSupplierNames():
    supplierInfo = getallData("suppliers")

    supplierNames = []
    for supplier in supplierInfo:
        supplierNames.append(supplier[0])
    
    return supplierNames

