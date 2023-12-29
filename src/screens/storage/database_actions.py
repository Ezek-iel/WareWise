import sqlite3
import time

def get_date():
    return time.strftime("%d %b %Y")


def getallData(tablename):
     
    connection = sqlite3.connect("storage\\database.db")
    cursor = connection.cursor()


    execString = "SELECT * FROM {0}".format(tablename)
    cursor.execute(execString)
    data = cursor.fetchall()
    return data

def addResource(supplier : int, product : int, pricePerUnit,quantity):
    connection = sqlite3.connect("storage\\database.db")
    cursor = connection.cursor()

    
    tableLength = len(getallData("resources"))
    cursor.executemany("INSERT INTO resources values( ?, ?, ?, ?, ?)", [(supplier, product, get_date(), pricePerUnit, quantity)])
    connection.commit()
    connection.close()

def addSupplier(name : str, resource : int, address : str = " "):
    connection = sqlite3.connect("storage\\database.db")
    cursor = connection.cursor()

    
    tableLength = len(getallData("suppliers"))
    cursor.executemany("INSERT INTO suppliers values(?, ?, ?)", [(name, address, resource)])
    connection.commit()
    connection.close()

def addProduct(productType : str, pricePerUnit : int, quantity : int):
    connection = sqlite3.connect("storage\\database.db")
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

