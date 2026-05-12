import sys
import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("main.ui", self)

        self.loadButton.clicked.connect(self.load_data)

    def load_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        result = cursor.execute("""
        SELECT * FROM coffee
        """).fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(7)

        headers = [
            "ID",
            "Название",
            "Обжарка",
            "Тип",
            "Описание вкуса",
            "Цена",
            "Объем",
        ]

        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(result):
            for column_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_index, column_index, item)

        connection.close()


app = QApplication(sys.argv)

window = CoffeeApp()
window.show()

sys.exit(app.exec())
