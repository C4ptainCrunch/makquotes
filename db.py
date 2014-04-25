# coding: utf-8

import sqlite3

conn = sqlite3.connect('quotes.db')
c = conn.cursor()

c.execute('''CREATE TABLE quotes (id int, quote text, likes int, hide int)''')

text = open("result").readlines()
text = map(lambda x: x.strip(), text)

i = 0
for line in text:
    values = (i, line.decode('utf8'))
    c.execute("INSERT INTO quotes  VALUES (?, ?, 0, 0)", values)
    i += 1

conn.commit()
conn.close()
