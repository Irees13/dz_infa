from PyQt5.QtWidgets import QLineEdit
from base_form import BaseForm

class EmployeesForm(BaseForm):
    def __init__(self, connection, parent=None):
        # Определяем параметры формы
        table_name = "Employees"
        fields = [
            {'name': 'employee_id', 'label': 'ID', 'widget': QLineEdit, 'required': False},  # ID автогенерируется
            {'name': 'full_name', 'label': 'ФИО', 'widget': QLineEdit, 'required': True},
            {'name': 'position', 'label': 'Должность', 'widget': QLineEdit, 'required': False},
            {'name': 'phone', 'label': 'Телефон', 'widget': QLineEdit, 'required': False},
            {'name': 'hire_date', 'label': 'Дата приёма', 'widget': QLineEdit, 'required': False},
        ]
        headers = ["ID", "ФИО", "Должность", "Телефон", "Дата приёма"]

        super().__init__(connection, table_name, fields, headers, parent)

    def clear_inputs(self):
        super().clear_inputs()