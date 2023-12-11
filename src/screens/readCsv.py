import csv

def readcsv():
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