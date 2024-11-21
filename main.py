import sys
import datetime


from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
#from qtconsole import QtCore


class Task:
    def __init__(self, task, time, completed):
        self.task = task
        self.time = time
        self.completed = completed


class Planner(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle("Планировщик")

        self.tasks = []

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.add_task)

        self.task_list = QListWidget()

        self.filter_cb = QCheckBox("Показать выполненные")
        self.filter_cb.stateChanged.connect(self.show_tasks)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_tasks)

        self.load_btn = QPushButton("Загрузить")
        self.load_btn.clicked.connect(self.load_tasks)

        self.delete_button = QPushButton('Удалить задачу')
        self.delete_button.clicked.connect(self.delete_task)

        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.clicked.connect(self.clear)

        layot = QVBoxLayout()
        self.setLayout(layot)

        layot.addWidget(self.calendar)
        layot.addWidget(self.task_list)
        layot.addWidget(self.filter_cb)
        layot.addWidget(self.delete_button)
        layot.addWidget(self.clear_btn)
        layot.addWidget(self.save_btn)
        layot.addWidget(self.load_btn)

    def add_task(self, date):
        task, ok = QInputDialog.getText(self, "Добавить задачу", "Введите задачу:")
        if ok:
            task_item = QListWidgetItem()
            task_item.task = Task(task, date.toString(), False)
            self.tasks.append(task_item.task)
            self.task_list.addItem(task_item)
            self.task_list.setItemWidget(task_item, q:=QCheckBox(f"{date.toString()} - {task}", self))
            q.stateChanged.connect(self.on_checkbox_changed)

    def show_tasks(self):
        self.task_list.clear()
        completed = self.filter_cb.isChecked()
        filtered_tasks = [task for task in self.tasks if task.completed == completed]

        for task in filtered_tasks:
            task_item = QListWidgetItem(f"{task.time} - {task.task}")
            task_item.task = task
            self.task_list.addItem(task_item)

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task.task},{task.time},{task.completed}\n")

    def load_tasks(self):
        self.tasks = []
        self.task_list.clear()
        with open("tasks.txt", "r") as file:
            for line in file:
                task_str = line.strip().split(",")
                task = Task(task_str[0], task_str[1], task_str[2] == "True")
                self.tasks.append(task)
                task_item = QListWidgetItem(f"{task.time} - {task.task}")
                task_item.task = task
                self.task_list.addItem(task_item)

    def delete_task(self):
        current_row = self.task_list.currentRow()
        if current_row >= 0:
            current_item = self.task_list.takeItem(current_row)
            del current_item

    def clear(self):
        self.task_list.clear()

    def on_checkbox_changed(self):
        box = self.sender()
        if box.isChecked():
             print(box.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Planner()
    ex.show()
    sys.exit(app.exec())