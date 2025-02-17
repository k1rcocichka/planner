import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QCalendarWidget, QInputDialog, QCheckBox, QLabel, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt, QTranslator, QLocale
from PyQt6.QtGui import QColor


class Task:
    """Класс для хранения информации о задаче."""
    def __init__(self, task, time, completed=False, color="#ffffff"):
        self.task = task
        self.time = time
        self.completed = completed
        self.color = color


class Planner(QWidget):
    """Основной класс приложения."""
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.initUI()

    def initUI(self):
        """Инициализация интерфейса."""
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle("Планировщик")
        
        self.tasks = []

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.add_task)

        self.task_list = QListWidget()
        
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

        self.task_list.itemDoubleClicked.connect(self.edit_task)

        self.color_cb = QComboBox()
        self.color_cb.addItem("Красный")
        self.color_cb.addItem("Оранжевый")
        self.color_cb.addItem("Жёлтый")
        self.color_cb.addItem("Зелёный")

        self.color = "Красный"

        """словарь с хешами цветов"""
        self.color_dict = {"Красный": "#e80000",
                           "Оранжевый": "#ff8c00",
                           "Жёлтый": "#ffd000",
                           "Зелёный": "#4fb76c",}

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
        layot3.addLayout(layot2)

        """лайауты в лайаут"""
        layot4.addLayout(layot3)
        self.setLayout(layot4)

        self.load_tasks()

    def add_task(self, date):
        """Добавление новой задачи."""
        task, ok = QInputDialog.getText(self, "Добавить задачу", "Введите задачу:")
        if ok and task:
            new_task = Task(task, date.toString())  # По умолчанию цвет фона — белый
            self.tasks.append(new_task)
            self.update_task_list()

        self.save_tasks()

    def update_task_list(self, filter_text="Показать все"):
        """Обновление списка задач."""
        self.task_list.clear()
        for task in self.tasks:
            if filter_text == "Показать выполненные" and not task.completed:
                continue
            if filter_text == "Показать невыполненные" and task.completed:
                continue

            item = QListWidgetItem(f"    {task.time} - {task.task}")
            item.task = task
            item.setBackground(QColor(task.color))  # Устанавливаем цвет фона
            self.task_list.addItem(item)
            checkbox = QCheckBox()
            checkbox.setChecked(task.completed)
            checkbox.stateChanged.connect(lambda state, t=task: self.on_checkbox_changed(t, state))
            self.task_list.setItemWidget(item, checkbox)
    

    def on_checkbox_changed(self, task, state):
        """Обработка изменения состояния чекбокса."""
        task.completed = state == Qt.CheckState.Checked.value
        self.save_tasks()

    def filter(self):
        """Фильтрация задач."""
        filter_text = self.parametr_cb.currentText()
        self.update_task_list(filter_text)

    def save_tasks(self):
        """Сохранение задач в файл."""
        try:
            with open("tasks.txt", "w") as file:
                for task in self.tasks:
                    file.write(f"{task.task},{task.time},{task.completed},{task.color}\n")  # Сохраняем цвет
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить задачи: {e}")

    def load_tasks(self):
        """Загрузка задач из файла."""
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = []
                for line in file:
                    task_str = line.strip().split(",")
                    task = Task(
                        task_str[0],
                        task_str[1],
                        task_str[2] == "True",
                        task_str[3] if len(task_str) > 3 else "#ffffff"  # Загружаем цвет
                    )
                    self.tasks.append(task)
            self.update_task_list()
            QMessageBox.information(self, "Успех", "Задачи успешно загружены.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить задачи: {e}")

    def delete_task(self):
        """Удаление выбранной задачи."""
        current_item = self.task_list.currentItem()
        if current_item:
            self.tasks.remove(current_item.task)
            self.update_task_list()
        self.save_tasks()

    def color_change(self):
        """Изменение цвета фона выбранной задачи."""
        current_item = self.task_list.currentItem()
        if current_item:
            selected_color = self.color_cb.currentText()
            color_hex = self.color_dict.get(selected_color, "#ffffff")  # Получаем HEX-код цвета
            current_item.task.color = color_hex  # Обновляем цвет в объекте задачи
            current_item.setBackground(QColor(color_hex))  # Применяем цвет к элементу списка
        self.save_tasks()

    def clear(self):
        """Очистка списка задач."""
        self.tasks = []
        self.update_task_list()
        self.save_tasks()

    def edit_task(self, item):
        task = item.task
        new_task, ok = QInputDialog.getText(self, "Редактировать задачу", "Введите новую задачу:", text=task.task)
        if ok and new_task:
            task.task = new_task
            self.update_task_list()
            self.save_tasks()
    
def my_hook(cls, exception, traceback):
    """дебаггер"""
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    planner = Planner()
    planner.show()
    sys.excepthook = my_hook
    sys.exit(app.exec())