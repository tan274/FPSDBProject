import mysql.connector

import connection_info




try:
    conn = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)

    conn.autocommit = False
    cursor = conn.cursor()
    characterID = 0  # for whichever characterID used
    skillName = ''  # name of skill inputted
    description = ''  # description of skill?
    damage = 0  # how much damage it does
    manaCost = 0  # how much mana it costs
    # how will damage/manaCost/description be determined?
    update_skillRel = "UPDATE skillRel SET column WHERE characterID = %d AND skillName = %s"
    val = (characterID, skillName)
    cursor.execute(update_skillRel, val)
    update_skills = "UPDATE skills SET column WHERE skillName = %s AND description = %s AND damage = %d AND manaCost = %d"
    val2 = (skillName, description, damage, manaCost)
    cursor.execute(update_skills, val2)

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

