import sqlite3

conn = sqlite3.connect("qw1.db")
cursor = conn.cursor()

id = input("Введите id сообщества: ")
minTimePostSec = input("Введите минимальное время добавления поста(в секундах): ")
warnSlowa = input("Введите запрещенные слова через пробел: ")
obyazSlowa = input("Введите обязательные слова через пробел: ")
sets = "INSERT INTO vktb1 (id, minTimePostSec, warnSlowa, obyazSlowa) VALUES (" + "\"" + id + "\"" + "," + "\"" + minTimePostSec + "\"" + "," + "\"" + warnSlowa + "\"" + "," + "\"" + obyazSlowa + "\"" + ")"
cursor.execute(sets)
conn.commit()

