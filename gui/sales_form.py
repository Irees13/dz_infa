from PyQt5.QtWidgets import QLineEdit, QDateEdit, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIntValidator
from base_form import BaseForm, QSqlQuery

class SalesForm(BaseForm):
    def __init__(self, connection, parent=None):
        # Определяем параметры формы
        table_name = "Sales"
        fields = [
            {'name': 'sale_id', 'label': 'ID', 'widget': QLineEdit, 'required': False},
            {'name': 'car_id', 'label': 'ID авто', 'widget': QLineEdit, 'required': True},
            {'name': 'client_id', 'label': 'ID клиента', 'widget': QLineEdit, 'required': True},
            {'name': 'employee_id', 'label': 'ID сотрудника', 'widget': QLineEdit, 'required': True},
            {'name': 'sale_date', 'label': 'Дата продажи', 'widget': QDateEdit, 'required': False},
            {'name': 'total_price', 'label': 'Общая сумма', 'widget': QLineEdit, 'required': False},
            {'name': 'payment_method', 'label': 'Способ оплаты', 'widget': QComboBox, 'required': False},
        ]
        headers = ["ID", "ID авто", "ID клиента", "ID сотрудника", "Дата продажи", "Общая сумма", "Способ оплаты"]

        super().__init__(connection, table_name, fields, headers, parent)

        # Настраиваем QDateEdit
        self.inputs['sale_date'].setCalendarPopup(True)
        self.inputs['sale_date'].setDate(QDate.currentDate())

        # Настраиваем QComboBox
        self.inputs['payment_method'].addItems(["Наличные", "Банковский перевод", "Рассрочка"])

        # Добавляем валидатор для total_price
        self.inputs['total_price'].setValidator(QIntValidator(0, 999999999, self))

        # Добавляем валидатор для car_id, client_id, employee_id
        self.inputs['car_id'].setValidator(QIntValidator(1, 999999, self))
        self.inputs['client_id'].setValidator(QIntValidator(1, 999999, self))
        self.inputs['employee_id'].setValidator(QIntValidator(1, 999999, self))

    def add_record(self):
        # Собираем значения из полей
        values = {}
        for field in self.fields[1:]:  # Пропускаем sale_id
            field_name = field['name']
            if field_name == 'sale_date':
                values[field_name] = self.inputs[field_name].date().toString(Qt.ISODate)
            elif field_name == 'payment_method':
                values[field_name] = self.inputs[field_name].currentText()
            else:
                values[field_name] = self.inputs[field_name].text()

        # Проверяем обязательные поля
        for field in self.fields[1:]:
            if field.get('required') and not values[field['name']]:
                QMessageBox.warning(self, "Ошибка", f"Поле '{field['label']}' обязательно для заполнения!")
                return

        # Проверяем, что car_id, client_id, employee_id — это числа
        for field_name in ['car_id', 'client_id', 'employee_id']:
            if not values[field_name].isdigit():
                QMessageBox.warning(self, "Ошибка", f"Поле '{field['label']}' должно быть числом!")
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
            if field_name in ['car_id', 'client_id', 'employee_id', 'total_price']:
                query.addBindValue(int(values[field_name]) if values[field_name] else 0)
            else:
                query.addBindValue(values[field_name])
            print(f"Binding {field_name} with value: {values[field_name]}")  # Отладка

        if query.exec_():
            self.model.select()
            self.clear_inputs()
            QMessageBox.information(self, "Успех", "Запись успешно добавлена!")
        else:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить запись: {query.lastError().text()}")

    def clear_inputs(self):
        super().clear_inputs()