import mysql.connector
import connection_info


try:
    conn = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                   host=connection_info.MyHost,
                                   database=connection_info.MyDatabase)

    conn.autocommit = False
    cursor = conn.cursor()
   #add 3 simply items (will change later)
    sql_update_query = '''
INSERT INTO Items  VALUES
('sword', 'a simple sword', 3, 1,15,5,10),
('dagger', 'a simple dagger',4 ,1,13,4,11),
('shield', 'a simple shield', 5,1,30, 10,2);
'''
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