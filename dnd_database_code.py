from flask import Flask, render_template, request, redirect
import sqlite3

DATABASE = 'dndspells.db'

app = Flask(__name__)

@app.route('/spells')
def spell_names():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('SELECT spell_name FROM spell ORDER BY spell_level ASC')
    ret = [i[0] for i in cursor.fetchall()]
    return render_template('spells_index.html', spells=ret)

@app.route('/')
def home():
    return render_template('home_index.html')



@app.route('/spell/<spell>')
def single_spell(spell):
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
    return render_template('single_spell_index.html', details = ret)




if __name__ == '__main__':
    app.run(debug=True)