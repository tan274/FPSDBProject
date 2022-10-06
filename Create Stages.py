import mysql.connector

import project_connection_info


try:
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                              host=connection_info.MyHost,
                              database=connection_info.MyDatabase)

    cnx.autocommit = False
    cursor = cnx.cursor()
    # Template for just running the insert commands for the databse base information
    sql_insert_query = ("INSERT INTO Stage(stageName, stageDescription) VALUES ('Village', 'A starting village that the player starts the game in.'), ('Forest', 'A small forest located near the starting village populated with weak monsters like goblins and slimes.'), ('Dungeon', 'A dungeon found outside the forest that seems to contain powerful monster as well as many riches.'), ('Island', 'A small island off of the coast that may hold hidden treasure.'), ('Labyrinth', 'A maze like creation that contains many monsters.'), ('Mountains', 'A mountainous region home to bandits that is said to be the home of a dragon.'), ('Rainbow Road', 'A road made of rainbow blocks, how did it get here?'), ('Green Hill Zone', 'A grassy field with many twists and turns.'), ('Library', 'A quiet location.'), ('Lair', 'The unbreachable lair that holds the final boss.');")
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
