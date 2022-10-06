'''


This is for when monster gets equipped certain amount of Items

'''

import mysql.connector
import connection_info
monstername = 'Giant troll'
amount = 2
ItemName = 'sword'


try:
    conn = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                   host=connection_info.MyHost,
                                   database=connection_info.MyDatabase)

    conn.autocommit = False
    cursor = conn.cursor()
    '''
       Update amount of Items for a monster
       (NOTE needs amount of items(var amount), var ItemName, var monstername to be passed in!)
       Ex: CHANGE
       monstername ItemName amount               -->           monstername ItemName  amount
        Giant troll  sword    2                                Giant troll sword     2+specified amount

       '''
    sql_update_query = 'UPDATE MonsterItems set amount = amount+' + str(
        amount) + ' where monsterName = \"' + monstername + '\" and ItemName = \"' + ItemName + '\" '
    cursor.execute(sql_update_query)


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