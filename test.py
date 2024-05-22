#Database assessment -- George Wilkins
#Imports

import sqlite3

#Constants and variables

DATABASE = "dndspells.db"

def all_spell_names():
    '''To select all spell names ordered by level ascending'''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = "SELECT spell_name FROM spell ORDER BY spell_level ASC"
    cursor.execute(sql)
    results = cursor.fetchall()
    #Loop through results
    print("Name")
    for spells in results:
        print(f"{spells[0]}") 

def info_about_one_spell():
    '''To select all information about a select spell'''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = """
    SELECT spell_level AS 'Level', spell_name AS 'Name' , description AS 'Description', at_higher_levels AS 'At higher levels', school AS 'School', GROUP_CONCAT(class_name, ', ') AS 'Class name' FROM spell_user
INNER JOIN user ON spell_user.user_id = user.id
INNER JOIN spell ON spell_user.spell_id = spell.id
WHERE spell_name LIKE 'Acid Splash'
GROUP BY spell_name
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    #Loop through results
    for spell in results:
        print(results)

#main code
#all_spell_names()
info_about_one_spell()