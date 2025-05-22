from PyQt5.QtWidgets import QLineEdit
from base_form import BaseForm

class ClientsForm(BaseForm):
    def __init__(self, connection, parent=None):
        # Определяем параметры формы
        table_name = "Clients"
        fields = [
            {'name': 'client_id', 'label': 'ID', 'widget': QLineEdit, 'required': False},  # ID автогенерируется
            {'name': 'full_name', 'label': 'ФИО', 'widget': QLineEdit, 'required': True},
            {'name': 'phone', 'label': 'Телефон', 'widget': QLineEdit, 'required': False},
            {'name': 'email', 'label': 'Email', 'widget': QLineEdit, 'required': False},
            {'name': 'address', 'label': 'Адрес', 'widget': QLineEdit, 'required': False},
        ]
        headers = ["ID", "ФИО", "Телефон", "Email", "Адрес"]

        super().__init__(connection, table_name, fields, headers, parent)

    def clear_inputs(self):
        super().clear_inputs()