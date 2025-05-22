from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QDateEdit, QFormLayout, QMessageBox, QFileDialog, QComboBox, QLineEdit, QLabel, QItemDelegate, QHeaderView
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from styles import STYLESHEET

class NumberFormatDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def displayText(self, value, locale):
        try:
            # Преобразуем число в строку с двумя знаками после запятой
            return "{:.2f}".format(float(value)) if value is not None else ""
        except (ValueError, TypeError):
            return str(value)

class ReportsForm(QWidget):
    def __init__(self, connection, parent=None):
        super().__init__(parent)
        self.connection = connection
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Выбор типа отчета
        self.report_type = QComboBox()
        self.report_type.addItems([
            "Общая сумма продаж по дате",
            "Самые активные клиенты",
            "Топ проданных автомобилей",
            "Поставки",
            "Средняя цена автомобиля по марке",
            "Статистика по типам оплаты",
            "Автомобили в наличии",
            "Эффективность сотрудников"
        ])
        self.report_type.currentIndexChanged.connect(self.update_form)

        # Форма для ввода параметров
        self.form_layout = QFormLayout()

        # Создаем виджеты и их метки
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date_label = QLabel("Начальная дата:")

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date_label = QLabel("Конечная дата:")

        # Изначально показываем поля для дат
        self.form_layout.addRow(self.start_date_label, self.start_date)
        self.form_layout.addRow(self.end_date_label, self.end_date)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.generate_button = QPushButton("Сгенерировать отчет")
        self.generate_button.clicked.connect(self.generate_report)
        self.export_button = QPushButton("Экспортировать в CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        buttons_layout.addWidget(self.generate_button)
        buttons_layout.addWidget(self.export_button)

        # Таблица для отображения результатов
        self.table_view = QTableView()
        self.model = QSqlQueryModel()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # форматирования чисел
        delegate = NumberFormatDelegate(self.table_view)
        self.table_view.setItemDelegate(delegate)

        # Добавляем элементы в layout
        layout.addWidget(self.report_type)
        layout.addLayout(self.form_layout)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

        # Применяем стили
        self.setStyleSheet(STYLESHEET)

    def update_form(self):
        # Скрываем все виджеты
        self.start_date_label.hide()
        self.start_date.hide()
        self.end_date_label.hide()
        self.end_date.hide()

        # Показываем нужные поля в зависимости от типа отчета
        report_type = self.report_type.currentText()
        if report_type in [
            "Общая сумма продаж по дате",
            "Самые активные клиенты",
            "Топ проданных автомобилей",
            "Поставки",
            "Статистика по типам оплаты",
            "Эффективность сотрудников"
        ]:
            self.start_date_label.show()
            self.start_date.show()
            self.end_date_label.show()
            self.end_date.show()

    def generate_report(self):
        report_type = self.report_type.currentText()
        query = QSqlQuery(self.connection)
        start_date = self.start_date.date().toString(Qt.ISODate)
        end_date = self.end_date.date().toString(Qt.ISODate)

        if report_type == "Общая сумма продаж по дате":
            query_str = """
            SELECT strftime('%Y-%m-%d', sale_date) AS sale_date, 
                   CAST(SUM(total_price) AS DECIMAL(15, 2)) AS total_sales
            FROM Sales
            WHERE sale_date BETWEEN ? AND ?
            GROUP BY sale_date
            ORDER BY sale_date
            """
            query.prepare(query_str)
            query.addBindValue(start_date)
            query.addBindValue(end_date)
            if query.exec_():
                self.model.setQuery(query)
                self.model.setHeaderData(0, Qt.Horizontal, "Дата")
                self.model.setHeaderData(1, Qt.Horizontal, "Общая сумма продаж")
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить запрос: {query.lastError().text()}")

        elif report_type == "Самые активные клиенты":
            query_str = """
            SELECT 
                c.client_id,
                c.full_name,
                COUNT(s.sale_id) AS purchase_count,
                CAST(SUM(s.total_price) AS DECIMAL(15, 2)) AS total_spent
            FROM Sales s
            JOIN Clients c ON s.client_id = c.client_id
            WHERE s.sale_date BETWEEN ? AND ?
            GROUP BY c.client_id, c.full_name
            ORDER BY purchase_count DESC
            LIMIT 5
            """
            query.prepare(query_str)
            query.addBindValue(start_date)
            query.addBindValue(end_date)
            if query.exec_():
                self.model.setQuery(query)
                self.model.setHeaderData(0, Qt.Horizontal, "ID клиента")
                self.model.setHeaderData(1, Qt.Horizontal, "ФИО")
                self.model.setHeaderData(2, Qt.Horizontal, "Количество покупок")
                self.model.setHeaderData(3, Qt.Horizontal, "Общая сумма")
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить запрос: {query.lastError().text()}")

        elif report_type == "Топ проданных автомобилей":
            query_str = """
            SELECT 
                c.car_id,
                cm.name AS model_name,
                m.name AS manufacturer_name,
                COUNT(s.sale_id) AS sales_count,
                CAST(SUM(s.total_price) AS DECIMAL(15, 2)) AS total_revenue
            FROM Sales s
            JOIN Cars c ON s.car_id = c.car_id
            JOIN CarModels cm ON c.model_id = cm.model_id
            JOIN Manufacturers m ON cm.manufacturer_id = m.manufacturer_id
            WHERE s.sale_date BETWEEN ? AND ?
            GROUP BY c.car_id, cm.name, m.name
            ORDER BY sales_count DESC
            LIMIT 5
            """
            query.prepare(query_str)
            query.addBindValue(start_date)
            query.addBindValue(end_date)
            if query.exec_():
                self.model.setQuery(query)
                self.model.setHeaderData(0, Qt.Horizontal, "ID авто")
                self.model.setHeaderData(1, Qt.Horizontal, "Модель")
                self.model.setHeaderData(2, Qt.Horizontal, "Производитель")
                self.model.setHeaderData(3, Qt.Horizontal, "Количество продаж")
                self.model.setHeaderData(4, Qt.Horizontal, "Общая выручка")
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить запрос: {query.lastError().text()}")

        elif report_type == "Поставки":
            query_str = """
            SELECT 
                s.supply_id,
                m.name AS manufacturer_name,
                s.count,
                s.supply_date
            FROM Supplies s
            JOIN Manufacturers m ON s.manufacturer_id = m.manufacturer_id
            WHERE s.supply_date BETWEEN ? AND ?
            ORDER BY s.supply_date
            """
            query.prepare(query_str)
            query.addBindValue(start_date)
            query.addBindValue(end_date)
            if query.exec_():
                self.model.setQuery(query)
                self.model.setHeaderData(0, Qt.Horizontal, "ID поставки")
                self.model.setHeaderData(1, Qt.Horizontal, "Производитель")
                self.model.setHeaderData(2, Qt.Horizontal, "Количество")
                self.model.setHeaderData(3, Qt.Horizontal, "Дата поставки")
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить запрос: {query.lastError().text()}")

        elif report_type == "Средняя цена автомобиля по марке":
            query_str = """
            SELECT 
                m.name AS manufacturer_name,
                CAST(AVG(c.price) AS DECIMAL(15, 2)) AS avg_price
            FROM Cars c
            JOIN CarModels cm ON c.model_id = cm.model_id
            JOIN Manufacturers m ON cm.manufacturer_id = m.manufacturer_id
            GROUP BY m.manufacturer_id, m.name
            ORDER BY avg_price DESC
            """
            if query.exec_(query_str):
                self.model.setQuery(query)
                self.model.setHeaderData(0, Qt.Horizontal, "Производитель")
                self.model.setHeaderData(1, Qt.Horizontal, "Средняя цена")
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить запрос: {query.lastError().text()}")

        elif report_type == "Статистика по типам оплаты":
            query_str = """
            SELECT 
                s.payment_method,
                COUNT(s.sale_id) AS transaction_count,
                CAST(SUM(s.total_price) AS DECIMAL(15, 2)) AS total_amount
            FROM Sales s
            WHERE s.sale_date BETWEEN ? AND ?
            GROUP BY s.payment_method
            ORDER BY transaction_count DESC
            """
            query.prepare(query_str)
            query.addBindValue(start_date)
            query.addBindValue(end_date)
            if query.exec_():
                self.model.setQuery(query)
                self.model.setHeaderData(0, Qt.Horizontal, "Способ оплаты")
                self.model.setHeaderData(1, Qt.Horizontal, "Количество транзакций")
                self.model.setHeaderData(2, Qt.Horizontal, "Общая сумма")
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить запрос: {query.lastError().text()}")

        elif report_type == "Автомобили в наличии":
            query_str = """
            SELECT 
                c.car_id,
                cm.name AS model_name,
                m.name AS manufacturer_name,
                c.color,
                c.year,
                CAST(c.price AS DECIMAL(15, 2)) AS price
            FROM Cars c
            JOIN CarModels cm ON c.model_id = cm.model_id
            JOIN Manufacturers m ON cm.manufacturer_id = m.manufacturer_id
            WHERE c.in_stock = TRUE
            ORDER BY c.car_id
            """
            if query.exec_(query_str):
                self.model.setQuery(query)
                self.model.setHeaderData(0, Qt.Horizontal, "ID авто")
                self.model.setHeaderData(1, Qt.Horizontal, "Модель")
                self.model.setHeaderData(2, Qt.Horizontal, "Производитель")
                self.model.setHeaderData(3, Qt.Horizontal, "Цвет")
                self.model.setHeaderData(4, Qt.Horizontal, "Год")
                self.model.setHeaderData(5, Qt.Horizontal, "Цена")
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить запрос: {query.lastError().text()}")

        elif report_type == "Эффективность сотрудников":
            query_str = """
            SELECT 
                e.employee_id,
                e.full_name,
                e.position,
                COUNT(s.sale_id) AS sales_count,
                CAST(SUM(s.total_price) AS DECIMAL(15, 2)) AS total_sales
            FROM Employees e
            LEFT JOIN Sales s ON e.employee_id = s.employee_id
            WHERE s.sale_date BETWEEN ? AND ? OR s.sale_date IS NULL
            GROUP BY e.employee_id, e.full_name, e.position
            ORDER BY total_sales DESC
            """
            query.prepare(query_str)
            query.addBindValue(start_date)
            query.addBindValue(end_date)
            if query.exec_():
                self.model.setQuery(query)
                self.model.setHeaderData(0, Qt.Horizontal, "ID сотрудника")
                self.model.setHeaderData(1, Qt.Horizontal, "ФИО")
                self.model.setHeaderData(2, Qt.Horizontal, "Должность")
                self.model.setHeaderData(3, Qt.Horizontal, "Количество продаж")
                self.model.setHeaderData(4, Qt.Horizontal, "Общая сумма продаж")
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить запрос: {query.lastError().text()}")

    def export_to_csv(self):
        if self.model.rowCount() == 0:
            QMessageBox.warning(self, "Предупреждение", "Нет данных для экспорта!")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить отчет", "", "CSV Files (*.csv)")
        if not file_name:
            return

        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                headers = [self.model.headerData(i, Qt.Horizontal) for i in range(self.model.columnCount())]
                f.write(','.join(headers) + '\n')
                for row in range(self.model.rowCount()):
                    row_data = []
                    for col in range(self.model.columnCount()):
                        data = str(self.model.data(self.model.index(row, col)))
                        try:
                            # Форматируем числа с двумя знаками после запятой
                            num = float(data)
                            data = "{:.2f}".format(num)
                        except (ValueError, TypeError):
                            pass
                        row_data.append(data.replace(',', ';'))
                    f.write(','.join(row_data) + '\n')
            QMessageBox.information(self, "Успех", "Отчет успешно экспортирован!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать отчет: {str(e)}")