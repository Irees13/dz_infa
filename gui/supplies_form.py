from PyQt5.QtWidgets import QLineEdit
from base_form import BaseForm

class SuppliesForm(BaseForm):
    def __init__(self, connection, parent=None):
        # Определяем параметры формы
        table_name = "Supplies"
        fields = [
            {'name': 'supply_id', 'label': 'ID', 'widget': QLineEdit, 'required': False},  # ID автогенерируется
            {'name': 'manufacturer_id', 'label': 'ID производителя', 'widget': QLineEdit, 'required': True},
            {'name': 'count', 'label': 'Количество', 'widget': QLineEdit, 'required': True},
            {'name': 'supply_date', 'label': 'Дата поставки', 'widget': QLineEdit, 'required': False},
        ]
        headers = ["ID", "ID производителя", "Количество", "Дата поставки"]

        super().__init__(connection, table_name, fields, headers, parent)

    def clear_inputs(self):
        super().clear_inputs()