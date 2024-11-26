import sys
import datetime


from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class Task:
    def __init__(self, task, time, completed, color):
        self.task = task
        self.time = time
        self.completed = completed
        self.color = color


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
        
        self.delete_btn = QPushButton('Удалить задачу')
        self.delete_btn.setStyleSheet('QPushButton {background-color: #274c77}')
        self.delete_btn.clicked.connect(self.delete_task)
        
        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.setStyleSheet('QPushButton {background-color: #274c77}')
        self.clear_btn.clicked.connect(self.clear)

        self.color_btn = QPushButton("Изменить цвет")
        self.color_btn.setStyleSheet('QPushButton {background-color: #274c77}')
        self.color_btn.clicked.connect(self.color_change)
        
        self.parametr_cb = QComboBox()
        self.parametr_cb.addItem("Показать все")
        self.parametr_cb.addItem("Показать выполненные")
        self.parametr_cb.addItem("Показать невыполненные")
        self.parametr_cb.activated.connect(self.filter)

        self.color_cb = QComboBox()
        self.color_cb.addItem("Красный")
        self.color_cb.addItem("Оранжевый")
        self.color_cb.addItem("Жёлтый")
        self.color_cb.addItem("Зелёный")

        
        self.color = "Красный"
        self.color_dict = {"Красный": "#e80000",
                           "Оранжевый": "#7fc97f",
                           "Жёлтый": "#7fc97f",
                           "Зелёный": "#7fc97f",}
        self.brush = QBrush()

        self.parametr_lb = QLabel('Параметры:')
        self.parametr_lb.setStyleSheet('font-family: Courier New; font-size: 14px;')

        self.task_lb = QLabel('Задачи:')
        self.task_lb.setStyleSheet('font-family: Courier New; font-size: 14px;')

        self.use_lb = QLabel('Взаимодействия:')
        self.use_lb.setStyleSheet('font-family: Courier New; font-size: 14px;')

        layot1 = QVBoxLayout()
        layot2 = QVBoxLayout()
        layot3 = QHBoxLayout()
        layot4 = QVBoxLayout()

        layot4.addWidget(self.calendar)
        layot1.addWidget(self.task_lb)
        layot1.addWidget(self.task_list)
        layot1.addWidget(self.parametr_lb)
        layot1.addWidget(self.parametr_cb)
        layot1.addWidget(self.color_cb)
        layot1.addWidget(self.color_btn)
        layot3.addLayout(layot1)

        layot2.addWidget(self.use_lb)
        layot2.addWidget(self.delete_btn)
        layot2.addWidget(self.clear_btn)
        layot2.addWidget(self.save_btn)
        layot2.addWidget(self.load_btn)
        layot3.addLayout(layot2)

        layot4.addLayout(layot3)
        self.setLayout(layot4)

    def add_task(self, date):
        task, ok = QInputDialog.getText(self, "Добавить задачу", "Введите задачу:")
        if ok:
            task_item = QListWidgetItem()
            task_item.task = Task(task, date.toString(), False, 'Обычный')
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
                file.write(f"{task.task},{task.time},{task.completed},{task.color}\n")

    def load_tasks(self):
        self.tasks = []
        self.task_list.clear()
        with open("tasks.txt", "r") as file:
            for line in file:
                task_str = line.strip().split(",")
                task = Task(task_str[0], task_str[1], task_str[2] == "True", task_str[3])
                self.tasks.append(task)
                task_item = QListWidgetItem(f"{task.time} - {task.task}")
                task_item.task = task
                self.task_list.addItem(task_item)

    def delete_task(self): #нужна хелпа
        current_row = self.task_list.currentRow()
        if current_row >= 0:
            current_item = self.task_list.takeItem(current_row)
            del current_item
        
    def color_change(self):
        current_row = self.task_list.currentRow()
        if current_row >= 0:
            current_item = self.task_list.item(current_row)
            brush = QBrush(QColor(self.color_dict[self.color_cb.currentText()]))
            current_item.setBackground(brush)
            self.update()
            print("change color")
            
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
