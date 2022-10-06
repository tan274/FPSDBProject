import mysql.connector

import project_connection_info


try:
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                              host=connection_info.MyHost,
                              database=connection_info.MyDatabase)

    cnx.autocommit = False
    cursor = cnx.cursor()
    # Select for choosing all monsters created so far
    sql_select_query = ("SELECT monsterName FROM Monsters;")
    cursor.execute(sql_select_query) # use monsterName as table drop down list
    
    chosenMonster = ""; # Variable used to take in monster chosen by user (whichever monster was selected from drop down list)
    
    # Select for choosing all items from chosen monster
    sql_select_query = ("SELECT itemName, amount FROM MonsterDrops WHERE monsterName = %s);")
    cursor.execute(sql_select_query, chosenMonster) # use itemName as table drop down list (might also want to show previous amount value)
    
    chosenItem = ""; # Variable used to take in stage chosen by user (whichever item was selected from drop down list, might not be specified so users can change all items of a monster)
    
    # Just use a static input field for any integer
    chosenAmount = 0; # Variable used to take in new amount of items (could do something like a plus and minus button as well)
    
    # Update for changing the items dropped by monsters
    # The monster and amount are required, so they can update the amount of all items for a single monster, or for a specific item of a monster
    if (chosenMonster != "" && chosenAmount != "")
        if (chosenItem == "") {
            cursor.execute("UPDATE MonsterDrops SET amount = %d WHERE monsterName = %s);", (chosenAmount, chosenMonster))
        } else {
            cursor.execute("UPDATE MonsterDrops SET amount = %d WHERE monsterName = %s AND itemName = %s);", (chosenAmount, chosenMonster, chosenItem))
        }
    } else {
        # Maybe throw a rollback not sure probably just do nothing is best here
        print("Input monster and amount!")
    }

    print("Record Updated successfully")
    # Commit your changes
    cnx.commit()

except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    # reverting changes because of exception
    cnx.rollback()
finally:
    # closing database connection.
    if cnx.is_connected():
        cursor.close()
        cnx.close()
        print("Connection is closed")     