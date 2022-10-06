import mysql.connector

import project_connection_info


try:
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                              host=connection_info.MyHost,
                              database=connection_info.MyDatabase)

    cnx.autocommit = False
    cursor = cnx.cursor()
    # Template for just running the insert commands for the databse base information
    sql_insert_query = ("INSERT INTO Monsters(monsterName, health, defense, attack) VALUES ('Slime', '1', '1', '1'), ('Goblin', '15', '2', '3'), ('Wolf', '20', '2', '3'), ('Troll', '30', '3', '5'), ('Bandit', '20', '2', '4'), ('Bandit Assassin', '10', '1', '10'), ('Minotaur', '40', '4', '10'), ('Dragon', '100', '5', '20'), ('Librarian', '999', '99', '999'), ('Gary', '150', '15', '50');")
    cursor.execute(sql_insert_query)

    print("Record Updated successfully")
    # Commit your changes
    cnx.commit()

except mysql.connector.Error as error:
    print("Failed to insert record to database rollback: {}".format(error))
    # reverting changes because of exception
    cnx.rollback()
finally:
    # closing database connection
    if cnx.is_connected():
        cursor.close()
        cnx.close()
        print("Connection is closed")                              
