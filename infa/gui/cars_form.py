from PyQt5.QtWidgets import QLineEdit
from base_form import BaseForm

class CarsForm(BaseForm):
    def __init__(self, connection, parent=None):
        # Определяем параметры формы
        table_name = "Cars"
        fields = [
            {'name': 'car_id', 'label': 'ID', 'widget': QLineEdit, 'required': False},  # ID автогенерируется
            {'name': 'model_id', 'label': 'Модель ID', 'widget': QLineEdit, 'required': True},
            {'name': 'vin_code', 'label': 'VIN', 'widget': QLineEdit, 'required': True},
            {'name': 'color', 'label': 'Цвет', 'widget': QLineEdit, 'required': False},
            {'name': 'year', 'label': 'Год', 'widget': QLineEdit, 'required': False},
            {'name': 'price', 'label': 'Цена', 'widget': QLineEdit, 'required': False},
            {'name': 'in_stock', 'label': 'В наличии (1/0)', 'widget': QLineEdit, 'required': False},
        ]
        headers = ["ID", "Модель ID", "VIN", "Цвет", "Год", "Цена", "В наличии"]

        super().__init__(connection, table_name, fields, headers, parent)

    def clear_inputs(self):
        super().clear_inputs()