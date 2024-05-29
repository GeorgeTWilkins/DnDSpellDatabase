from flask import Flask, render_template
import sqlite3

DATABASE = 'dndspells.db'

app = Flask(__name__)
@app.route('/')
def spell_names():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('SELECT spell_name FROM spell ORDER BY spell_level ASC')
    ret = [i[0] for i in cursor.fetchall()]
    return render_template('spell_names_index.html', spells=ret)


if __name__ == '__main__':
    app.run(debug=True)