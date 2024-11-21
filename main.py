import sys
import datetime


from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


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

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setStyleSheet('QPushButton {background-color: #274c77}')
        self.save_btn.clicked.connect(self.save_tasks)

        self.load_btn = QPushButton("Загрузить")
        self.load_btn.setStyleSheet('QPushButton {background-color: #274c77}')
        self.load_btn.clicked.connect(self.load_tasks)
        
        self.delete_button = QPushButton('Удалить задачу')
        self.delete_button.setStyleSheet('QPushButton {background-color: #274c77}')
        self.delete_button.clicked.connect(self.delete_task)
        
        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.setStyleSheet('QPushButton {background-color: #274c77}')
        self.clear_btn.clicked.connect(self.clear)
        
        self.combobox = QComboBox()
        self.combobox.addItem("Показать все")
        self.combobox.addItem("Показать выполненные")
        self.combobox.addItem("Показать невыполненные")
        self.combobox.activated.connect(self.filter)

        self.labelpm = QLabel('Параметры:')
        self.labelpm.setStyleSheet('font-family: Courier New; font-size: 14px;')

        self.labeltask = QLabel('Задачи:')
        self.labeltask.setStyleSheet('font-family: Courier New; font-size: 14px;')

        layot = QVBoxLayout()
        self.setLayout(layot)

        layot.addWidget(self.calendar)
        layot.addWidget(self.labeltask)
        layot.addWidget(self.task_list)
        layot.addWidget(self.labelpm)
        layot.addWidget(self.combobox)
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

    def filter(self):
        sender = self.sender()
        if sender.currentText() == "Показать выполненные":
            print("Показать выполненные")
            self.task_list.clear()
            filtered_tasks = [task for task in self.tasks if task.completed == True]

            for task in filtered_tasks:
                task_item = QListWidgetItem()
                task_item.task = task
                self.task_list.addItem(task_item)
                self.task_list.setItemWidget(task_item, q:=QCheckBox(f"{task.time} - {task.task}", self))
                q.stateChanged.connect(self.on_checkbox_changed)
                if task.completed:
                    q.setChecked(True)
                else:
                    q.setChecked(False)

        elif sender.currentText() == "Показать невыполненные":
            print("Показать невыполненные")
            self.task_list.clear()
            filtered_tasks = [task for task in self.tasks if task.completed == False]
            for task in filtered_tasks:
                task_item = QListWidgetItem()
                task_item.task = task
                self.task_list.addItem(task_item)
                self.task_list.setItemWidget(task_item, q:=QCheckBox(f"{task.time} - {task.task}", self))
                q.stateChanged.connect(self.on_checkbox_changed)
                if task.completed:
                    q.setChecked(True)
                else:
                    q.setChecked(False)

        else:
            print("Показать все")
            self.task_list.clear()
            for task in self.tasks:
                task_item = QListWidgetItem()
                task_item.task = task
                self.task_list.addItem(task_item)
                self.task_list.setItemWidget(task_item, q:=QCheckBox(f"{task.time} - {task.task}", self))
                q.stateChanged.connect(self.on_checkbox_changed)
                if task.completed:
                    q.setChecked(True)
                else:
                    q.setChecked(False)
 
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

    def delete_task(self): #нужна помощь Ильи
        current_row = self.task_list.currentRow()
        if current_row >= 0:
            current_item = self.task_list.takeItem(current_row)
            del current_item

    def clear(self):
        self.task_list.clear()

    def on_checkbox_changed(self):
        sender: QCheckBox = self.sender()
        control = [control for control in self.tasks if control.task in sender.text()]
        if sender.isChecked():
            control[0].completed = True
        else:
            control[0].completed = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Planner()
    ex.show()
    sys.exit(app.exec())