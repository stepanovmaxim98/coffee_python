import sqlite3

connection = sqlite3.connect("coffee.sqlite")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    roast TEXT,
    type TEXT,
    taste TEXT,
    price INTEGER,
    volume INTEGER
)
""")

coffee_data = [
    ("Эфиопия Иргачефф", "Средняя", "В зернах", "Цитрус, ягоды", 1200, 250),
    ("Бразилия Сантос", "Темная", "Молотый", "Шоколад, орехи", 900, 250),
    ("Колумбия Supremo", "Светлая", "В зернах", "Карамель, фрукты", 1400, 500),
]

cursor.executemany(
    """
INSERT INTO coffee (name, roast, type, taste, price, volume)
VALUES (?, ?, ?, ?, ?, ?)
""",
    coffee_data,
)

connection.commit()
connection.close()

print("База данных создана!")
