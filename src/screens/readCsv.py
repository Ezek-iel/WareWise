import csv

def readResourcesCsv():
    data = []
    with open("sampleData.csv","r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dataRow = []
            dataRow.append(row["Product"])
            dataRow.append(row["Quantity"])
            dataRow.append(row["Supplier"])
            dataRow.append(row["Status"])
            dataRow.append(row["Price Per Unit"])
            data.append(dataRow)
    return data

productInfo = [["Sudan Y", 20000, 1650],["Convertible Z", 30000, 1700], ["Car Cheap R", 4000, 1740]]

supplierInfo = [["Aorg",3400,45004,340000],["Bcorp",4500,33232,450000],["Ccom",3400,4213,340234]]
