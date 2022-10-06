import mysql.connector

import project_connection_info


try:
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                              host=connection_info.MyHost,
                              database=connection_info.MyDatabase)

    cnx.autocommit = False
    cursor = cnx.cursor()
    # Template for just running the insert commands for the databse base information
    sql_insert_query = ("INSERT INTO MonsterDrops(monsterDropID, monsterName, itemName, amount) VALUES ('1', 'Slime', 'test2', '99'), ('2', 'Goblin', 'Dagger', '2'), ('3', 'Troll', 'Club', '1'), ('4', 'Minotaur', 'TEst1', '1'), ('5', 'Bandit', 'Dagger', '3'), ('6', 'Assassin', 'Dagger', '7'), ('7', 'Librarian', 'Test3', '0'), ('8', 'Gary', 'Test3', '2');")
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
