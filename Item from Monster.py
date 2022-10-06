import mysql.connector

import project_connection_info


try:
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                              host=connection_info.MyHost,
                              database=connection_info.MyDatabase)

    cnx.autocommit = False
    cursor = cnx.cursor()
    
    # Select for choosing all usernames created so far
    sql_select_query = ("SELECT username FROM Player;")
    cursor.execute(sql_select_query) # use username as table drop down list
    
    currentUser = ""; # Variable used to take in chosen user (whichever username was selected from drop down list)
    
    # Select for choosing all monster drops created so far
    sql_select_query = ("SELECT monsterName, itemName as mdItemName, amount as mdAmount FROM MonsterDrops;")
    cursor.execute(sql_select_query) # use probably all three values as table drop down list
    
    # All values stored from chosen monster drop from drop down list
    chosenMonsterName = ""; # Variable used to take in chosen monster name
    chosenItemName = ""; # Variable used to take in chosen item name
    chosenAmount = 0; # Variable used to take in chosen amount
    
    # Get items and amount of that item that user already has (might have to be careful not to increase items equiped by characters)
    cursor.execute("SELECT itemName as irItemName, amount as irAmount FROM ItemRel WHERE username = %s AND characterID = NULL);", (currentUser))
    
    # Update or Insertion for if they already had the item or not
    for (irItemName, irAmount) in cursor {
        if (irItemName == chosenItemName) {
            newAmount = irAmount + chosenAmount;
            cursor.execute("UPDATE ItemRel SET amount = %d WHERE username = %s AND itemName = %s);", (newAmount, currentUser, chosenItemName))
            print("Record Updated successfully")
            break;
        }
    } else {
        cursor.execute("INSERT INTO ItemRel(itemName, username, characterID, amount) VALUES ('%s', '%s', NULL, '%d');", (chosenItemName, currentUser, chosenAmount))
        print("Record Inserted successfully")
    }
    
    # Commit your changes
    cnx.commit()

except mysql.connector.Error as error:
    print("Failed to update or insert record to database rollback: {}".format(error))
    # reverting changes because of exception
    cnx.rollback()
finally:
    # closing database connection.
    if cnx.is_connected():
        cursor.close()
        cnx.close()
        print("Connection is closed")     