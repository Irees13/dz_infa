import sys
import os

# Добавляем текущую папку в PYTHONPATH, чтобы импорты работали правильно
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QMenuBar, QAction, QMessageBox, QHBoxLayout, QStackedWidget
)
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtCore import Qt
from styles import STYLESHEET

# Импортируем формы
from clients_form import ClientsForm
from cars_form import CarsForm
from employees_form import EmployeesForm
from sales_form import SalesForm
from supplies_form import SuppliesForm
from reports_form import ReportsForm

class AutoSalonApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления автосалоном")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(STYLESHEET)

        # Подключение к БД
        self.connection = QSqlDatabase.addDatabase('QSQLITE')
        self.connection.setDatabaseName('database/autosalon.db')

        if not self.connection.open():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к БД")
            return

        # Меню
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Основной контент
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Главная компоновка: боковая панель + основная область
        main_layout = QHBoxLayout()

        # Боковая панель с кнопками
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(10)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)

        self.label = QLabel("Управление автосалоном")
        self.label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.label)

        # Кнопки навигации
        self.btn_clients = QPushButton("Клиенты")
        self.btn_cars = QPushButton("Автомобили")
        self.btn_employees = QPushButton("Сотрудники")
        self.btn_sales = QPushButton("Продажи")
        self.btn_supplies = QPushButton("Поставки")
        self.btn_reports = QPushButton("Отчёты")

        # Добавляем кнопки в боковую панель
        sidebar_layout.addWidget(self.btn_clients)
        sidebar_layout.addWidget(self.btn_cars)
        sidebar_layout.addWidget(self.btn_employees)
        sidebar_layout.addWidget(self.btn_sales)
        sidebar_layout.addWidget(self.btn_supplies)
        sidebar_layout.addWidget(self.btn_reports)
        sidebar_layout.addStretch()

        sidebar.setLayout(sidebar_layout)
        sidebar.setFixedWidth(250)
        main_layout.addWidget(sidebar)

        # Основная область с формами
        self.stack = QStackedWidget()

        # Инициализация форм с передачей connection
        self.clients_form = ClientsForm(self.connection, parent=self)
        self.cars_form = CarsForm(self.connection, parent=self)
        self.employees_form = EmployeesForm(self.connection, parent=self)
        self.sales_form = SalesForm(self.connection, parent=self)
        self.supplies_form = SuppliesForm(self.connection, parent=self)
        self.reports_form = ReportsForm(self.connection, parent=self)

        # Добавляем формы в QStackedWidget
        self.stack.addWidget(self.clients_form)
        self.stack.addWidget(self.cars_form)
        self.stack.addWidget(self.employees_form)
        self.stack.addWidget(self.sales_form)
        self.stack.addWidget(self.supplies_form)
        self.stack.addWidget(self.reports_form)

        main_layout.addWidget(self.stack)
        self.central_widget.setLayout(main_layout)

        # События кнопок (переключение страниц)
        self.btn_clients.clicked.connect(lambda: self.stack.setCurrentWidget(self.clients_form))
        self.btn_cars.clicked.connect(lambda: self.stack.setCurrentWidget(self.cars_form))
        self.btn_employees.clicked.connect(lambda: self.stack.setCurrentWidget(self.employees_form))
        self.btn_sales.clicked.connect(lambda: self.stack.setCurrentWidget(self.sales_form))
        self.btn_supplies.clicked.connect(lambda: self.stack.setCurrentWidget(self.supplies_form))
        self.btn_reports.clicked.connect(lambda: self.stack.setCurrentWidget(self.reports_form))

        # Устанавливаем начальную страницу
        self.stack.setCurrentWidget(self.clients_form)


    def closeEvent(self, event):
        self.connection.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoSalonApp()
    window.show()
    sys.exit(app.exec_())