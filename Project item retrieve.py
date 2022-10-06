import mysql.connector

import project_connection_info


cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                              host=connection_info.MyHost,
                              database=connection_info.MyDatabase)                           

cursor = cnx.cursor()

# tempItemName; Creation of item name for insertion

query = ("INSERT INTO Items(itemName, description, normalCost, premiumCost, health, defense, attack) VALUES ('Dagger', 'A simple small dagger.', '5', '2', '1', '1', '2');")

cursor.execute(query)

cursor.close()
cnx.close()                              
