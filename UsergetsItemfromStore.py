
'''


This is for when user gets items from store

'''
import mysql.connector
import connection_info

#Need user to specify these variables for user to obtain item
#username = 'tan123'
#ItemName= 'sword'
#amount = 2
#Curr ='normalCurr'
stritemcost= ""

if Curr == 'normalCurr':
    stritemcost = 'normalCost'
else:
    stritemcost = 'premiumCost'


print('UPDATE ItemRel set amount = amount+'+str(amount)+' where username = \"'+username+'\" and ItemName = \"'+ItemName+'\"')
print('INSERT INTO ItemRel  '+'select '+username+', characterID, '+ItemName+', '+str(amount)+' from ItemRel where username = \"'+username+'\"')
print('UPDATE Player SET ' + Curr + '= ' + Curr + '- ' + str(
        amount) + ' * (select ' + stritemcost + ' from Items where ItemName = \"' + ItemName + '\") where username = \"' + username + '\"')


try:
    conn= mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                                              host=connection_info.MyHost,
                                                                database=connection_info.MyDatabase)

    conn.autocommit = False
    cursor = conn.cursor()

    '''
    Update amount of Items for a username in ItemRel 
    (NOTE needs amount of items(var amount), var ItemName, and var username to be passed in!)
    Ex: CHANGE
    username characterID ItemName amount               -->           username characterID  ItemName  amount
    tan123    123          sword    2                               tan123   123           sword     2-specified amount
    
    '''
    sql_update_query = 'UPDATE ItemRel set amount = amount+'+str(amount)+' where username = \"'+username+'\" and ItemName = \"'+ItemName+'\"'
    cursor.execute(sql_update_query)
    error = cursor.fetchone()

    # If the previous query didn't do anything, insert new row into ItemRel
    '''
    INSERT NEW ROW INTO ITEMREL ONLY IF tan123 doesnt have sword already listed inside
    Ex: added into ItemRel
    username characterID ItemName amount                      
    tan123    123          sword    specified amount                               

    '''
    if error==None:
        sql_update_query = 'INSERT INTO ItemRel  '+'select '+username+', characterID, '+ItemName+', '+str(amount)+' from ItemRel where username = \"'+username+'\"'
        cursor.execute(sql_update_query)


    #Subtracting the item costs from Player total currency.
    '''
    UPDATE total specified currency in Player and subtract it from the amount of items requested
    (NOTE: needs to pass in whether user is using normalCurrency or premiumCurrency(var Curr)
    
    Ex:                                                                   Within   Items    
    username level normalCurr premiumCurr                                 ItemName   normalCost               
    tan123    34      126        67                                        sword       3
    normalCurr for tan123 would become 120 if user requested 2 swords to be bought
    '''
    sql_update_query = 'UPDATE Player SET ' + Curr + '= ' + Curr + '- ' + str(
        amount) + ' * (select ' + stritemcost + ' from Items where ItemName = \"' + ItemName + '\") where username = \"' + username + '\"'
    cursor.execute(sql_update_query)
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