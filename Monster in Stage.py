import mysql.connector

import project_connection_info


try:
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                              host=connection_info.MyHost,
                              database=connection_info.MyDatabase)

    cnx.autocommit = False
    cursor = cnx.cursor()
    
    # Select for choosing all stages created so far
    sql_select_query = ("SELECT stageName FROM Stage;")
    cursor.execute(sql_select_query) # use stageName as table drop down list
    
    chosenStage = ""; # Variable used to take in stage chosen by user (whichever stage was selected from drop down list)
    
    # Select for choosing all monsters from chosen stage
    sql_select_query = ("SELECT monsterName, amount FROM StageMonsters WHERE stageName = %s);")
    cursor.execute(sql_select_query, chosenStage) # use monsterName as table drop down list (might also want to show previous amount value)
    
    chosenMonster = ""; # Variable used to take in monster chosen by user (whichever item was selected from drop down list, might not be specified so users can change all monsters of a stage)
    
    # Just use a static input field for any integer
    chosenAmount = 0; # Variable used to take in new amount of monsters (could do something like a plus and minus button as well)
    
    # Update for changing the monsters in a stage
    # The stage and amount are required, so they can update the amount of all monsters for a single stage, or for a specific monster of a stage
    if (chosenStage != "" && chosenAmount != "")
        if (chosenMonster == "") {
            cursor.execute("UPDATE StageMonsters SET amount = %d WHERE stageName = %s);", (chosenAmount, chosenStage))
        } else {
            cursor.execute("UPDATE StageMonsters SET amount = %d WHERE stageName = %s AND monsterName = %s);", (chosenAmount, chosenStage, chosenMonster))
        }
    } else {
        # Maybe throw a rollback not sure probably just do nothing is best here
        print("Input stage and amount!")
    }
   
    print("Record Updated successfully")
    # Commit your changes
    cnx.commit()

except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    # reverting changes because of exception
    cnx.rollback()
finally:
    # closing database connection
    if cnx.is_connected():
        cursor.close()
        cnx.close()
        print("Connection is closed")     