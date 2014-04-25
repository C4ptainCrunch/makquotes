import sqlite3
import cgi
import random
from flask import Flask, g, abort, url_for, redirect, render_template, make_response, request

app = Flask(__name__)
DATABASE = 'quotes.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def count_rows(table):
    cur = get_db().execute("SELECT Count() FROM %s" % table)
    c = cur.fetchone()[0]
    cur.close()
    return c


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    count = count_rows("quotes")
    id = query_db("SELECT id FROM quotes LIMIT ?,1", (random.randint(0, count),), True)[0]
    return redirect(url_for('quote', id=id))


@app.route('/quote/<id>')
def quote(id):
    row = query_db("SELECT * FROM quotes WHERE id=?", (id,), True)
    if row is None:
        abort(404)

    id, quote, likes, hide = row
    hide = hide == 1
    return render_template('quote.html', quote=quote, id=id, likes=likes)


@app.route('/like/<id>')
def like(id):
    liked = request.cookies.get('poney', "")
    liked = liked.split(" ") if liked else []
    if id in liked:
        return redirect(url_for('quote', id=id))
    liked.append(str(id))
    row = query_db("SELECT * FROM quotes WHERE id=?", (id,), True)
    if row is None:
        abort(404)

    id, quote, likes, hide = row

    newlikes = likes + 1
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE quotes SET likes=? WHERE id=?", (newlikes, id,))
    db.commit()
    cur.close()
    response = make_response(redirect(url_for('quote', id=id)))
    response.set_cookie('poney', " ".join(liked))
    return response


if __name__ == "__main__":
    app.run(debug=True)
