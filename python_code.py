#Database assessment -- George Wilkins
#Imports

import os
import textwrap
import sqlite3

#Constants and variables
screen_width, _ = os.get_terminal_size()

DATABASE = 'dndspells.db'

def all_spell_names():
    '''To select all spell names ordered by level ascending
    '''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = 'SELECT spell_name FROM spell ORDER BY spell_level ASC'
    cursor.execute(sql)
    results = cursor.fetchall()
    print('Spell name')
    for spells in results:
        print(f'{spells[0]}') 

def prints_info_about_one_spell(name):
    '''To select all information about a select spell
    
    Parameters:
    -----------
    name: str
        This is the name of the spell
    '''
    # Won't have user input via text, and instead buttons
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = f'''
        SELECT spell_level AS 'Level', spell_name AS 'Name' , description AS 'Description',
            at_higher_levels AS 'At higher levels', school AS 'School',
            GROUP_CONCAT(class_name, ', ') AS 'Class name'
        FROM spell_user
        INNER JOIN user ON spell_user.user_id = user.id
        INNER JOIN spell ON spell_user.spell_id = spell.id
        WHERE spell_name LIKE '{name}'
        GROUP BY spell_name
    '''
    cursor.execute(sql)
    results = cursor.fetchall()
    # Will make the spell level etc. stand out in html
    for spell in results:
        print(f'''
Spell level: {spell[0]}
Spell name: {spell[1]}
{textwrap.fill('Description: ' + spell[2], screen_width -20)}
At higher levels: {spell[3]}
School: {spell[4]}
Class list: {spell[5]}
''')

#main code
all_spell_names()
#prints_info_about_one_spell(input ('What spell would you like to know about? '))