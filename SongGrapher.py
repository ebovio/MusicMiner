import pymongo
import numpy as np
import matplotlib.pyplot as plt

dbPath = 'mongodb://localhost:27017/' #Direccion de la conexion
dbName = 'canciones' # Nombre de la BD
colName = 'lista_canciones' #Nombre de la coleccion

myclient = pymongo.MongoClient(dbPath)
mydb = myclient[dbName]
mycol = mydb[colName]

year = 1957 
year_list = np.array([])
average_valence = np.array([])

valenceStats = {
}

while(year<=2018):
    for x in mycol.find( {'year': str(year)} ):
        if year not in valenceStats:
            valenceStats[year] = np.array([])
            valenceStats[year] = np.append(valenceStats[year], x['valence'])
        else:
            valenceStats[year] = np.append(valenceStats[year], x['valence'])
    year_list = np.append(year_list,year)
    year +=1


for i in year_list:
    average_valence = np.append(average_valence, np.average(valenceStats[i]))

print(average_valence)

plt.plot(year_list,average_valence,'ro')
plt.xlabel('Año')
plt.ylabel('Valencia Promedio')
plt.show()






