#Database assessment -- George Wilkins
#Imports

import os
import textwrap
import sqlite3

#Constants and variables
screen_width, _ = os.get_terminal_size()

DATABASE = 'dndspells.db'

def all_spell_names_ASC():
    '''To select all spell names ordered by level ascending
    '''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = 'SELECT spell_name FROM spell ORDER BY spell_level ASC'
    cursor.execute(sql)
    results = cursor.fetchall()
    print('Spell name:')
    for spells in results:
        print(f'{spells[0]}') 

def all_spell_desc_level_ASC():
    '''To select all spell names and their descriptions ordered by level ascending
    '''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = 'SELECT spell_name, description FROM spell ORDER BY spell_level ASC'
    cursor.execute(sql)
    results = cursor.fetchall()
    for spells in results:
        print(f'{textwrap.fill(spells[0] + ": " + spells[1], screen_width - 5)}\n')


def all_spells_with_classes_level_ASC():
    '''To select all spells and order by level ascending
    '''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = '''SELECT spell_name AS 'spells' , GROUP_CONCAT(class_name, ', ') AS 'classes'
        FROM spell_user INNER JOIN user ON spell_user.user_id = user.id
        INNER JOIN spell ON spell_user.spell_id = spell.id GROUP BY spell_name
        ORDER BY spell_level ASC;
    '''
    cursor.execute(sql)
    results = cursor.fetchall()
    print('Spell name:                    Class name:')
    for info in results:
        print(f'{info[0]:<30} {info[1]}')

def classes_ASC():
    '''To select all classes that can cast spells
    '''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = 'SELECT class_name FROM user ORDER BY class_name ASC'
    cursor.execute(sql)
    results = cursor.fetchall()
    print('Class name:')
    for classes in results:
        print(f'{classes[0]}')

def all_spells_with_upcast_level_ASC():
    '''To select all information about spells that can be upcast
    '''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = '''SELECT spell_level AS 'Level', spell_name AS 'Name' , description AS 'Description',
        at_higher_levels AS 'At higher levels', school AS 'School',
        GROUP_CONCAT(class_name, ', ') AS 'Class name' FROM spell_user
        INNER JOIN user ON spell_user.user_id = user.id
        INNER JOIN spell ON spell_user.spell_id = spell.id
        WHERE at_higher_levels IS NOT NULL
        GROUP BY spell_name
        ORDER BY spell_level ASC
    '''
    cursor.execute(sql)
    results = cursor.fetchall()
    for spell in results:
        # textwrap.fill makes it so that the text doesn't wrap round mid word. Probably won't be used in final product, but cool
        print(f'''
Spell level: {spell[0]} 
Spell name: {spell[1]}\n
{textwrap.fill('Description: ' + spell[2], screen_width -5)}\n
{textwrap.fill('At higher levels: ' + spell[3], screen_width -5)}
School: {spell[4]}
Class list: {spell[5]}
''')

def add_spell(information):
    ''' Tod add a spell into the databse

    Parameters:
    -----------
    information: list
    information: list
        This is the informaiton about the spell the user entered
    '''
    spl, spn, desc, ahl, sch, cls  = information
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql_spell = '''
        INSERT INTO spell (spell_level, spell_name, description, at_higher_levels, school) 
        VALUES (?, ?, ?, ?, ?);
    ''', (spl.strip(), spn.strip(), desc.strip(), ahl.strip(), sch.strip())
    cursor.execute(*sql_spell)
    # Will have a dropdown select tool so I won't need to verify user input
    classes = cls.split('/')
    # Runs as many times as needed for all classes to be inputed into bridging table
    for i in range(len(classes)):
        sql_class = '''
            INSERT INTO spell_user (spell_id, user_id)
            VALUES ((SELECT id FROM spell WHERE spell_name = ?), (SELECT id FROM user WHERE class_name = ?))
        ''', (spn, classes[i])
        cursor.execute(*sql_class)
    db.commit()

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
        WHERE spell_name LIKE ?
        GROUP BY spell_name
    ''', (name,)
    cursor.execute(*sql)
    results = cursor.fetchall()
    # Will make the spell level etc. stand out in html
    for spell in results:
        print(f'''
Spell level: {spell[0]}
Spell name: {spell[1]}
{textwrap.fill('Description: ' + spell[2], screen_width -5)}
At higher levels: {spell[3]}
School: {spell[4]}
Class list: {spell[5]}
''')
        
def delete_spell(name):
    '''To delete everything about a specific spell

    Parameters:
    -----------
    name: str
    This is the name of the spell you want to delete
    '''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql_spell = '''
        DELETE FROM spell_user WHERE spell_id = (SELECT spell.id FROM spell WHERE spell_name = ?);
    ''', (name,)
    sql_spell_user = '''
        DELETE FROM spell WHERE spell_name = ?;
    ''', (name,)
    cursor.execute(*sql_spell,)
    cursor.execute(*sql_spell_user)
    db.commit()

#main code  

#delete_spell(input('Please enter what spell you would like to delete: \n'))
add_spell(input('Please enter spell level, spell name, description, at higher levels (if available, otherwise enter as a space), school, and classes all sperated by a comma and if there are multiple classes, sperate by a "/"\n').split(','))
#all_spells_with_upcast_level_ASC()
#all_spell_desc_level_ASC()
#all_spells_with_classes_level_ASC()
#classes_ASC()
#all_spell_names_ASC()
#prints_info_about_one_spell(input ('What spell would you like to know about? '))