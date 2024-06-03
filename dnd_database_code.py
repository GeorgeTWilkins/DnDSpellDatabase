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

spell_name = 'Acid Splash'

@app.route(f'/spells/{spell_name}')
def single_spell():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute



if __name__ == '__main__':
    app.run(debug=True)