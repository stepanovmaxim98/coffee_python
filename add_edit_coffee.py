import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog


class AddEditCoffeeForm(QDialog):
    def __init__(self, coffee_id=None, refresh_callback=None):
        super().__init__()

        uic.loadUi("addEditCoffeeForm.ui", self)

        self.coffee_id = coffee_id
        self.refresh_callback = refresh_callback

        self.saveButton.clicked.connect(self.save_data)
        self.cancelButton.clicked.connect(self.close)

        if self.coffee_id:
            self.load_data()

    def load_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()

        result = cursor.execute(
            "SELECT name, roast, type, taste, price, volume FROM coffee WHERE id=?",
            (self.coffee_id,)
        ).fetchone()

        conn.close()

        if result:
            self.nameEdit.setText(result[0])
            self.roastEdit.setText(result[1])
            self.typeEdit.setText(result[2])
            self.tasteEdit.setText(result[3])
            self.priceEdit.setValue(result[4])
            self.volumeEdit.setValue(result[5])

    def save_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()

        data = (
            self.nameEdit.text(),
            self.roastEdit.text(),
            self.typeEdit.text(),
            self.tasteEdit.text(),
            self.priceEdit.value(),
            self.volumeEdit.value()
        )

        if self.coffee_id:
            cursor.execute("""
                UPDATE coffee
                SET name=?, roast=?, type=?, taste=?, price=?, volume=?
                WHERE id=?
            """, data + (self.coffee_id,))
        else:
            cursor.execute("""
                INSERT INTO coffee (name, roast, type, taste, price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, data)

        conn.commit()
        conn.close()

        if self.refresh_callback:
            self.refresh_callback()

        self.close()