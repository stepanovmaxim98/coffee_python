import sys
import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from add_edit_coffee import AddEditCoffeeForm


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("main.ui", self)

        self.loadButton.clicked.connect(self.load_data)

        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()

        result = cursor.execute("SELECT * FROM coffee").fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(7)

        headers = ["ID", "Название", "Обжарка", "Тип", "Вкус", "Цена", "Объём"]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(result):
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))

        conn.close()

    def add_coffee(self):
        self.form = AddEditCoffeeForm(refresh_callback=self.load_data)
        self.form.exec()

    def edit_coffee(self):
        row = self.tableWidget.currentRow()

        if row == -1:
            return

        coffee_id = int(self.tableWidget.item(row, 0).text())

        self.form = AddEditCoffeeForm(
            coffee_id=coffee_id,
            refresh_callback=self.load_data
        )
        self.form.exec()


app = QApplication(sys.argv)
window = CoffeeApp()
window.show()
sys.exit(app.exec())