import mysql.connector

import project_connection_info


try:
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                              host=connection_info.MyHost,
                              database=connection_info.MyDatabase)

    cnx.autocommit = False
    cursor = cnx.cursor()
    # Template for just running the insert commands for the databse base information
    sql_insert_query = ("INSERT INTO StageMonsters(stageName, monsterName, amount) VALUES ('Village', 'Slime', '3'), ('Forest', 'Goblin', '5'), ('Forest', 'Wolf', '3'), ('Dungeon', 'Troll', '1'), ('Labyrinth', 'Minotaur', '1'), ('Mountains', 'Bandit', '4'), ('Mountains', 'Dragon', '1'), ('Rainbow Road', 'Assassin', '1'), ('Library', 'Librarian', '1'), ('Lair', 'Gary', '1');")
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
