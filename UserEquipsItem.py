'''


This is for when user equips item for a specific characterID

'''

import mysql.connector
import connection_info

#Need user to specify these variables for user to obtain item
#username = 'tan123'
#characterID = '123'
#ItemName= 'sword'
#amount = 2
#UPDATE ItemRel set amount = amount-2 where username = 'tan123' and ItemName = 'sword';
#UPDATE Player SET normalCurr = normalCurr - 2* (select normalCost from Items where ItemName = 'sword') where username = 'tan123';
#INSERT INTO ItemRel select  'tan123', characterID, 'shield',2 from ItemRel where username = 'tan123';



try:
    conn= mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                                              host=connection_info.MyHost,
                                                                database=connection_info.MyDatabase)

    conn.autocommit = False
    cursor = conn.cursor()
    '''
       Update amount of Items for a specific character within the Username
       (NOTE needs amount of items(var amount), var ItemName, var characterID, and var username to be passed in!)
       Ex: CHANGE
       username characterID ItemName amount               -->           username characterID  ItemName  amount
       tan123    123          sword    2                               tan123   123           sword     2+specified amount

       '''
    sql_update_query = 'UPDATE ItemRel set amount = amount+' + str(
        amount) + ' where username = \"' + username + '\" and ItemName = \"' + ItemName + '\" and characterID = \"'+characterID+'\"'

    '''
           Removing the item from every other characterID within the specified username 
           (NOTE needs amount of items(var amount), var ItemName, var characterID, and var username to be passed in!)
           Ex: CHANGE
           username characterID ItemName amount               -->           username characterID  ItemName  amount
           tan123    234         sword    2                               tan123      234          sword     2-specified amount
           '''
    sql_update_query = 'UPDATE ItemRel set amount = amount-' + str(
        amount) + ' where username = \"' + username + '\" and ItemName = \"' + ItemName + '\" and characterID != \"' + characterID + '\"'
    print("Record Updated successfully ")

    # Commit your changes
    conn.commit()

except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    # reverting changes because of exception
    conn.rollback()
finally:
    # closing database connection.
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("connection is closed")