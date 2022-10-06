import math

import mysql.connector
import tkinter as tk

import connection_info

#NOTE: A large portion of this code was copied from, or heavily based on code from the following webpage:
#https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter



#def executeQuery(query):
#    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
#                              host=connection_info.MyHost,
#                              database=connection_info.MyDatabase)
#

    #cursor = cnx.cursor()
    #cursor.execute(query)

    #return cursor



options = ["Player", "Character", "Item", "Monster", "Skill", "Stage", "ItemRel", "SkillRel", "MonsterItems", "MonsterDrops", "MonsterSkills", "StageMonsters"]
updateOptions = ["Player", "Character", "Item", "Monster", "Skill", "Stage", "StageMonsters", "MonsterDrops"]
actionsOptions = ["Fight a Monster!", "Acquire Item From Monster", "Pick Strongest Skill!", "Buy an Item", "Equip an Item", 'Obtain player information as well as max amount of Items for a character', "Return players in order of net worth"]

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #for F in (StartPage, AddPageOne, RetrievePageOne, UpdatePageOne):
        for F in (StartPage, RetrievePageOne, AddPageOne, UpdatePageOne, ActionsPageOne, FightBQ, StrongestSkill, EquipItemPageOne,UserEquipItem,MonsterEquipItem, BuyItemPage, MaxItemAmountPage, PlayerUpdate, CharacterUpdate, ItemUpdate, MonsterUpdate, SkillUpdate, StageUpdate, StageMonstersUpdate, MonsterDropsUpdate, IFMDUpdate, PlayerAdd, CharacterAdd, ItemAdd, MonsterAdd, SkillAdd, StageAdd, ItemRelAdd, SkillRelAdd, MonsterItemsAdd, MonsterDropsAdd, MonsterSkillsAdd, StageMonstersAdd, PlayerRetrieve, CharacterRetrieve, ItemRetrieve, MonsterRetrieve, MonsterSkillretrieve, SkillRelRetrieve, SkillRetrieve, StageRetrieve, StageMonstersRetrieve, MonsterDropsRetrieve, PlayersNetWorth):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Would you like to add, retrieve, update, or run an action?")
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Add Something",
                            command=lambda: controller.show_frame("AddPageOne"))
        button2 = tk.Button(self, text="Retrieve Something",
                            command=lambda: controller.show_frame("RetrievePageOne"))
        button3 = tk.Button(self, text="Update Something",
                            command=lambda: controller.show_frame("UpdatePageOne"))
        button4 = tk.Button(self, text="Actions",
                            command=lambda: controller.show_frame("ActionsPageOne"))
        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()


class AddPageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="What would you like to add?")
        label.pack(side="top", fill="x", pady=10)


        variable = tk.StringVar(self)
        variable.set(options[0])

        dropDown = tk.OptionMenu(self, variable, *options)
        dropDown.pack()

        def APOOk():
            if (variable.get() == "Player"):
                controller.show_frame("PlayerAdd")
            elif (variable.get() == "Character"):
                controller.show_frame("CharacterAdd")
            elif (variable.get() == "Item"):
                controller.show_frame("ItemAdd")
            elif (variable.get() == "Monster"):
                controller.show_frame("MonsterAdd")
            elif (variable.get() == "Skill"):
                controller.show_frame("SkillAdd")
            elif (variable.get() == "Stage"):
                controller.show_frame("StageAdd")
            elif (variable.get() == "ItemRel"):
                controller.show_frame("ItemRelAdd")
            elif (variable.get() == "SkillRel"):
                controller.show_frame("SkillRelAdd")
            elif (variable.get() == "MonsterItems"):
                controller.show_frame("MonsterItemsAdd")
            elif (variable.get() == "MonsterDrops"):
                controller.show_frame("MonsterDropsAdd")
            elif (variable.get() == "MonsterSkills"):
                controller.show_frame("MonsterSkillsAdd")
            else:
                controller.show_frame("StageMonstersAdd")

        button2 = tk.Button(self, text="OK", command=APOOk)
        button2.pack()


        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()




class PlayerAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding a Player:")
        label.pack(side="top", fill="x", pady=10)




        def addPlayer():

            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()



            varUsername = username.get("1.0", "end-1c")
            varLevel = level.get("1.0", "end-1c")
            varNormalCurr = normalCurr.get("1.0", "end-1c")
            varPremiumCurr = premiumCurr.get("1.0", "end-1c")

            valid = True
            if (varUsername == ""):
                print("Please specify a username!")
                return
            else:
                testUniqueUsernameQuery = "SELECT * FROM Player WHERE username = \"" + varUsername + "\";"
                cursor.execute(testUniqueUsernameQuery)


                areAny = False
                for retVal in cursor:
                    areAny = True
                    #print(retVal)

                if (areAny):
                    print("Username already taken! Please specify a unique username.")
                    return


            if (varLevel == ""):
                varLevel = "1"
                print("Starting Level defaulting to 1")
            elif (not varLevel.isnumeric()):
                print("Please put a positive integer for starting level.")
                return
            elif (int(varLevel) < 1):
                print("Please put a positive integer for starting level.")
                return



            if (varNormalCurr == ""):
                varNormalCurr = "1000"
                print("Starting Normal Currency defaulting to 1000")
            elif (not varNormalCurr.isnumeric()):
                print("Please put a non-negative integer for starting currency.")
                return
            elif (int(varNormalCurr) < 0):
                print("Please put a non-negative integer for starting currency.")
                return


            if (varPremiumCurr == ""):
                varPremiumCurr = "0"
                print("Starting Premium Currency defaulting to 0")
            elif (not varPremiumCurr.isnumeric()):
                print("Please put a non-negative integer for starting currency.")
                return
            elif (int(varPremiumCurr) < 0):
                print("Please put a non-negative integer for starting currency.")
                return

            query = "INSERT INTO Player (username, level, normalCurr, premiumCurr) VALUES (\"" + varUsername + "\",  \"" + varLevel + "\", \"" + varNormalCurr + "\", \"" + varPremiumCurr + "\");"

            try:
                cursor.execute(query)
                cnx.commit()

                print("User: " + varUsername + " successfully added!")
            except:
                print("Error - Aborted")
                cnx.rollback()
            finally:
                cursor.close()
                cnx.close()




        usernameLabel = tk.Label(self, text="Username:")
        usernameLabel.pack()

        username = tk.Text(self, height=1)
        username.pack()

        levelLabel = tk.Label(self, text="Starting Level (default 1):")
        levelLabel.pack()

        level = tk.Text(self, height=1)
        level.pack()

        normalCurrLabel = tk.Label(self, text="Starting Normal Currency (default 1000):")
        normalCurrLabel.pack()

        normalCurr = tk.Text(self, height=1)
        normalCurr.pack()

        premiumCurrLabel = tk.Label(self, text="Starting Premium Currency (default 0):")
        premiumCurrLabel.pack()

        premiumCurr = tk.Text(self, height=1)
        premiumCurr.pack()






        button2 = tk.Button(self, text="Go!",
                            command=lambda: addPlayer())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()





class CharacterAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding a Character:")
        label.pack(side="top", fill="x", pady=10)

        def addCharacter():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()

            varCharacterName = characterName.get("1.0", "end-1c")
            varOwnerName = ownerName.get("1.0", "end-1c")
            varLevel = level.get("1.0", "end-1c")
            varHealth = health.get("1.0", "end-1c")
            varDefense = defense.get("1.0", "end-1c")
            varAttack = attack.get("1.0", "end-1c")
            varMana = mana.get("1.0", "end-1c")


            seeIfUserExists = "SELECT * FROM Player WHERE username = \"" + varOwnerName + "\";"
            cursor.execute(seeIfUserExists)

            exists = False
            for retVal in cursor:
                exists = True

            if (not exists):
                print("A user with the name: " + varOwnerName + "does not exist.")
                return

            seeIfCharacterAlreadyOwned = "SELECT * FROM Characters WHERE characterName = \"" + varCharacterName + "\" AND ownerName = \"" +  varOwnerName + "\";"

            cursor.execute(seeIfCharacterAlreadyOwned)

            exists = False
            for retVal in cursor:
                exists = True

            if (exists):
                print("This character is already owned by that player.")
                return

            query = "INSERT INTO Characters VALUES (\"" + varCharacterName + "\", \"" + varOwnerName + "\", " + varLevel + ", " + varHealth + ", " + varDefense + ", " + varAttack + ", " + varMana + ");"
            #print(query)

            try:
                cursor.execute(query)
                cnx.commit()
                print("Character successfully added")

            except:
                cnx.rollback()

            for retVal in cursor:
                print(retVal)

            cursor.close()
            cnx.close()

        characterNameLabel = tk.Label(self, text="Character Name:")
        characterNameLabel.pack()

        characterName = tk.Text(self, height=1)
        characterName.pack()

        ownerNameLabel = tk.Label(self, text="Owner Name:")
        ownerNameLabel.pack()

        ownerName = tk.Text(self, height=1)
        ownerName.pack()



        varLevelLabel = tk.Label(self, text="Character Level:")
        varLevelLabel.pack()

        level = tk.Text(self, height=1)
        level.pack()


        varHealthLabel = tk.Label(self, text="Character Health:")
        varHealthLabel.pack()

        health = tk.Text(self, height=1)
        health.pack()



        varDefenseLabel = tk.Label(self, text="Character Defense:")
        varDefenseLabel.pack()

        defense = tk.Text(self, height=1)
        defense.pack()



        varAttackLabel = tk.Label(self, text="Character Attack:")
        varAttackLabel.pack()

        attack = tk.Text(self, height=1)
        attack.pack()



        varManaLabel = tk.Label(self, text="Character Mana:")
        varManaLabel.pack()

        mana = tk.Text(self, height=1)
        mana.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: addCharacter())
        button2.pack()











        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()










class ItemAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding an Item:")
        label.pack(side="top", fill="x", pady=10)




        def addItem():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                            host=connection_info.MyHost,
                            database=connection_info.MyDatabase)

            cursor = cnx.cursor()

            varItemName = itemName.get("1.0", "end-1c")
            varDescription = description.get("1.0", "end-1c")
            varNormalCost = normalCost.get("1.0", "end-1c")
            varPremiumCost = premiumCost.get("1.0", "end-1c")
            varHealth = health.get("1.0", "end-1c")
            varDefense = defense.get("1.0", "end-1c")
            varAttack = attack.get("1.0", "end-1c")


            #VULNERABLE TO SQL INJECTION
            #Replace with prepared statement.
            query = "INSERT INTO Items (itemName, description, normalCost, premiumCost, health, defense, attack) VALUES (\"" + varItemName + "\", \"" + varDescription + "\", " + varNormalCost + ", " + varPremiumCost + ", " + varHealth + ", " + varDefense + ", " + varAttack + ");"
            print(query)

            try:
                cursor.execute(query)

                cnx.commit()
            except:
                cnx.rollback()

            for retVal in cursor:
                print(retVal)


            cursor.close()
            cnx.close()




        itemNameLabel = tk.Label(self, text="Item Name:")
        itemNameLabel.pack()

        itemName = tk.Text(self, height=1)
        itemName.pack()


        descriptionLabel = tk.Label(self, text="Description:")
        descriptionLabel.pack()

        description = tk.Text(self, height=10)
        description.pack()



        normalCostLabel = tk.Label(self, text="Normal Cost:")
        normalCostLabel.pack()

        normalCost = tk.Text(self, height=1)
        normalCost.pack()


        premiumCostLabel = tk.Label(self, text="Premium Cost:")
        premiumCostLabel.pack()

        premiumCost = tk.Text(self, height=1)
        premiumCost.pack()


        healthLabel = tk.Label(self, text="Item Health:")
        healthLabel.pack()

        health = tk.Text(self, height=1)
        health.pack()



        defenseLabel = tk.Label(self, text="Item Defense:")
        defenseLabel.pack()

        defense = tk.Text(self, height=1)
        defense.pack()


        attackLabel = tk.Label(self, text="Item Attack:")
        attackLabel.pack()

        attack = tk.Text(self, height=1)
        attack.pack()






        button2 = tk.Button(self, text="Go!",
                            command=lambda: addItem())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()


class MonsterAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding a Monster:")
        label.pack(side="top", fill="x", pady=10)

        def addMonster():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            try:

                cnx.autocommit = False
                cursor = cnx.cursor()
                cnx.start_transaction(isolation_level='SERIALIZABLE')

                varMonsterName = monsterNameInput.get("1.0", "end-1c")
                varMonsterLevel = monsterLevelInput.get("1.0", "end-1c")
                varMonsterHealth = monsterHealthInput.get("1.0", "end-1c")
                varMonsterDefense = monsterDefenseInput.get("1.0", "end-1c")
                varMonsterAttack = monsterAttackInput.get("1.0", "end-1c")


                # Insert for new Monster
                cursor.execute("INSERT INTO Monsters(monsterName, level, health, defense, attack) VALUES ('%s', '%d', '%d', '%d', '%d');" % (varMonsterName, int(varMonsterLevel), int(varMonsterHealth), int(varMonsterDefense), int(varMonsterAttack)))

                # Commit your changes
                cnx.commit()

                print("Insertion successful.")

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

        monsterNameLabel = tk.Label(self, text="Monster Name:")
        monsterNameLabel.pack()

        monsterNameInput = tk.Text(self, height=1, width=20)
        monsterNameInput.pack()

        monsterLevelLabel = tk.Label(self, text="Monster Level:")
        monsterLevelLabel.pack()

        monsterLevelInput = tk.Text(self, height=1, width=5)
        monsterLevelInput.pack()

        monsterHealthLabel = tk.Label(self, text="Monster Health:")
        monsterHealthLabel.pack()

        monsterHealthInput = tk.Text(self, height=1, width=5)
        monsterHealthInput.pack()

        monsterDefenseLabel = tk.Label(self, text="Monster Defense:")
        monsterDefenseLabel.pack()

        monsterDefenseInput = tk.Text(self, height=1, width=5)
        monsterDefenseInput.pack()

        monsterAttackLabel = tk.Label(self, text="Monster Attack:")
        monsterAttackLabel.pack()

        monsterAttackInput = tk.Text(self, height=1, width=5)
        monsterAttackInput.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: addMonster())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()


class SkillRelAdd(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding a Skill For a Character:")
        label.pack(side="top", fill="x", pady=10)

        def addSkillRel():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')

            varCharacterName = characterName.get("1.0", "end-1c")
            varSkillName = skillName.get("1.0", "end-1c")

            if varCharacterName == "":
                print("Please specify a character name!")
                return
            elif varSkillName == "":
                print("Please specify a skill name!")
                return
            else:
                query = "INSERT INTO SkillRel(characterName, skillName) VALUES ('%s', '%s')" % (varCharacterName, varSkillName)
                cursor.execute(query)

            cursor.callproc("GetSkillRel", [varCharacterName])

            results = [r.fetchall() for r in cursor.stored_results()]
            for i in range(len(results[0])):
                print(results[0][i])


        characterNameLabel = tk.Label(self, text="Character Name:")
        characterNameLabel.pack()

        characterName = tk.Text(self, height=1)
        characterName.pack()

        skillNameLabel = tk.Label(self, text="Skill Name:")
        skillNameLabel.pack()

        skillName = tk.Text(self, height=1)
        skillName.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: addSkillRel())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()


class SkillAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding a Skill:")
        label.pack(side="top", fill="x", pady=10)

        def addSkill():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')

            varSkillName = skillName.get("1.0", "end-1c")
            varDescription = description.get("1.0", "end-1c")
            varDamage = damage.get("1.0", "end-1c")
            varManaCost = manaCost.get("1.0", "end-1c")

            # VULNERABLE TO SQL INJECTION
            # Replace with prepared statement.
            query = "INSERT INTO Skills (skillName, description, damage, manaCost) VALUES ('%s', '%s', '%s', '%s');" % (
                varSkillName, varDescription, varDamage, varManaCost)
            cursor.execute(query)
            cursor.callproc("GetSkills", [varSkillName])

            results = [r.fetchall() for r in cursor.stored_results()]
            for i in range(len(results[0])):
                print(results[0][i])

            cursor.close()
            cnx.close()

        skillNameLabel = tk.Label(self, text="Skill Name:")
        skillNameLabel.pack()

        skillName = tk.Text(self, height=1)
        skillName.pack()

        descriptionLabel = tk.Label(self, text="Description:")
        descriptionLabel.pack()

        description = tk.Text(self, height=1)
        description.pack()

        damageLabel = tk.Label(self, text="Damage:")
        damageLabel.pack()

        damage = tk.Text(self, height=1)
        damage.pack()

        manaCostLabel = tk.Label(self, text="Mana Cost:")
        manaCostLabel.pack()

        manaCost = tk.Text(self, height=1)
        manaCost.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: addSkill())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()


class StageAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding a Stage:")
        label.pack(side="top", fill="x", pady=10)

        def addStage():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            try:

                cnx.autocommit = False
                cursor = cnx.cursor()
                cnx.start_transaction(isolation_level='SERIALIZABLE')

                varStageName = stageNameInput.get("1.0", "end-1c")
                varStageDescription = stageDescriptionInput.get("1.0", "end-1c")

                # Insert for new Stage
                cursor.execute("INSERT INTO Stage(stageName, stageDescription) VALUES ('%s', '%s');" %
                               (varStageName, varStageDescription))

                # Commit your changes
                cnx.commit()

                print("Insertion successful.")

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

        stageNameLabel = tk.Label(self, text="Stage Name:")
        stageNameLabel.pack()

        stageNameInput = tk.Text(self, height=1, width=20)
        stageNameInput.pack()

        stageDescriptionLabel = tk.Label(self, text="Stage Description:")
        stageDescriptionLabel.pack()

        stageDescriptionInput = tk.Text(self, height=5, width=40)
        stageDescriptionInput.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: addStage())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()


class ItemRelAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding to ItemRel:")
        label.pack(side="top", fill="x", pady=10)

        def addItemRel():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')

            varusername = username.get("1.0", "end-1c")
            varcharacterID = characterID.get("1.0", "end-1c")
            varItemName = itemname.get("1.0", "end-1c")
            varamount = amount.get("1.0", "end-1c")



            query = "INSERT INTO ItemRel (username, characterName, ItemName, amount) VALUES (\"" + varusername + "\", \"" + varcharacterID + "\", \"" + varItemName + "\", \"" + varamount + "\");"
            print(query)

            try:
                cursor.execute(query)

                cnx.commit()
            except:
                cnx.rollback()
            cursor.execute('select * from ItemRel')
            for retVal in cursor:
                print(retVal)

            cursor.close()
            cnx.close()

        usernameLabel = tk.Label(self, text="Username:")
        usernameLabel.pack()
        username = tk.Text(self, height=1)
        username.pack()

        characterIDLabel = tk.Label(self, text="Character ID:")
        characterIDLabel.pack()
        characterID = tk.Text(self, height=1)
        characterID.pack()

        itemnameLabel = tk.Label(self, text="Item Name:")
        itemnameLabel.pack()
        itemname = tk.Text(self, height=1)
        itemname.pack()

        amountLabel = tk.Label(self, text="Amount:")
        amountLabel.pack()
        amount = tk.Text(self, height=1)
        amount.pack()


        button2 = tk.Button(self, text="Go!",
                            command=lambda: addItemRel())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()


class MonsterItemsAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding an Monster Item:")
        label.pack(side="top", fill="x", pady=10)

        def addItem():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')

            varmonstername = monstername.get("1.0", "end-1c")
            varamount = amount.get("1.0", "end-1c")

            varItemName = itemName.get("1.0", "end-1c")


            # VULNERABLE TO SQL INJECTION
            # Replace with prepared statement.
            query = "INSERT INTO MonsterItems (monsterName, itemName, amount) VALUES (\"" + varmonstername + "\", \"" + varItemName + "\", " + str(varamount) + ");"
            print(query)

            try:
                cursor.execute(query)

                cnx.commit()
            except:
                cnx.rollback()
            cursor.execute('select * from MonsterItems')

            for retVal in cursor:
                print(retVal)

            cursor.close()
            cnx.close()
        monsternameLabel = tk.Label(self, text="MonsterName:")
        monsternameLabel.pack()
        monstername = tk.Text(self, height=1)
        monstername.pack()

        itemNameLabel = tk.Label(self, text="Item Name:")
        itemNameLabel.pack()
        itemName = tk.Text(self, height=1)
        itemName.pack()



        amountLabel = tk.Label(self, text="Amount:")
        amountLabel.pack()
        amount = tk.Text(self, height=1)
        amount.pack()



        button2 = tk.Button(self, text="Go!",
                            command=lambda: addItem())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()


class MonsterDropsAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding to MonsterDrops:")
        label.pack(side="top", fill="x", pady=10)

        def addMonsterDrop():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            try:

                cnx.autocommit = False
                cursor = cnx.cursor()
                cnx.start_transaction(isolation_level='SERIALIZABLE')

                varMonsterName = monsterNameInput.get("1.0", "end-1c")
                varItemName = itemNameInput.get("1.0", "end-1c")
                varAmount = amountInput.get("1.0", "end-1c")

                # Insert for new Stage
                cursor.execute("INSERT INTO MonsterDrops(monsterDropID, monsterName, itemName, amount) VALUES (NULL, '%s', '%s', '%d');" %
                               (varMonsterName, varItemName, int(varAmount)))

                # Commit your changes
                cnx.commit()

                print("Insertion successful.")

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

        monsterNameLabel = tk.Label(self, text="Monster Name:")
        monsterNameLabel.pack()

        monsterNameInput = tk.Text(self, height=1, width=20)
        monsterNameInput.pack()

        itemNameLabel = tk.Label(self, text="Item Name:")
        itemNameLabel.pack()

        itemNameInput = tk.Text(self, height=1, width=20)
        itemNameInput.pack()

        amountLabel = tk.Label(self, text="Amount:")
        amountLabel.pack()

        amountInput = tk.Text(self, height=1, width=5)
        amountInput.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: addMonsterDrop())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()


class MonsterSkillsAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding to MonsterSkills:")
        label.pack(side="top", fill="x", pady=10)

        def addMonsterSkill():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')

            varMonsterName = monsterName.get("1.0", "end-1c")
            varSkillName = skillName.get("1.0", "end-1c")

            cursor.execute("INSERT INTO MonsterSkills(monsterName, skillName) VALUES ('%s', '%s')" % (
            varMonsterName, varSkillName))

            cursor.callproc("GetMonsterSkills", [varMonsterName])

            results = [r.fetchall() for r in cursor.stored_results()]
            for i in range(len(results[0])):
                print(results[0][i])

        monsterNameLabel = tk.Label(self, text="Monster Name:")
        monsterNameLabel.pack()

        monsterName = tk.Text(self, height=1)
        monsterName.pack()

        skillNameLabel = tk.Label(self, text="Skill Name:")
        skillNameLabel.pack()

        skillName = tk.Text(self, height=1)
        skillName.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: addMonsterSkill())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()


class StageMonstersAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Adding to StageMonsters:")
        label.pack(side="top", fill="x", pady=10)

        def addStageMonsters():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            try:

                cnx.autocommit = False
                cursor = cnx.cursor()
                cnx.start_transaction(isolation_level='SERIALIZABLE')

                varStageName = stageNameInput.get("1.0", "end-1c")
                varMonsterName = monsterNameInput.get("1.0", "end-1c")
                varAmount = amountInput.get("1.0", "end-1c")

                # Insert for new Stage
                cursor.execute(
                    "INSERT INTO StageMonsters(stageName, monsterName, amount) VALUES ('%s', '%s', '%d');" %
                    (varStageName, varMonsterName, int(varAmount)))

                # Commit your changes
                cnx.commit()

                print("Insertion successful.")

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

        stageNameLabel = tk.Label(self, text="Stage Name:")
        stageNameLabel.pack()

        stageNameInput = tk.Text(self, height=1, width=20)
        stageNameInput.pack()

        monsterNameLabel = tk.Label(self, text="Monster Name:")
        monsterNameLabel.pack()

        monsterNameInput = tk.Text(self, height=1, width=20)
        monsterNameInput.pack()

        amountLabel = tk.Label(self, text="Amount:")
        amountLabel.pack()

        amountInput = tk.Text(self, height=1, width=5)
        amountInput.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: addStageMonsters())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("AddPageOne"))
        button.pack()


















class RetrievePageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="What would you like to retrieve?")
        label.pack(side="top", fill="x", pady=10)


        variable = tk.StringVar(self)
        variable.set(options[0])

        dropDown = tk.OptionMenu(self, variable, *options)
        dropDown.pack()

        def RPOOk():
            if (variable.get() == "Player"):
                controller.show_frame("PlayerRetrieve")
            elif (variable.get() == "Character"):
                controller.show_frame("CharacterRetrieve")
            elif (variable.get() == "Item"):
                controller.show_frame("ItemRetrieve")
            elif (variable.get() == "Monster"):
                controller.show_frame("MonsterRetrieve")
            elif (variable.get() == "Skill"):
                controller.show_frame("SkillRetrieve")
            elif (variable.get() == "SkillRel"):
                controller.show_frame("SkillRelRetrieve")
            elif (variable.get() == "MonsterSkills"):
                controller.show_frame("MonsterSkillretrieve")
            elif (variable.get() == "Stage"):
                controller.show_frame("StageRetrieve")
            elif (variable.get() == "MonsterDrops"):
                controller.show_frame("MonsterDropsRetrieve")
            elif (variable.get() == "StageMonsters"):
                controller.show_frame("StageMonstersRetrieve")

        button2 = tk.Button(self, text="OK", command=RPOOk)
        button2.pack()


        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()




class PlayerRetrieve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Retrieving a Player:")
        label.pack(side="top", fill="x", pady=10)




        def retrievePlayer():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='READ COMMITTED')
            query = "SELECT * FROM Player;"

            usernameVar = usernameInput.get("1.0", "end-1c")

            if (usernameVar != ""):
                query = "SELECT * FROM Player WHERE username = \"" + usernameVar + "\";"

            try:
                cursor.execute(query)

                any = False
                print("(Username, Level, Normal Currency, Premium Currency)")
                for retVal in cursor:
                    any = True
                    #print(len(retVal))
                    #print("Username: " + retVal[0] + "; Level: " + retVal[1])
                    print(retVal)


                if (not any):
                    print("No results found.")
            except:
                cnx.rollback()
            return







        usernameLabel = tk.Label(self, text="Username (Leave empty to display all users):")
        usernameLabel.pack()

        usernameInput = tk.Text(self, height=1)
        usernameInput.pack()


        button2 = tk.Button(self, text="Go!",
                           command=lambda: retrievePlayer())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("RetrievePageOne"))
        button.pack()


class CharacterRetrieve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Retrieving a Character (Leave both fields empty to retrieve all characters):")
        label.pack(side="top", fill="x", pady=10)



        def retrieveCharacters():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()

            cnx.start_transaction(isolation_level='READ COMMITTED')

            characterVar = characterInput.get("1.0", "end-1c")
            usernameVar = usernameInput.get("1.0", "end-1c")

            query = "SELECT * FROM Characters"

            if (characterVar != ""):
                query += " WHERE characterName = \"" + characterVar + "\""
                if (usernameVar != ""):
                    query += " AND ownerName = \"" + usernameVar + "\""
            elif(usernameVar != ""):
                query += " WHERE ownerName = \"" + usernameVar + "\""

            query += ";"

            try:
                cursor.execute(query)

                any = False
                print("(Character Name, Owner Username, Level, Health, Defense, Attack, Mana)")
                for retVal in cursor:
                    any = True
                    #print(len(retVal))
                    #print("Username: " + retVal[0] + "; Level: " + retVal[1])
                    print(retVal)


                if (not any):
                    print("No results found.")
            except:
                cnx.rollback()
            return




        characterLabel = tk.Label(self, text="Character Name (Leave empty to display all characters owned by the below user):")
        characterLabel.pack()

        characterInput = tk.Text(self, height=1)
        characterInput.pack()


        usernameLabel = tk.Label(self, text="Username (Leave empty to display all users that own the above character):")
        usernameLabel.pack()

        usernameInput = tk.Text(self, height=1)
        usernameInput.pack()



        button2 = tk.Button(self, text="Go!",
                            command=lambda: retrieveCharacters())

        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("RetrievePageOne"))
        button.pack()








class ItemRetrieve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Retrieving an Item:")
        label.pack(side="top", fill="x", pady=10)
        cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                      host=connection_info.MyHost,
                                      database=connection_info.MyDatabase)
        cursor = cnx.cursor()
        cnx.start_transaction(isolation_level='READ COMMITTED')

        varItemName = 'itemnameonly'
        cursor.callproc("GetItems", [varItemName])
        results = [r.fetchall() for r in cursor.stored_results()]
        itemlist = [i[0] for i in results[0]]
        tempitem = tk.StringVar(self)
        tempitem.set(itemlist[0])
        Itemlabel = tk.Label(self, text="Item Name")
        Itemlabel.pack()
        dropDown2 = tk.OptionMenu(self, tempitem, *itemlist)
        dropDown2.pack()




        def getResults():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                            host=connection_info.MyHost,
                            database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            varItemName = tempitem.get()
            cursor.callproc("GetItems", [varItemName])
            results = [r.fetchall() for r in cursor.stored_results()]
            final_result = [i for i in results[0]]
            for i in final_result:
                print(i)


            cursor.close()
            cnx.close()







        button2 = tk.Button(self, text="Go!",
                            command=lambda: getResults())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("RetrievePageOne"))
        button.pack()








class MonsterRetrieve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Retrieving a Monster:")
        label.pack(side="top", fill="x", pady=10)

        infoArray = []

        def applytoLabel():
            n = len(infoArray)
            element = ''
            for i in range(n):
                element = element + infoArray[i] + '\n'
            return element

        def getResults():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            try:

                cnx.autocommit = False
                cursor = cnx.cursor()
                cnx.start_transaction(isolation_level='READ COMMITTED')

                varMonsterName = monsterNameInput.get("1.0", "end-1c")

                # Using stored procedure to select for choosing all monsters created so far
                cursor.callproc("GetMonsters", [varMonsterName])

                results = [r.fetchall() for r in cursor.stored_results()]

                # Create array that holds monster values for printing on label
                for i in range(len(results[0])):
                    infoArray.append(results[0][i][0] + ", " + str(results[0][i][1]) + ", " + str(results[0][i][2]) + ", " + str(results[0][i][3]) + ", " + str(results[0][i][4]))

                # Commit your changes
                cnx.commit()

                print("Retrieve successful.")

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

            label.config(text=applytoLabel())
            infoArray.clear()

        monsterNameLabel = tk.Label(self, text="Monster Name:")
        monsterNameLabel.pack()

        monsterNameInput = tk.Text(self, height=1)
        monsterNameInput.pack()

        dataLabel = tk.Label(self, text=applytoLabel())
        dataLabel.pack(pady=10)

        button2 = tk.Button(self, text="Go!",
                            command=lambda: getResults())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("RetrievePageOne"))
        button.pack()


class SkillRetrieve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Retrieving a Skill:")
        label.pack(side="top", fill="x", pady=10)

        def getSkills():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='READ COMMITTED')

            varSkillName = skillName.get("1.0", "end-1c")
            cursor.callproc("GetSkills", [varSkillName])

            results = [r.fetchall() for r in cursor.stored_results()]
            for i in range(len(results[0])):
                print(results[0][i])

            cursor.close()
            cnx.close()

        skillNameLabel = tk.Label(self, text="Skill Name:")
        skillNameLabel.pack()

        skillName = tk.Text(self, height=1)
        skillName.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: getSkills())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("RetrievePageOne"))
        button.pack()

class SkillRelRetrieve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Retrieving a Skill for Character:")
        label.pack(side="top", fill="x", pady=10)

        def getSkillRel():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='READ COMMITTED')

            varCharacterName = characterName.get("1.0", "end-1c")
            cursor.callproc("GetSkillRel", [varCharacterName])

            results = [r.fetchall() for r in cursor.stored_results()]
            for i in range(len(results[0])):
                print(results[0][i])

            cursor.close()
            cnx.close()

        characterNameLabel = tk.Label(self, text="Character Name:")
        characterNameLabel.pack()

        characterName = tk.Text(self, height=1)
        characterName.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: getSkillRel())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("RetrievePageOne"))
        button.pack()


class MonsterSkillretrieve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Retrieving a Skill for Monster:")
        label.pack(side="top", fill="x", pady=10)

        def getMonsterSkills():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='READ COMMITTED')

            varMonsterName = monsterName.get("1.0", "end-1c")
            cursor.callproc("GetMonsterSkills", [varMonsterName])

            results = [r.fetchall() for r in cursor.stored_results()]
            for i in range(len(results[0])):
                print(results[0][i])

            cursor.close()
            cnx.close()

        monsterNameLabel = tk.Label(self, text="Monster Name:")
        monsterNameLabel.pack()

        monsterName = tk.Text(self, height=1)
        monsterName.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: getMonsterSkills())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("RetrievePageOne"))
        button.pack()


class StageRetrieve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Retrieving a Stage:")
        label.pack(side="top", fill="x", pady=10)

        infoArray = []

        def applytoLabel():
            n = len(infoArray)
            element = ''
            for i in range(n):
                element = element + infoArray[i] + '\n'
            return element

        def getResults():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            try:

                cnx.autocommit = False
                cursor = cnx.cursor()
                cnx.start_transaction(isolation_level='READ COMMITTED')

                varStageName = stageNameInput.get("1.0", "end-1c")

                # Using stored procedure to select for choosing all stages created so far
                cursor.callproc("GetStages", [varStageName])

                results = [r.fetchall() for r in cursor.stored_results()]

                # Create array that holds stage values for printing on label
                for i in range(len(results[0])):
                    infoArray.append(results[0][i][0] + ": " + str(results[0][i][1]))

                # Commit your changes
                cnx.commit()

                print("Retrieve successful.")

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

            label.config(text=applytoLabel())
            infoArray.clear()

        stageNameLabel = tk.Label(self, text="Stage Name:")
        stageNameLabel.pack()

        stageNameInput = tk.Text(self, height=1)
        stageNameInput.pack()

        dataLabel = tk.Label(self, text="")
        dataLabel.pack(pady=10)

        button2 = tk.Button(self, text="Go!",
                            command=lambda: getResults())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("RetrievePageOne"))
        button.pack()


class MonsterDropsRetrieve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Retrieving MonsterDrops:")
        label.pack(side="top", fill="x", pady=10)

        infoArray = []

        def applytoLabel():
            n = len(infoArray)
            element = ''
            for i in range(n):
                element = element + infoArray[i] + '\n'
            return element

        def getResults():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            try:

                cnx.autocommit = False
                cursor = cnx.cursor()
                cnx.start_transaction(isolation_level='READ COMMITTED')

                varMonsterName = monsterNameInput.get("1.0", "end-1c")

                if varMonsterName == "":
                    cursor.execute("SELECT * FROM MonsterDrops;")
                else:
                    cursor.execute("SELECT * FROM MonsterDrops WHERE monsterName = '%s';" % varMonsterName)

                for (monsterDropID, monsterName, itemName, amount) in cursor:
                    infoArray.append(monsterName + " has " + str(amount) + " " + itemName + "s")

                # Commit your changes
                cnx.commit()

                print("Retrieve successful.")

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

            label.config(text=applytoLabel())
            infoArray.clear()

        monsterNameLabel = tk.Label(self, text="Monster Name:")
        monsterNameLabel.pack()

        monsterNameInput = tk.Text(self, height=1)
        monsterNameInput.pack()

        dataLabel = tk.Label(self, text="")
        dataLabel.pack(pady=10)

        button2 = tk.Button(self, text="Go!",
                            command=lambda: getResults())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("RetrievePageOne"))
        button.pack()


class StageMonstersRetrieve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Retrieving a Stage:")
        label.pack(side="top", fill="x", pady=10)

        infoArray = []

        def applytoLabel():
            n = len(infoArray)
            element = ''
            for i in range(n):
                element = element + infoArray[i] + '\n'
            return element

        def getResults():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            try:

                cnx.autocommit = False
                cursor = cnx.cursor()
                cnx.start_transaction(isolation_level='READ COMMITTED')

                varStageName = stageNameInput.get("1.0", "end-1c")

                if varStageName == "":
                    cursor.execute("SELECT * FROM StageMonsters;")
                else:
                    cursor.execute("SELECT * FROM StageMonsters WHERE stageName = '%s';" % varStageName)

                for (stageName, monsterName, amount) in cursor:
                    infoArray.append(stageName + " has " + str(amount) + " " + monsterName + "s")

                # Commit your changes
                cnx.commit()

                print("Retrieve successful.")

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

            label.config(text=applytoLabel())
            infoArray.clear()

        stageNameLabel = tk.Label(self, text="Stage Name:")
        stageNameLabel.pack()

        stageNameInput = tk.Text(self, height=1)
        stageNameInput.pack()

        dataLabel = tk.Label(self, text="")
        dataLabel.pack(pady=10)

        button2 = tk.Button(self, text="Go!",
                            command=lambda: getResults())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("RetrievePageOne"))
        button.pack()








class UpdatePageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="What would you like to update?")
        label.pack(side="top", fill="x", pady=10)

        variable = tk.StringVar(self)
        variable.set(updateOptions[0])

        dropDown = tk.OptionMenu(self, variable, *updateOptions)
        dropDown.pack()

        def UPOOk():
            if (variable.get() == "Player"):
                controller.show_frame("PlayerUpdate")
            elif (variable.get() == "Character"):
                controller.show_frame("CharacterUpdate")
            elif (variable.get() == "Item"):
                controller.show_frame("ItemUpdate")
            elif (variable.get() == "Monster"):
                controller.show_frame("MonsterUpdate")
            elif (variable.get() == "Skill"):
                controller.show_frame("SkillUpdate")
            elif (variable.get() == "Stage"):
                controller.show_frame("StageUpdate")
            elif (variable.get() == "StageMonsters"):
                controller.show_frame("StageMonstersUpdate")
            elif (variable.get() == "MonsterDrops"):
                controller.show_frame("MonsterDropsUpdate")

        button2 = tk.Button(self, text="OK", command=UPOOk)
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PlayerUpdate(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Updating a Player:")
        label.pack(side="top", fill="x", pady=10)





        def addPlayer():

            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')


            varUsername = username.get("1.0", "end-1c")
            varLevel = level.get("1.0", "end-1c")
            varNormalCurr = normalCurr.get("1.0", "end-1c")
            varPremiumCurr = premiumCurr.get("1.0", "end-1c")

            valid = True
            if (varUsername == ""):
                print("Please specify a username!")
                return
            else:
                testUniqueUsernameQuery = "SELECT * FROM Player WHERE username = \"" + varUsername + "\";"
                cursor.execute(testUniqueUsernameQuery)


                areAny = False
                for retVal in cursor:
                    areAny = True
                    #print(retVal)

                if (not areAny):
                    print("No user with that username exists.")
                    return


            if (varLevel == ""):
                print("Please put a positive integer for level.")
                return
            elif (not varLevel.isnumeric()):
                print("Please put a positive integer for level.")
            elif (int(varLevel) < 1):
                print("Please put a positive integer for level.")
                return



            if (varNormalCurr == ""):
                print("Please put a non-negative integer for currency.")
                return
            elif (not varNormalCurr.isnumeric()):
                print("Please put a non-negative integer for currency.")
                return
            elif (int(varNormalCurr) < 0):
                print("Please put a non-negative integer for currency.")
                return


            if (varPremiumCurr == ""):
                print("Please put a non-negative integer for currency.")
                return
            elif (not varPremiumCurr.isnumeric()):
                print("Please put a non-negative integer for currency.")
                return
            elif (int(varPremiumCurr) < 0):
                print("Please put a non-negative integer for currency.")
                return

            query = "UPDATE Player SET level = \"" + varLevel + "\", normalCurr = \"" + varNormalCurr + "\", premiumCurr = \"" + varPremiumCurr + "\" WHERE username = \"" + varUsername + "\";"

            try:
                cursor.execute(query)
                cnx.commit()

                print("User: " + varUsername + " successfully updated!")
            except:
                print("Error - Aborted")
                cnx.rollback()
            finally:
                cursor.close()
                cnx.close()




        usernameLabel = tk.Label(self, text="Username of player to update:")
        usernameLabel.pack()

        username = tk.Text(self, height=1)
        username.pack()

        levelLabel = tk.Label(self, text="Updated Level:")
        levelLabel.pack()

        level = tk.Text(self, height=1)
        level.pack()

        normalCurrLabel = tk.Label(self, text="Updated Normal Currency:")
        normalCurrLabel.pack()

        normalCurr = tk.Text(self, height=1)
        normalCurr.pack()

        premiumCurrLabel = tk.Label(self, text="Updated Premium Currency:")
        premiumCurrLabel.pack()

        premiumCurr = tk.Text(self, height=1)
        premiumCurr.pack()






        button2 = tk.Button(self, text="Go!",
                            command=lambda: addPlayer())
        button2.pack()





        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("UpdatePageOne"))
        button.pack()


class CharacterUpdate(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Updating a Character:")
        label.pack(side="top", fill="x", pady=10)











        def updateCharacter():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')
            varCharacterName = characterName.get("1.0", "end-1c")
            varOwnerName = ownerName.get("1.0", "end-1c")
            varLevel = level.get("1.0", "end-1c")
            varHealth = health.get("1.0", "end-1c")
            varDefense = defense.get("1.0", "end-1c")
            varAttack = attack.get("1.0", "end-1c")
            varMana = mana.get("1.0", "end-1c")


            seeIfUserExists = "SELECT * FROM Player WHERE username = \"" + varOwnerName + "\";"
            cursor.execute(seeIfUserExists)

            exists = False
            for retVal in cursor:
                exists = True

            if (not exists):
                print("A user with the name: " + varOwnerName + "does not exist.")
                return

            seeIfCharacterAlreadyOwned = "SELECT * FROM Characters WHERE characterName = \"" + varCharacterName + "\" AND ownerName = \"" +  varOwnerName + "\";"

            cursor.execute(seeIfCharacterAlreadyOwned)

            exists = False
            for retVal in cursor:
                exists = True

            if (not exists):
                print("This character is not owned by that user.")
                return

            query = "UPDATE Characters SET level = \"" + varLevel + "\", health = \"" + varHealth + "\", defense = \"" + varDefense + "\", attack = \"" + varAttack + "\", mana = \"" + varMana + "\" WHERE characterName = \"" + varCharacterName + "\" AND ownerName = \"" +  varOwnerName + "\";"
            #print(query)

            try:
                cursor.execute(query)
                cnx.commit()
                print("Character successfully updated")

            except:
                cnx.rollback()

            for retVal in cursor:
                print(retVal)

            cursor.close()
            cnx.close()

        characterNameLabel = tk.Label(self, text="Character Name:")
        characterNameLabel.pack()

        characterName = tk.Text(self, height=1)
        characterName.pack()

        ownerNameLabel = tk.Label(self, text="Owner Name:")
        ownerNameLabel.pack()

        ownerName = tk.Text(self, height=1)
        ownerName.pack()



        varLevelLabel = tk.Label(self, text="Character Level:")
        varLevelLabel.pack()

        level = tk.Text(self, height=1)
        level.pack()


        varHealthLabel = tk.Label(self, text="Character Health:")
        varHealthLabel.pack()

        health = tk.Text(self, height=1)
        health.pack()



        varDefenseLabel = tk.Label(self, text="Character Defense:")
        varDefenseLabel.pack()

        defense = tk.Text(self, height=1)
        defense.pack()



        varAttackLabel = tk.Label(self, text="Character Attack:")
        varAttackLabel.pack()

        attack = tk.Text(self, height=1)
        attack.pack()



        varManaLabel = tk.Label(self, text="Character Mana:")
        varManaLabel.pack()

        mana = tk.Text(self, height=1)
        mana.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: updateCharacter())
        button2.pack()












        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("UpdatePageOne"))
        button.pack()


class ItemUpdate(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Updating an Item:")
        label.pack(side="top", fill="x", pady=10)

        def updateItem():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')

            varItemName = itemName.get("1.0", "end-1c")
            vardescription = description.get("1.0", "end-1c")
            varnormalCost= normalcost.get("1.0", "end-1c")
            varPremiumCost = premiumcost.get("1.0", "end-1c")
            varHealth = health.get("1.0", "end-1c")
            varDefense = defense.get("1.0", "end-1c")
            varattack = attack.get("1.0", "end-1c")
            #CAlled stored procedure here to check if item name exists within the Items table
            cursor.callproc("GetItems", [varItemName])
            results = [r.fetchall() for r in cursor.stored_results()]


            exists = False
            if len(results) !=0:
                exists = True

            if (not exists):
                print("The Item " + varItemName + " does not exist.")
                return

            query = "UPDATE Items SET ItemName = \"" + varItemName + "\", description = \"" + vardescription + \
                    "\", normalCost= \"" + varnormalCost + "\", premiumCost = \"" + varPremiumCost + "\", health = \"" + varHealth +\
                    "\", defense = \"" + varDefense + "\", attack= \"" + varattack + "\" where ItemName = \"" + varItemName + "\";"
            print(query)

            try:
                cursor.execute(query)
                cnx.commit()
                print("Item successfully updated")

            except:
                cnx.rollback()
            cursor.execute('select * from Items')
            for retVal in cursor:
                print(retVal)

            cursor.close()
            cnx.close()

        itemNameLabel = tk.Label(self, text="Item Name:")
        itemNameLabel.pack()
        itemName = tk.Text(self, height=1)
        itemName.pack()

        descriptionLabel = tk.Label(self, text="Item Description:")
        descriptionLabel.pack()
        description= tk.Text(self, height=1)
        description.pack()

        normalcostlabel = tk.Label(self, text="Item Normal cost:")
        normalcostlabel.pack()
        normalcost= tk.Text(self, height=1)
        normalcost.pack()

        premiumcostLabel = tk.Label(self, text="Item Premium cost:")
        premiumcostLabel.pack()
        premiumcost = tk.Text(self, height=1)
        premiumcost.pack()

        healthLabel = tk.Label(self, text="Item Health :")
        healthLabel.pack()
        health = tk.Text(self, height=1)
        health.pack()

        varDefenseLabel = tk.Label(self, text="Item Defense:")
        varDefenseLabel.pack()
        defense = tk.Text(self, height=1)
        defense.pack()

        varAttackLabel = tk.Label(self, text="Item  Attack:")
        varAttackLabel.pack()
        attack = tk.Text(self, height=1)
        attack.pack()


        button2 = tk.Button(self, text="Go!",
                            command=lambda: updateItem())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("UpdatePageOne"))
        button.pack()


class MonsterUpdate(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Updating a Monster:")
        label.pack(side="top", fill="x", pady=10)

        selectMonsters = []

        cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                      host=connection_info.MyHost,
                                      database=connection_info.MyDatabase)
        try:

            cnx.autocommit = False
            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='READ COMMITTED')

            # Using stored procedure to select for choosing all monsters created so far
            cursor.callproc("GetMonsters", [''])

            results = [r.fetchall() for r in cursor.stored_results()]

            # Create array that holds values for printing on label
            for i in range(len(results[0])):
                selectMonsters.append(results[0][i][0])


            # Commit your changes
            cnx.commit()

        except mysql.connector.Error as error:
            print("Failed to select record from database rollback: {}".format(error))
            # reverting changes because of exception
            cnx.rollback()
        finally:
            # closing database connection.
            if cnx.is_connected():
                cursor.close()
                cnx.close()
                print("Connection is closed")


        variable = tk.StringVar(self)
        variable.set(selectMonsters[0])

        dropDown = tk.OptionMenu(self, variable, *selectMonsters)
        dropDown.pack()

        def updateMonster():
            varOldMonsterName = variable.get()

            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            try:

                cnx.autocommit = False
                cursor = cnx.cursor(buffered=True)
                cnx.start_transaction(isolation_level='SERIALIZABLE')

                varNewMonsterName = monsterNameInput.get("1.0", "end-1c")
                if varNewMonsterName == "":
                    varNewMonsterName = varOldMonsterName
                varLevel = levelInput.get("1.0", "end-1c")
                varHealth = healthInput.get("1.0", "end-1c")
                varDefense = defenseInput.get("1.0", "end-1c")
                varAttack = attackInput.get("1.0", "end-1c")

                # Using stored procedure to select for choosing data from monster chosen
                cursor.callproc("GetMonsters", [varOldMonsterName])

                results = [r.fetchall() for r in cursor.stored_results()]

                # Set values for update
                for i in range(len(results[0])):
                    if varLevel == "":
                        varLevel = results[0][i][1]
                    if varHealth == "":
                        varHealth = results[0][i][2]
                    if varDefense == "":
                        varDefense = results[0][i][3]
                    if varAttack == "":
                        varAttack = results[0][i][4]

                # Update for monster selected
                cursor.execute("UPDATE Monsters SET monsterName = '%s', level = %d, health = %d, defense = %d, attack = %d WHERE monsterName = '%s';" % (varNewMonsterName, int(varLevel), int(varHealth), int(varDefense), int(varAttack), varOldMonsterName))

                # Update for propagation of changes to monsterName to StageMonsters
                cursor.execute("UPDATE StageMonsters SET monsterName = '%s' WHERE monsterName = '%s';" %
                               (varNewMonsterName, varOldMonsterName))

                # Update for propagation of changes to monsterName to MonsterDrops
                cursor.execute("UPDATE MonsterDrops SET monsterName = '%s' WHERE monsterName = '%s';" %
                               (varNewMonsterName, varOldMonsterName))

                # Commit your changes
                cnx.commit()

                print("Update successful.")

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")


        monsterNameLabel = tk.Label(self, text="Monster Name:")
        monsterNameLabel.pack()

        monsterNameInput = tk.Text(self, height=1)
        monsterNameInput.pack()

        levelLabel = tk.Label(self, text="Monster Level:")
        levelLabel.pack()

        levelInput = tk.Text(self, height=1)
        levelInput.pack()

        healthLabel = tk.Label(self, text="Monster Health:")
        healthLabel.pack()

        healthInput = tk.Text(self, height=1)
        healthInput.pack()

        defenseLabel = tk.Label(self, text="Monster Defense:")
        defenseLabel.pack()

        defenseInput = tk.Text(self, height=1)
        defenseInput.pack()

        attackLabel = tk.Label(self, text="Monster Attack:")
        attackLabel.pack()

        attackInput = tk.Text(self, height=1)
        attackInput.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: updateMonster())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("UpdatePageOne"))
        button.pack()


class SkillUpdate(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Updating a Skill:")
        label.pack(side="top", fill="x", pady=10)

        def updateSkills():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')
            varSkillName = skillName.get("1.0", "end-1c")
            varDescription = description.get("1.0", "end-1c")
            varDamage = damage.get("1.0", "end-1c")
            varManaCost = manaCost.get("1.0", "end-1c")

            cursor.execute(
                "UPDATE Skills SET skillName = '%s', description = '%s', damage = '%s', manaCost = '%s' WHERE skillName = '%s'" % (
                    varSkillName, varDescription, varDamage, varManaCost, varSkillName))
            # print updated output
            cursor.callproc("GetSkills", [varSkillName])

            results = [r.fetchall() for r in cursor.stored_results()]
            for i in range(len(results[0])):
                print(results[0][i])

            cursor.close()
            cnx.close()

        skillNameLabel = tk.Label(self, text="Skill Name:")
        skillNameLabel.pack()

        skillName = tk.Text(self, height=1)
        skillName.pack()

        descriptionLabel = tk.Label(self, text="Description:")
        descriptionLabel.pack()

        description = tk.Text(self, height=1)
        description.pack()

        damageLabel = tk.Label(self, text="Damage:")
        damageLabel.pack()

        damage = tk.Text(self, height=1)
        damage.pack()

        manaCostLabel = tk.Label(self, text="Mana Cost:")
        manaCostLabel.pack()

        manaCost = tk.Text(self, height=1)
        manaCost.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: updateSkills())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("UpdatePageOne"))
        button.pack()


class StageUpdate(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Updating a Stage:")
        label.pack(side="top", fill="x", pady=10)

        selectStages = []

        cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                      host=connection_info.MyHost,
                                      database=connection_info.MyDatabase)
        try:

            cnx.autocommit = False
            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')

            # Using stored procedure to select for choosing all stages created so far
            cursor.callproc("GetStages", [''])

            results = [r.fetchall() for r in cursor.stored_results()]

            # Create array that holds values for printing on label
            for i in range(len(results[0])):
                selectStages.append(results[0][i][0])

            # Commit your changes
            cnx.commit()

        except mysql.connector.Error as error:
            print("Failed to select record from database rollback: {}".format(error))
            # reverting changes because of exception
            cnx.rollback()
        finally:
            # closing database connection.
            if cnx.is_connected():
                cursor.close()
                cnx.close()
                print("Connection is closed")


        variable = tk.StringVar(self)
        variable.set(selectStages[0])

        dropDown = tk.OptionMenu(self, variable, *selectStages)
        dropDown.pack()

        def updateStage():
            varOldStageName = variable.get()

            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            try:

                cnx.autocommit = False
                cursor = cnx.cursor(buffered=True)
                cnx.start_transaction(isolation_level='SERIALIZABLE')

                varNewStageName = stageNameInput.get("1.0", "end-1c")
                if varNewStageName == "":
                    varNewStageName = varOldStageName
                varStageDescription = stageDescriptionInput.get("1.0", "end-1c")

                # Using stored procedure to select for choosing data from monster chosen
                cursor.callproc("GetStages", [varOldStageName])

                results = [r.fetchall() for r in cursor.stored_results()]

                # Set values for update
                for i in range(len(results[0])):
                    if varStageDescription == "":
                        varStageDescription = results[0][i][1]

                # Update for stage selected
                cursor.execute("UPDATE Stage SET stageName = '%s', stageDescription = '%s' WHERE stageName = '%s';" % (
                    varNewStageName, varStageDescription, varOldStageName))

                # Update for propagation of changes to stageName to StageMonsters
                cursor.execute("UPDATE StageMonsters SET stageName = '%s' WHERE stageName = '%s';" %
                               (varNewStageName, varOldStageName))

                # Commit your changes
                cnx.commit()

                print("Update successful.")

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")


        stageNameLabel = tk.Label(self, text="Stage Name:")
        stageNameLabel.pack()

        stageNameInput = tk.Text(self, height=1)
        stageNameInput.pack()

        stageDescriptionLabel = tk.Label(self, text="Stage Description:")
        stageDescriptionLabel.pack()

        stageDescriptionInput = tk.Text(self, height=1)
        stageDescriptionInput.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: updateStage())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("UpdatePageOne"))
        button.pack()


class StageMonstersUpdate(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Updating the Monsters in a Stage:")
        label.pack(side="top", fill="x", pady=10)

        selectStages = []
        selectMonsters = []

        cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                      host=connection_info.MyHost,
                                      database=connection_info.MyDatabase)
        try:

            cnx.autocommit = False
            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='READ COMMITTED')

            # Select for choosing all stages in StageMonsters
            sql_select_query = "SELECT DISTINCT stageName FROM StageMonsters;"
            cursor.execute(sql_select_query)

            for (stageName) in cursor:
                selectStages.append(stageName)

            # Select for choosing all monsters in StageMonsters
            sql_select_query = "SELECT DISTINCT monsterName FROM StageMonsters;"
            cursor.execute(sql_select_query)

            for (monsterName) in cursor:
                selectMonsters.append(monsterName)

            # Commit your changes
            cnx.commit()

        except mysql.connector.Error as error:
            print("Failed to select record from database rollback: {}".format(error))
            # reverting changes because of exception
            cnx.rollback()
        finally:
            # closing database connection.
            if cnx.is_connected():
                cursor.close()
                cnx.close()
                print("Connection is closed")

        if not selectStages:
            selectStages.append("None")

        variable = tk.StringVar(self)
        variable.set(selectStages[0])

        dropDown = tk.OptionMenu(self, variable, *selectStages)
        dropDown.pack()

        if not selectMonsters:
            selectMonsters.append("None")

        variable2 = tk.StringVar(self)
        variable2.set(selectMonsters[0])

        dropDown = tk.OptionMenu(self, variable2, *selectMonsters)
        dropDown.pack()

        def updateMonstersInStage():
            varStageName = variable.get()
            varMonsterName = variable2.get()

            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            try:

                cnx.autocommit = False
                cursor = cnx.cursor(buffered=True)
                cnx.start_transaction(isolation_level='SERIALIZABLE')

                varStageAmount = stageAmountInput.get("1.0", "end-1c")

                if varStageAmount != "":
                    cursor.execute("UPDATE StageMonsters SET amount = %d WHERE stageName = '%s' AND monsterName = '%s';" % (int(varStageAmount), varStageName, varMonsterName))
                    print("Record Updated successfully")
                else:
                    print("Choose amount to update!")

                # Commit your changes
                cnx.commit()

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

        stageAmountLabel = tk.Label(self, text="New Amount:")
        stageAmountLabel.pack()

        stageAmountInput = tk.Text(self, height=1, width=5)
        stageAmountInput.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: updateMonstersInStage())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("UpdatePageOne"))
        button.pack()


class MonsterDropsUpdate(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Updating the Items a Monster Drops:")
        label.pack(side="top", fill="x", pady=10)

        selectMonsters = []
        selectItems = []

        cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                      host=connection_info.MyHost,
                                      database=connection_info.MyDatabase)
        try:

            cnx.autocommit = False
            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='READ COMMITTED')

            # Select for choosing all monsters in MonsterDrops
            sql_select_query = "SELECT DISTINCT monsterName FROM MonsterDrops;"
            cursor.execute(sql_select_query)

            for (monsterName) in cursor:
                selectMonsters.append(monsterName)

            # Select for choosing all monsters in StageMonsters
            sql_select_query = "SELECT DISTINCT itemName FROM MonsterDrops;"
            cursor.execute(sql_select_query)

            for (itemName) in cursor:
                selectItems.append(itemName)

            # Commit your changes
            cnx.commit()

        except mysql.connector.Error as error:
            print("Failed to select record from database rollback: {}".format(error))
            # reverting changes because of exception
            cnx.rollback()
        finally:
            # closing database connection.
            if cnx.is_connected():
                cursor.close()
                cnx.close()
                print("Connection is closed")

        if not selectMonsters:
            selectMonsters.append("None")

        variable = tk.StringVar(self)
        variable.set(selectMonsters[0])

        dropDown = tk.OptionMenu(self, variable, *selectMonsters)
        dropDown.pack()

        if not selectItems:
            selectItems.append("None")

        variable2 = tk.StringVar(self)
        variable2.set(selectItems[0])

        dropDown = tk.OptionMenu(self, variable2, *selectItems)
        dropDown.pack()

        def updateItemsDroppedByMonsters():
            varMonsterName = variable.get()
            varItemName = variable2.get()

            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            try:

                cnx.autocommit = False
                cursor = cnx.cursor(buffered=True)
                cnx.start_transaction(isolation_level='SERIALIZABLE')

                varItemAmount = itemAmountInput.get("1.0", "end-1c")

                if varItemAmount != "":
                    cursor.execute("UPDATE MonsterDrops SET amount = %d WHERE monsterName = '%s' AND itemName = '%s';" % (int(varItemAmount), varMonsterName, varItemName))
                    print("Record Updated successfully")
                else:
                    print("Choose amount to update!")

                # Commit your changes
                cnx.commit()

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

        itemAmountLabel = tk.Label(self, text="New Amount:")
        itemAmountLabel.pack()

        itemAmountInput = tk.Text(self, height=1, width=5)
        itemAmountInput.pack()

        button2 = tk.Button(self, text="Go!",
                            command=lambda: updateItemsDroppedByMonsters())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("UpdatePageOne"))
        button.pack()











#GIYS PUT YOUE BIG QUERIES AND TASKS THAT MIGHT NOT FIT WITHIN THE MOLD OF ADD RETRIEVE OR UPDATE A VARIABLE HEREEEE!!!
class ActionsPageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="What would you like to do?")
        label.pack(side="top", fill="x", pady=10)

        variable = tk.StringVar(self)
        variable.set(actionsOptions[0])

        dropDown = tk.OptionMenu(self, variable, *actionsOptions)
        dropDown.pack()

        def BQPOOk():
            if variable.get() == "Fight a Monster!":
                controller.show_frame("FightBQ")
            elif variable.get() == "Acquire Item From Monster":
                controller.show_frame("IFMDUpdate")
            elif variable.get() == "Pick Strongest Skill!":
                controller.show_frame("StrongestSkill")
            elif variable.get() == 'Buy an Item':
                controller.show_frame("BuyItemPage")
            elif variable.get() == 'Equip an Item':
                controller.show_frame('EquipItemPageOne')
            elif variable.get() == 'Obtain player information as well as max amount of Items for a character':
                controller.show_frame('MaxItemAmountPage')
            elif variable.get() == "Return players in order of net worth":
                controller.show_frame("PlayersNetWorth")


        button2 = tk.Button(self, text="OK", command=BQPOOk)
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()



class PlayersNetWorth(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Player's net worth")
        label.pack(side="top", fill="x", pady=10)



        def PNWOk():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)


            try:
                cursor = cnx.cursor()
                cnx.start_transaction(isolation_level='READ COMMITTED')


                subquery1 = "SELECT itemName, (normalCost + premiumCost*10) as totalCost FROM Items"
                subquery2 = "SELECT itemName, username, amount FROM ItemRel"


                subquery3 = """
                        SELECT sq2.username, SUM(sq1.totalCost * sq2.amount) itemCost
                        FROM ( %s ) as sq1 JOIN ( %s ) as sq2 
                        ON sq1.itemName = sq2.itemName
                        GROUP BY sq2.username
                 """ % (subquery1, subquery2)


                subquery4 = "SELECT username, (normalCurr + premiumCurr*10) as totalCurr FROM Player"


                query = """
                    SELECT sq3.username, SUM(sq3.itemCost + sq4.totalCurr) netWorth
                    FROM ( %s ) as sq3 JOIN ( %s ) as sq4
                    ON sq3.username = sq4.username
                    GROUP BY sq3.username
                    ORDER BY netWorth DESC
                    ;
                """ % (subquery3, subquery4)




                print(query)
                cursor.execute(query)

                for outVal in cursor:
                    print(outVal[0] + ": " + str(outVal[1]))


            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")



        button2 = tk.Button(self, text="Go!", command=PNWOk)
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class FightBQ(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="The battle begins!")
        label.pack(side="top", fill="x", pady=10)


        selectUsername = []
        selectMonsterFight = []

        cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                      host=connection_info.MyHost,
                                      database=connection_info.MyDatabase)
        try:

            cnx.autocommit = False
            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='READ COMMITTED')

            # Select for choosing all usernames created so far
            sql_select_query = "SELECT username, level FROM Player;"
            cursor.execute(sql_select_query)

            for (username, level) in cursor:
                selectUsername.append(username)

            # Select for choosing all monster drops created so far
            sql_select_query = "SELECT * FROM StageMonsters;"
            cursor.execute(sql_select_query)

            for (stageName, monsterName, amount) in cursor:
                selectMonsterFight.append(str(amount) + " " + monsterName + " in the " + stageName + " stage")

            # Commit your changes
            cnx.commit()

        except mysql.connector.Error as error:
            print("Failed to select record from database rollback: {}".format(error))
            # reverting changes because of exception
            cnx.rollback()
        finally:
            # closing database connection.
            if cnx.is_connected():
                cursor.close()
                cnx.close()
                print("Connection is closed")

        if not selectUsername:
            selectUsername.append("None")

        variable = tk.StringVar(self)
        variable.set(selectUsername[0])

        dropDown = tk.OptionMenu(self, variable, *selectUsername)
        dropDown.pack()

        if not selectMonsterFight:
            selectMonsterFight.append("None")

        variable2 = tk.StringVar(self)
        variable2.set(selectMonsterFight[0])

        dropDown2 = tk.OptionMenu(self, variable2, *selectMonsterFight)
        dropDown2.pack()

        infoArray = []

        def applytoLabel():
            n = len(infoArray)
            element = ''
            for i in range(n):
                element = element + infoArray[i] + '\n'
            return element

        def optimizeFight():
            varUsername = variable.get()
            varFight = variable2.get()
            fightVars = varFight.split(" ")
            varMonsterName = fightVars[1]
            varAmount = fightVars[0]
            varStageName = fightVars[4]

            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            try:

                cnx.autocommit = False
                cursor = cnx.cursor(buffered=True)
                cnx.start_transaction(isolation_level='SERIALIZABLE')

                cursor.execute("SELECT * FROM (SELECT c.characterName, (c.attack + i.attack) as damage, i.itemName as used, 'item' as type FROM Characters c JOIN ItemRel ir ON c.characterName = ir.characterName AND c.ownerName = ir.username JOIN Items i ON ir.itemName = i.itemName WHERE c.ownerName = '%s' UNION SELECT c.characterName, damage, s.skillName as used, 'skill' as type  FROM Characters c JOIN SkillRel sr ON c.characterName = sr.characterName JOIN Skills s ON sr.skillName = s.skillName AND c.mana > s.manaCost WHERE c.ownerName = '%s') as a GROUP BY characterName HAVING damage = (SELECT damage FROM (SELECT b.characterName, max(damage) FROM (SELECT c.characterName, (c.attack + i.attack) as damage, i.itemName as used, 'item' as type FROM Characters c JOIN ItemRel ir ON c.characterName = ir.characterName AND c.ownerName = ir.username JOIN Items i ON ir.itemName = i.itemName WHERE c.ownerName = '%s' UNION SELECT c.characterName, damage, s.skillName as used, 'skill' as type FROM Characters c JOIN SkillRel sr ON c.characterName = sr.characterName JOIN Skills s ON sr.skillName = s.skillName AND c.mana > s.manaCost WHERE c.ownerName = '%s' GROUP BY characterName) as b GROUP BY characterName) as d WHERE a.characterName = d.characterName) ORDER BY damage DESC LIMIT 4;" % (varUsername, varUsername, varUsername, varUsername))

                totalDamage = 0
                characterArray = []
                for (characterName, damage, used, type) in cursor:
                    infoArray.append(characterName + " used a " + used + " " + type + " to deal " + str(damage) + " damage!")
                    characterArray.append(characterName)
                    totalDamage = totalDamage + damage

                cursor.execute("SELECT m.health, (m.health * %d) as totalHealth, (m.attack * %d) as totalAttack, m.defense FROM Monsters m JOIN StageMonsters sm ON m.monsterName = sm.monsterName WHERE sm.monsterName = '%s';" % (int(varAmount), int(varAmount), varMonsterName))

                for (health, totalHealth, totalAttack, defense) in cursor:
                    damageDealt = totalDamage - (defense * int(varAmount))
                    if damageDealt > totalHealth:
                        infoArray.append("Your party dealt " + str(totalDamage) + " damage killing the " + str(varAmount) + " " + varMonsterName + "s!")
                        cursor.execute("DELETE FROM StageMonsters WHERE monsterName = '%s' AND stageName = '%s'" % (varMonsterName, varStageName))
                        print("Defeated the fight! Deletion Successful.")
                    else:
                        monstersKilled = math.floor(damageDealt / health)
                        if monstersKilled < 0:
                            monstersKilled = 0
                        infoArray.append("Your party dealt " + str(totalDamage) + " damage killing " + str(monstersKilled) + " " + varMonsterName + "s!")
                        infoArray.append("The " + varMonsterName + "s attack back doing " + str(totalAttack) + " damage!")
                        cursor.execute("UPDATE StageMonsters SET amount = %d WHERE monsterName = '%s' AND stageName = '%s'" % ((int(varAmount) - monstersKilled), varMonsterName, varStageName))
                        for x in characterArray:
                            cursor.execute("UPDATE Characters SET health = health - %d WHERE characterName = '%s' AND ownerName = '%s'" % (round(totalAttack / len(characterArray)), x, varUsername))
                        print("Did not defeat the enemies! Update Successful.")

                # Commit your changes
                cnx.commit()

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

            label.config(text=applytoLabel())
            infoArray.clear()

        button2 = tk.Button(self, text="Optimize fight",
                            command=lambda: optimizeFight())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("ActionsPageOne"))
        button.pack()


class IFMDUpdate(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Updating the Items a Player gets from Monster Drops:")
        label.pack(side="top", fill="x", pady=10)

        selectMonsterDrops = []
        selectUsername = []

        cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                      host=connection_info.MyHost,
                                      database=connection_info.MyDatabase)
        try:

            cnx.autocommit = False
            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='READ COMMITTED')

            # Select for choosing all monster drops created so far
            sql_select_query = "SELECT monsterName, itemName, amount FROM MonsterDrops;"
            cursor.execute(sql_select_query)

            for (monsterName, itemName, amount) in cursor:
                selectMonsterDrops.append(monsterName + " dropped " + str(amount) + " " + itemName)

            # Select for choosing all usernames created so far
            sql_select_query = "SELECT username, level FROM Player;"
            cursor.execute(sql_select_query)

            for (username, level) in cursor:
                selectUsername.append(username)

            # Commit your changes
            cnx.commit()

        except mysql.connector.Error as error:
            print("Failed to select record from database rollback: {}".format(error))
            # reverting changes because of exception
            cnx.rollback()
        finally:
            # closing database connection.
            if cnx.is_connected():
                cursor.close()
                cnx.close()
                print("Connection is closed")

        if not selectMonsterDrops:
            selectMonsterDrops.append("None")

        variable = tk.StringVar(self)
        variable.set(selectMonsterDrops[0])

        dropDown = tk.OptionMenu(self, variable, *selectMonsterDrops)
        dropDown.pack()

        if not selectUsername:
            selectUsername.append("None")

        variable2 = tk.StringVar(self)
        variable2.set(selectUsername[0])

        dropDown2 = tk.OptionMenu(self, variable2, *selectUsername)
        dropDown2.pack()

        def updateIFMD():
            varMonsterDrop = variable.get()
            monsterDropsVars = varMonsterDrop.split(" ")
            varItemName = monsterDropsVars[3]
            varAmount = monsterDropsVars[2]
            varUsername = variable2.get()

            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)

            try:

                cnx.autocommit = False
                cursor = cnx.cursor(buffered=True)
                cnx.start_transaction(isolation_level='SERIALIZABLE')

                # Select to get item data for username selected
                cursor.execute(
                    "SELECT itemName, amount FROM ItemRel WHERE username = '%s' AND characterName = NULL;" % varUsername)

                # Update or insert for monster drop acquired
                for (itemName, amount) in cursor:
                    if itemName == varItemName:
                        newAmount = amount + varAmount;
                        cursor.execute("UPDATE ItemRel SET amount = %d WHERE username = '%s' AND itemName = '%s');" % (
                                newAmount, varItemName, varUsername))
                        print("Record Updated successfully")
                        break;
                else:
                    cursor.execute(
                        "INSERT INTO ItemRel(itemName, username, characterName, amount) VALUES ('%s', '%s', NULL, '%d');" % (varItemName, varUsername, int(varAmount)))
                    print("Record Inserted successfully")

                # Commit your changes
                cnx.commit()

            except mysql.connector.Error as error:
                print("Failed to select record from database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            finally:
                # closing database connection.
                if cnx.is_connected():
                    cursor.close()
                    cnx.close()
                    print("Connection is closed")

        button2 = tk.Button(self, text="Go!",
                            command=lambda: updateIFMD())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("ActionsPageOne"))
        button.pack()


class StrongestSkill(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Pick the Strongest Skill for Characters that have Skills!")
        label.pack(side="top", fill="x", pady=10)

        def GetStrongestSkill():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            cursor = cnx.cursor()
            cursor.execute("select characterName, Skills.skillName, description, damage, manaCost from SkillRel join Skills on SkillRel.skillName = Skills.skillName where damage in (select max(damage) from Skills) group by characterName;")

            for i in cursor:
                print(i)
        button2 = tk.Button(self, text="Go!",
                            command=lambda: GetStrongestSkill())
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("ActionsPageOne"))
        button.pack()


class EquipItemPageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Equip Item for Monster or Player?")
        label.pack(side="top", fill="x", pady=10)
        options = ['Player', 'Monster']

        variable = tk.StringVar(self)
        variable.set(options[0])

        dropDown = tk.OptionMenu(self, variable, *options)
        dropDown.pack()

        def APOOk():
            if (variable.get() == "Player"):
                controller.show_frame("UserEquipItem")
            elif (variable.get() == "Monster"):
                controller.show_frame("MonsterEquipItem")

        button2 = tk.Button(self, text="OK", command=APOOk)
        button2.pack()

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("ActionsPageOne"))
        button.pack()


class UserEquipItem(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Equipping an Item:")
        label.pack(side="top", fill="x", pady=10)

        cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                      host=connection_info.MyHost,
                                      database=connection_info.MyDatabase)
        cursor = cnx.cursor()
        cnx.start_transaction(isolation_level='READ COMMITTED')

        varPlayerName = 'playernameonly'
        cursor.callproc("GetPlayers", [varPlayerName])
        results = [r.fetchall() for r in cursor.stored_results()]
        final_result = [i[0] for i in results[0]]
        variable = tk.StringVar(self)
        variable.set(final_result[0])
        Playerlabel = tk.Label(self, text="Player name")
        Playerlabel.pack()
        dropDown = tk.OptionMenu(self, variable, *final_result)
        dropDown.pack()

        characterIDlabel = tk.Label(self, text="CharacterID:")
        characterIDlabel.pack()
        characterID = tk.Text(self, height=1)
        characterID.pack()

        varItemName = 'itemnameonly'
        cursor.callproc("GetItems", [varItemName])
        results = [r.fetchall() for r in cursor.stored_results()]
        itemlist = [i[0] for i in results[0]]
        tempitem = tk.StringVar(self)
        tempitem.set(itemlist[0])
        Itemlabel = tk.Label(self, text="Item Name")
        Itemlabel.pack()
        dropDown2 = tk.OptionMenu(self, tempitem, *itemlist)
        dropDown2.pack()






        def EquipItem():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')


            varItemName = tempitem.get()
            varamount = amount.get("1.0", "end-1c")
            varcharacterID = characterID.get("1.0", "end-1c")
            varPlayer = variable.get()


            addquery = 'UPDATE ItemRel set amount = amount+' + str(
                varamount) + ' where username = \"' + varPlayer + '\" and ItemName = \"' + varItemName + '\" and characterName = \"' + varcharacterID + '\";'
            removequery = 'UPDATE ItemRel set amount = amount-' + str(
                varamount) + ' where username = \"' + varPlayer + '\" and ItemName = \"' + varItemName + '\" and characterName != \"' + varcharacterID + '\";'
            try:
                print("#####ITEMREL BEFORE")
                cursor.execute('select * from ItemRel')
                for i in cursor:
                    print(i)
                cursor.execute(removequery)
                if cursor.rowcount !=0:
                    cursor.execute(addquery)
                    if cursor.rowcount <1:
                        insertquery = 'INSERT INTO ItemRel(username, characterName,itemName,  amount) VALUES (\"'+varPlayer+'\", \"'\
                         +str(varcharacterID)+'\", \"'+varItemName+'\", '+str(varamount)+');'
                        cursor.execute(insertquery)

                print("#####ITEMREL AFTER")
                cursor.execute('select * from ItemRel')
                for i in cursor:
                    print(i)


            except:
                print("Could not update the Character Items. Maybe syntax issue?")
                cnx.rollback()
            cnx.commit()

            cursor.close()
            cnx.close()


        amountlabel= tk.Label(self, text="amount:")
        amountlabel.pack()
        amount= tk.Text(self, height=1)
        amount.pack()





        button2 = tk.Button(self, text="Go!",command=lambda: EquipItem())
        button2.pack()

        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("EquipItemPageOne"))
        button.pack()


class MonsterEquipItem(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Equipping an Item:")
        label.pack(side="top", fill="x", pady=10)

        cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                      host=connection_info.MyHost,
                                      database=connection_info.MyDatabase)
        cursor = cnx.cursor()
        cnx.start_transaction(isolation_level='READ COMMITTED')

        query = "SELECT monsterName FROM MonsterItems;"
        cursor.execute(query)
        result = cursor.fetchall()
        final_result = [i[0] for i in result]
        variable = tk.StringVar(self)
        variable.set(final_result[0])
        Playerlabel = tk.Label(self, text="Monster name")
        Playerlabel.pack()
        dropDown = tk.OptionMenu(self, variable, *final_result)
        dropDown.pack()



        varItemName = 'itemnameonly'
        cursor.callproc("GetItems", [varItemName])
        results = [r.fetchall() for r in cursor.stored_results()]
        itemlist = [i[0] for i in results[0]]
        tempitem = tk.StringVar(self)
        tempitem.set(itemlist[0])
        Itemlabel = tk.Label(self, text="Item Name")
        Itemlabel.pack()
        dropDown2 = tk.OptionMenu(self, tempitem, *itemlist)
        dropDown2.pack()






        def EquipItem():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            cursor = cnx.cursor()
            cnx.start_transaction(isolation_level='SERIALIZABLE')


            varItemName = tempitem.get()
            varamount = amount.get("1.0", "end-1c")
            varPlayer = variable.get()


            addquery = 'UPDATE MonsterItems set amount = amount+' + str(
                varamount) + ' where monsterName = \"' + varPlayer + '\" and ItemName = \"' + varItemName + '\"; '
            try:
                print("#####MonsterItems BEFORE")
                cursor.execute('select * from MonsterItems')
                for i in cursor:
                    print(i)


                cursor.execute(addquery)
                if cursor.rowcount <1:
                    insertquery = 'INSERT INTO MonsterItems(monsterName, itemName,  amount) VALUES (\"' + varPlayer + '\", \"' \
                                     + varItemName + '\", ' + str(varamount) + ');'
                    cursor.execute(insertquery)
                print("#####MonsterItems AFTER")
                cursor.execute('select * from MonsterItems')
                for i in cursor:
                    print(i)

            except:
                print("Could not update the MOnster Items. Maybe syntax issue?")
                cnx.rollback()
            cnx.commit()

            cursor.close()
            cnx.close()


        amountlabel= tk.Label(self, text="amount:")
        amountlabel.pack()
        amount= tk.Text(self, height=1)
        amount.pack()





        button2 = tk.Button(self, text="Go!",command=lambda: EquipItem())
        button2.pack()

        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("EquipItemPageOne"))
        button.pack()


class BuyItemPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Buy an Item:")
        label.pack(side="top", fill="x", pady=10)
        cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                      host=connection_info.MyHost,
                                      database=connection_info.MyDatabase)
        cursor = cnx.cursor()
        cnx.start_transaction(isolation_level='READ COMMITTED')

        varPlayerName = 'playernameonly'
        cursor.callproc("GetPlayers", [varPlayerName])
        results = [r.fetchall() for r in cursor.stored_results()]
        final_result = [i[0] for i in results[0]]
        variable = tk.StringVar(self)
        variable.set(final_result[0])
        Playerlabel= tk.Label(self, text="Player name")
        Playerlabel.pack()
        dropDown = tk.OptionMenu(self, variable, *final_result)
        dropDown.pack()

        varItemName = 'itemnameonly'
        cursor.callproc("GetItems", [varItemName])
        results = [r.fetchall() for r in cursor.stored_results()]
        itemlist = [i[0] for i in results[0]]
        tempitem = tk.StringVar(self)
        tempitem.set(itemlist[0])
        Itemlabel = tk.Label(self, text="Item Name")
        Itemlabel.pack()
        dropDown2 = tk.OptionMenu(self, tempitem, *itemlist)
        dropDown2.pack()


        currlist = ['normalCurr', 'premiumCurr']
        tempcurr= tk.StringVar(self)
        tempcurr.set(currlist[0])
        currlabel = tk.Label(self, text="Currency Type")
        currlabel.pack()
        dropDown2 = tk.OptionMenu(self, tempcurr, *currlist)
        dropDown2.pack()

        cursor.close()
        cnx.close()


        def BuyItem():
            varusername =variable.get()
            try:
                cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                                          host=connection_info.MyHost,
                                                          database=connection_info.MyDatabase)
                cursor = cnx.cursor()
                cnx.start_transaction(isolation_level='SERIALIZABLE')

                varamount = amount.get("1.0", "end-1c")
                varItemName = tempitem.get()
                varCurr = tempcurr.get()


                if varCurr == 'normalCurr':
                    stritemcost = 'normalCost'
                else:
                    stritemcost = 'premiumCost'
                print("#####ITEMREL Before")
                cursor.execute('select * from ItemRel')
                for i in cursor:
                    print(i)




                addquery = 'UPDATE ItemRel set amount = amount+' + str(
                    varamount) + ' where username = \"' + varusername + '\" and ItemName = \"' + varItemName + '\"'
                cursor.execute(addquery)
                error = cursor.rowcount


                if error <1:
                    varcharacterID = 111
                    insertquery = 'INSERT INTO ItemRel(username, characterName,itemName,  amount) VALUES (\"' + varusername + '\", \"' \
                                  + str(varcharacterID) + '\", \"' + varItemName + '\", ' + str(varamount) + ');'
                    cursor.execute(insertquery)
                print("#####ITEMREL AFTER")
                cursor.execute('select * from ItemRel')
                for i in cursor:
                    print(i)

                print("#####Player Before")
                cursor.execute('select * from Player')
                for i in cursor:
                    print(i)



                sql_update_query = 'UPDATE Player SET ' + varCurr + '= ' + varCurr + '- ' + str(
                    varamount) + ' * (select ' + stritemcost + ' from Items where ItemName = \"' + varItemName + '\") where username = \"' + varusername + '\"'
                cursor.execute(sql_update_query)

                print("#####Player AFTER")
                cursor.execute('select * from Player')
                for i in cursor:
                    print(i)


            except mysql.connector.Error as error:
                print("Failed to update record to database rollback: {}".format(error))
                # reverting changes because of exception
                cnx.rollback()
            cnx.commit()
            cursor.close()
            cnx.close()



        amountlabel = tk.Label(self, text="amount:")
        amountlabel.pack()
        amount = tk.Text(self, height=1)
        amount.pack()

        button2 = tk.Button(self, text="OK", command=lambda: BuyItem())
        button2.pack()

        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("ActionsPageOne"))
        button.pack()


class MaxItemAmountPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Equipping an Item:")
        label.pack(side="top", fill="x", pady=10)

        cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                      host=connection_info.MyHost,
                                      database=connection_info.MyDatabase)
        cursor = cnx.cursor()
        cnx.start_transaction(isolation_level='READ COMMITTED')

        varPlayerName = 'playernameonly'
        cursor.callproc("GetPlayers", [varPlayerName])
        results = [r.fetchall() for r in cursor.stored_results()]
        final_result = [i[0] for i in results[0]]
        variable = tk.StringVar(self)
        variable.set(final_result[0])
        Playerlabel = tk.Label(self, text="Player name")
        Playerlabel.pack()
        dropDown = tk.OptionMenu(self, variable, *final_result)
        dropDown.pack()



        def MaxItemRow():
            cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                          host=connection_info.MyHost,
                                          database=connection_info.MyDatabase)
            cursor = cnx.cursor(buffered =True)
            cnx.start_transaction(isolation_level='SERIALIZABLE')

            varPlayer = variable.get()
            query = 'select p.username, p.level,i.characterName, i.ItemName, i.amount from Player as p JOIN ItemRel as i  ON p.username=i.username where p.username = \"' + varPlayer+ '\" GROUP BY i.ItemName,i.amount, i.characterName  having i.amount = (select max(i2.amount) from ItemRel as i2 where i2.characterName= i.characterName);'

            try:

                cursor.execute(query)
                for i in cursor:
                    print(i)

            except:
                print("Couldn't execute the action")
                cnx.rollback()

            cursor.close()
            cnx.close()







        button2 = tk.Button(self, text="Go!",command=lambda: MaxItemRow())
        button2.pack()

        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("ActionsPageOne"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()