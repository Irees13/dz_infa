from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QPushButton, QHBoxLayout, QMessageBox, QFormLayout, QDialog, QItemDelegate, QLineEdit, QHeaderView
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtCore import Qt, QDate
from styles import STYLESHEET
import sys

class NumberFormatDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def displayText(self, value, locale):
        try:
            return "{:.0f}".format(float(value)) if value is not None else ""
        except (ValueError, TypeError):
            return str(value)

class BaseEditDialog(QDialog):
    def __init__(self, record_id, table_name, fields, connection, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Редактирование записи в {table_name}")
        self.connection = connection
        self.record_id = record_id
        self.table_name = table_name
        self.fields = fields
        self.setStyleSheet(STYLESHEET)

        layout = QVBoxLayout()

        # Получаем текущие данные записи
        query = QSqlQuery(self.connection)
        query.prepare(f"SELECT * FROM {self.table_name} WHERE {self.fields[0]['name']} = ?")
        query.addBindValue(self.record_id)
        if not query.exec_():
            QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить запрос: {query.lastError().text()}")
            self.reject()
            return
        if not query.next():
            QMessageBox.critical(self, "Ошибка", f"Запись с ID {self.record_id} не найдена!")
            self.reject()
            return

        # Создаем поля для редактирования
        self.inputs = {}
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignLeft)
        form_layout.setHorizontalSpacing(10)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)

        for field in self.fields[1:]:  # Пропускаем ID при редактировании
            field_name = field['name']
            value = query.value(field_name)
            input_widget = field['widget']()
            
            # Настройка значений в зависимости от типа виджета
            if isinstance(input_widget, QLineEdit):
                if field_name in ['price', 'total_price', 'car_id', 'client_id', 'employee_id']:
                    input_widget.setText("{:.0f}".format(float(value)) if value is not None else "")
                else:
                    input_widget.setText(str(value) if value is not None else "")
            elif field_name == 'sale_date':
                input_widget.setCalendarPopup(True)
                input_widget.setDate(QDate.fromString(str(value), Qt.ISODate) if value else QDate.currentDate())
            elif field_name == 'payment_method':
                input_widget.addItems(["Наличные", "Банковский перевод", "Рассрочка"])
                input_widget.setCurrentText(str(value) if value else "Наличные")

            self.inputs[field_name] = input_widget
            form_layout.addRow(f"{field['label']}:", input_widget)

        layout.addLayout(form_layout)

        # Кнопки
        button_box = QHBoxLayout()
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_changes)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        layout.addLayout(button_box)

        self.setLayout(layout)

    def save_changes(self):
        # Собираем значения из полей
        values = {}
        for field in self.fields[1:]:  # Пропускаем ID
            field_name = field['name']
            input_widget = self.inputs[field_name]
            if field_name == 'sale_date':
                values[field_name] = input_widget.date().toString(Qt.ISODate)
            elif field_name == 'payment_method':
                values[field_name] = input_widget.currentText()
            else:
                values[field_name] = input_widget.text()

        # Проверяем обязательные поля
        for field in self.fields[1:]:
            if field.get('required') and not values[field['name']]:
                QMessageBox.warning(self, "Ошибка", f"Поле '{field['label']}' обязательно для заполнения!")
                return

        # Формируем запрос на обновление
        query = QSqlQuery(self.connection)
        set_clause = ", ".join([f"{field['name']} = ?" for field in self.fields[1:]])
        query.prepare(f"""
            UPDATE {self.table_name}
            SET {set_clause}
            WHERE {self.fields[0]['name']} = ?
        """)
        for field in self.fields[1:]:
            query.addBindValue(values[field['name']])
        query.addBindValue(self.record_id)

        if query.exec_():
            self.accept()
            QMessageBox.information(self, "Успех", "Запись успешно обновлена!")
        else:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить запись: {query.lastError().text()}")

class BaseForm(QWidget):
    def __init__(self, connection, table_name, fields, headers, parent=None):
        super().__init__(parent)
        self.connection = connection
        self.table_name = table_name
        self.fields = fields
        self.headers = headers
        self.setStyleSheet(STYLESHEET)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Таблица
        self.table_view = QTableView()
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.table_view)

        # Модель данных
        self.model = QSqlTableModel(self, self.connection)
        self.model.setTable(self.table_name)
        
        # Устанавливаем заголовки для всех столбцов таблицы
        for idx, header in enumerate(self.headers):
            self.model.setHeaderData(idx, Qt.Horizontal, header)
        
        self.model.select()

        #форматирования чисел
        delegate = NumberFormatDelegate(self.table_view)
        self.table_view.setItemDelegate(delegate)

        self.table_view.setModel(self.model)
        self.table_view.resizeColumnsToContents()

        # Форма добавления
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignLeft)
        form_layout.setHorizontalSpacing(10)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)

        self.inputs = {}
        for field in self.fields[1:]:  # Пропускаем ID в форме добавления
            field_name = field['name']
            input_widget = field['widget']()
            self.inputs[field_name] = input_widget
            form_layout.addRow(f"{field['label']}:", input_widget)

        layout.addLayout(form_layout)

        # Кнопки управления
        button_layout = QHBoxLayout()
        self.add_button = QPushButton(f"Добавить в {self.table_name}")
        self.add_button.clicked.connect(self.add_record)
        self.edit_button = QPushButton(f"Редактировать в {self.table_name}")
        self.edit_button.clicked.connect(self.edit_record)
        self.delete_button = QPushButton(f"Удалить из {self.table_name}")
        self.delete_button.clicked.connect(self.delete_record)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_record(self):
        # Собираем значения из полей
        values = {}
        for field in self.fields[1:]:  # Пропускаем ID
            field_name = field['name']
            input_widget = self.inputs[field_name]
            if field_name == 'sale_date':
                values[field_name] = input_widget.date().toString(Qt.ISODate)
            elif field_name == 'payment_method':
                values[field_name] = input_widget.currentText()
            else:
                values[field_name] = input_widget.text()

        # Проверяем обязательные поля
        for field in self.fields[1:]:
            if field.get('required') and not values[field['name']]:
                QMessageBox.warning(self, "Ошибка", f"Поле '{field['label']}' обязательно для заполнения!")
                return

        # Формируем запрос на добавление
        query = QSqlQuery(self.connection)
        placeholders = ", ".join(["?" for _ in self.fields[1:]])
        columns = ", ".join([field['name'] for field in self.fields[1:]])
        query.prepare(f"""
            INSERT INTO {self.table_name} ({columns})
            VALUES ({placeholders})
        """)
        for field in self.fields[1:]:
            field_name = field['name']
            if field_name in ['car_id', 'client_id', 'employee_id', 'total_price', 'price', 'year', 'in_stock', 'count', 'model_id', 'manufacturer_id']:
                query.addBindValue(int(values[field_name]) if values[field_name] else 0)
            else:
                query.addBindValue(values[field_name])

        if query.exec_():
            self.model.select()
            self.clear_inputs()
            QMessageBox.information(self, "Успех", "Запись успешно добавлена!")
        else:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить запись: {query.lastError().text()}")

    def edit_record(self):
        selected_row = self.table_view.currentIndex().row()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования!")
            return

        record = self.model.record(selected_row)
        record_id = record.value(self.fields[0]['name'])
        print(f"Editing record with ID: {record_id}")  # Отладка

        dialog = BaseEditDialog(record_id, self.table_name, self.fields, self.connection, self)
        if dialog.exec_() == QDialog.Accepted:
            self.model.select()

    def delete_record(self):
        selected_row = self.table_view.currentIndex().row()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления!")
            return

        record = self.model.record(selected_row)
        record_id = record.value(self.fields[0]['name'])
        print(f"Deleting record with ID: {record_id}")  # Отладка

        reply = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Вы действительно хотите удалить запись с ID {record_id}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            query = QSqlQuery(self.connection)
            query.prepare(f"DELETE FROM {self.table_name} WHERE {self.fields[0]['name']} = ?")
            query.addBindValue(record_id)
            print(f"Executing DELETE query: DELETE FROM {self.table_name} WHERE {self.fields[0]['name']} = {record_id}")

            if query.exec_():
                self.model.select()
                QMessageBox.information(self, "Успех", "Запись успешно удалена!")
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить запись: {query.lastError().text()}")

    def clear_inputs(self):
        for field in self.fields[1:]:
            input_widget = self.inputs[field['name']]
            if field['name'] == 'sale_date':
                input_widget.setDate(QDate.currentDate())
            elif field['name'] == 'payment_method':
                input_widget.setCurrentIndex(0)
            else:
                input_widget.clear()