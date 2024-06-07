from flask import Flask, render_template, request, redirect, url_for
import sqlite3

DATABASE = 'dndspells.db'

app = Flask(__name__)

@app.route('/spells')
def spell_names():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('SELECT spell_name, spell_level FROM spell ORDER BY spell_level ASC')
    level_to_spells = []
    for name, level in cursor.fetchall():
        level = int(level)
        if level >= len(level_to_spells):
            level_to_spells.append([])
        level_to_spells[level].append(name)
    return render_template('spells.html', spells=level_to_spells)

@app.route('/classes')
def class_names():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('SELECT class_name FROM user ORDER BY class_name ASC')
    ret = [i[0] for i in cursor.fetchall()]
    return render_template('classes.html', classes=ret)

@app.route('/classes/<class_name>')
def single_class(class_name):
    print(class_name)
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = f'''
                SELECT spell_name, spell_level FROM spell_user
                INNER JOIN user ON spell_user.user_id = user.id
                INNER JOIN spell ON spell_user.spell_id = spell.id
                WHERE class_name = ?
                GROUP BY spell_name
                ORDER BY spell_level
                ''', (class_name,)
    cursor.execute(*sql)
    level_to_spells = []
    for name, level in cursor.fetchall():
        level = int(level)
        while level >= len(level_to_spells):
            level_to_spells.append([])
        level_to_spells[level].append(name)
    length = len(level_to_spells)
    return render_template('single_class.html', spells=level_to_spells, class_name=class_name, length=length)

@app.route('/spell/<spell>')
def single_spell(spell):
    single_spell_header = ['Level: ', 'Name: ', 'Description: ', 'At higher levels: ', 'School: ', 'Classes: ']
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
    ''', (spell,)
    cursor.execute(*sql)
    ret = cursor.fetchone()
    return render_template('single_spell.html', details = ret, single_spell_header = single_spell_header)

@app.route('/add_spell_input', methods = ['GET'])
def add_spell_input():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''
                SELECT class_name FROM user ORDER BY class_name ASC
                   ''')
    classes = cursor.fetchall()
    schools = ['Abjuration', 'Conjuration', 'Divination', 'Enchantment', 'Evocation', 'Illusion', 'Necromancy', 'Transmutation']
    return render_template('add_spell_input.html', schools=schools, classes=classes)
    

@app.route('/add_spell_save', methods = ['GET'])
def add_spell_save():  
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    if request.method == 'GET':
        spl, spn, desc, ahl, sch, cls = request.args.get('spl'), request.args.get('spn'), request.args.get('desc'), request.args.get('ahl'), request.args.get('sch'), request.args.getlist('cls')
        sql_spell = '''
            INSERT INTO spell (spell_level, spell_name, description, at_higher_levels, school) 
            VALUES (?, ?, ?, ?, ?);
        ''', (spl, spn, desc, ahl, sch)
        cursor.execute(*sql_spell)
        for i in range(len(cls)):
            sql_class = '''
                INSERT INTO spell_user (spell_id, user_id)
                VALUES ((SELECT id FROM spell WHERE spell_name = ?), (SELECT id FROM user WHERE class_name = ?))
            ''', (spn, cls[i])
            cursor.execute(*sql_class)
        #Make sure that at_higher_levels is NULL if need be
        cursor.execute('''
            UPDATE spell 
            SET at_higher_levels = NULL 
            WHERE at_higher_levels = '';
        ''')
        db.commit()
        return redirect(url_for('single_spell', spell=spn))
    else:
        # This should never happen, but just incase
        schools = ['Abjuration', 'Conjuration', 'Divination', 'Enchantment', 'Evocation', 'Illusion', 'Necromancy', 'Transmutation']
        return render_template('add_spell_input.html', schools=schools)


@app.route('/delete_spells_input', methods = ['GET'])
def delete_spells_input():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''
                    SELECT spell_name FROM spell ORDER BY spell_level ASC
                   ''')
    spell_names_remove = cursor.fetchall()
    return render_template('delete_spells_input.html', spell_names_remove=spell_names_remove)
    

@app.route('/delete_spells_save', methods = ['GET'])
def delete_spells_save():  
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    if request.method == 'GET':
        spell = request.args.getlist('delete_spells')
        print("|"*80)
        print(spell)
        for i in range(len(spell)):
            sql_spell_user = '''
                DELETE FROM spell_user WHERE spell_id = (SELECT spell.id FROM spell WHERE spell_name = ?);
        ''', (spell[i],)
            cursor.execute(*sql_spell_user)
            sql_spell = '''
            DELETE FROM spell WHERE spell_name = ?;
        ''', (spell[i],)
            cursor.execute(*sql_spell)
        db.commit()
        return render_template('index.html', )
    else:
        # This should never happen, but just incase
        return render_template('delete_spells_input.html', )


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)