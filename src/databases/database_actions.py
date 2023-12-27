import sqlite3
import time

def get_date():
    return time.strftime("%d %b %Y")

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

def getallData(tablename):
     execString = "SELECT * FROM {0}".format(tablename)
     cursor.execute(execString)
     data = cursor.fetchall()
     return data

def addResource(supplier : int, product : int):
    tableLength = len(getallData("resources"))
    cursor.executemany("INSERT INTO resources values(?, ?, ?, ?)", [(tableLength + 1, supplier, product, get_date())])
    connection.commit()
    connection.close()

def addSupplier(name : str, resource : int, address : str = " "):
    tableLength = len(getallData("suppliers"))
    cursor.executemany("INSERT INTO resources values(?, ?, ?, ?)", [(tableLength + 1, name, address, resource)])
    connection.commit()
    connection.close()

def addProduct(productType : str, pricePerUnit : int, quantity : int):
    tableLength = len(getallData("products"))
    cursor.executemany("INSERT INTO resources values(?, ?, ?, ?, ?)", [(tableLength + 1, quantity, pricePerUnit, get_date(), productType)])
    connection.commit()
    connection.close()

