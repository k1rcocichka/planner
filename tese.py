import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QCalendarWidget, QInputDialog, QCheckBox, QLabel, QComboBox, QMessageBox, QDialog, QTextEdit
)
from PyQt6.QtCore import Qt, QTranslator
from PyQt6.QtGui import QColor


class Task:
    """Класс для хранения информации о задаче."""
    def __init__(self, task, time, note="", completed=False, color="#ffffff"):
        self.task = task
        self.time = time
        self.note = note  # Записка (описание задачи)
        self.completed = completed
        self.color = color  # Цвет фона задачи


class TaskDialog(QDialog):
    """Диалоговое окно для добавления задачи с запиской."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Добавить задачу"))
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        # Поле для ввода названия задачи
        self.task_input = QTextEdit()
        self.task_input.setPlaceholderText(self.tr("Введите задачу..."))
        layout.addWidget(self.task_input)

        # Поле для ввода записки
        self.note_input = QTextEdit()
        self.note_input.setPlaceholderText(self.tr("Добавьте описание..."))
        layout.addWidget(self.note_input)

        # Кнопки
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton(self.tr("Добавить"))
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton(self.tr("Отмена"))
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_task_data(self):
        """Возвращает введенные данные."""
        return self.task_input.toPlainText(), self.note_input.toPlainText()


class AboutWindow(QDialog):
    """Окно 'О программе'."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("О программе"))
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        # Текст о программе
        about_text = QLabel(self.tr(
            "Планировщик задач\n\n"
            "Версия 1.0\n"
            "Автор: Ваше Имя\n"
            "© 2023"
        ))
        about_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(about_text)

        # Кнопка закрытия
        close_btn = QPushButton(self.tr("Закрыть"))
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)


class Planner(QWidget):
    """Основной класс приложения."""
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.initUI()

    def initUI(self):
        """Инициализация интерфейса."""
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle(self.tr("Планировщик задач"))

        # Виджеты
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.add_task)

        self.task_list = QListWidget()

        self.save_btn = QPushButton(self.tr("Сохранить"))
        self.save_btn.clicked.connect(self.save_tasks)

        self.load_btn = QPushButton(self.tr("Загрузить"))
        self.load_btn.clicked.connect(self.load_tasks)

        self.delete_btn = QPushButton(self.tr("Удалить задачу"))
        self.delete_btn.clicked.connect(self.delete_task)

        self.clear_btn = QPushButton(self.tr("Очистить"))
        self.clear_btn.clicked.connect(self.clear)

        self.color_btn = QPushButton(self.tr("Изменить цвет"))
        self.color_btn.clicked.connect(self.color_change)

        self.about_btn = QPushButton(self.tr("О программе"))
        self.about_btn.clicked.connect(self.show_about_window)

        self.parametr_cb = QComboBox()
        self.parametr_cb.addItems([
            self.tr("Показать все"),
            self.tr("Показать выполненные"),
            self.tr("Показать невыполненные")
        ])
        self.parametr_cb.activated.connect(self.filter)

        self.color_cb = QComboBox()
        self.color_cb.addItems([
            self.tr("Красный"),
            self.tr("Оранжевый"),
            self.tr("Жёлтый"),
            self.tr("Зелёный")
        ])

        # Цвета
        self.color_dict = {
            self.tr("Красный"): "#e80000",
            self.tr("Оранжевый"): "#ff8c00",
            self.tr("Жёлтый"): "#ffd000",
            self.tr("Зелёный"): "#4fb76c",
        }

        # Лейауты
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.task_list)
        layout.addWidget(self.parametr_cb)
        layout.addWidget(self.color_cb)
        layout.addWidget(self.color_btn)
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.load_btn)
        layout.addWidget(self.about_btn)
        self.setLayout(layout)

    def add_task(self, date):
        """Добавление новой задачи."""
        dialog = TaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task, note = dialog.get_task_data()
            if task:
                new_task = Task(task, date.toString(), note)
                self.tasks.append(new_task)
                self.update_task_list()

    def update_task_list(self, filter_text=None):
        """Обновление списка задач."""
        if filter_text is None:
            filter_text = self.parametr_cb.currentText()
        self.task_list.clear()
        for task in self.tasks:
            if filter_text == self.tr("Показать выполненные") and not task.completed:
                continue
            if filter_text == self.tr("Показать невыполненные") and task.completed:
                continue

            item = QListWidgetItem(f"{task.time} - {task.task}")
            item.task = task
            item.setBackground(QColor(task.color))  # Устанавливаем цвет фона
            if task.note:
                item.setToolTip(self.tr("Описание: ") + task.note)  # Добавляем подсказку с описанием
            self.task_list.addItem(item)
            checkbox = QCheckBox()
            checkbox.setChecked(task.completed)
            checkbox.stateChanged.connect(lambda state, t=task: self.on_checkbox_changed(t, state))
            self.task_list.setItemWidget(item, checkbox)

    def on_checkbox_changed(self, task, state):
        """Обработка изменения состояния чекбокса."""
        task.completed = state == Qt.CheckState.Checked.value

    def filter(self):
        """Фильтрация задач."""
        filter_text = self.parametr_cb.currentText()
        self.update_task_list(filter_text)

    def save_tasks(self):
        """Сохранение задач в файл."""
        try:
            with open("tasks.txt", "w") as file:
                for task in self.tasks:
                    file.write(f"{task.task},{task.time},{task.completed},{task.color},{task.note}\n")
            QMessageBox.information(self, self.tr("Успех"), self.tr("Задачи успешно сохранены."))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Ошибка"), self.tr(f"Не удалось сохранить задачи: {e}"))

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
                        task_str[4] if len(task_str) > 4 else "",  # Загружаем записку
                        task_str[2] == "True",
                        task_str[3] if len(task_str) > 3 else "#ffffff"
                    )
                    self.tasks.append(task)
            self.update_task_list()
            QMessageBox.information(self, self.tr("Успех"), self.tr("Задачи успешно загружены."))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Ошибка"), self.tr(f"Не удалось загрузить задачи: {e}"))

    def delete_task(self):
        """Удаление выбранной задачи."""
        current_item = self.task_list.currentItem()
        if current_item:
            self.tasks.remove(current_item.task)
            self.update_task_list()

    def color_change(self):
        """Изменение цвета фона выбранной задачи."""
        current_item = self.task_list.currentItem()
        if current_item:
            selected_color = self.color_cb.currentText()
            color_hex = self.color_dict.get(selected_color, "#ffffff")
            current_item.task.color = color_hex
            current_item.setBackground(QColor(color_hex))

    def clear(self):
        """Очистка списка задач."""
        self.tasks = []
        self.update_task_list()

    def show_about_window(self):
        """Открытие окна 'О программе'."""
        about_window = AboutWindow()
        about_window.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Загрузка перевода
    translator = QTranslator()
    if translator.load("planner_ru.qm"):
        app.installTranslator(translator)

    planner = Planner()
    planner.show()
    sys.exit(app.exec())