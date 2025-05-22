# styles.py
STYLESHEET = """
/* Базовый стиль для всех виджетов */
QWidget {
    font-family: Arial, sans-serif;
    font-size: 14px;
    background-color: #f5f5f5;
}

/* Стиль для меток */
QLabel {
    font-size: 16px;
    font-weight: bold;
    color: #333;
    margin: 10px;
}

/* Стиль для кнопок */
QPushButton {
    background-color: #4CAF50;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    margin: 5px;
    min-width: 200px;
}
QPushButton:hover {
    background-color: #45a049;
}
QPushButton:pressed {
    background-color: #3d8b40;
}

/* Стиль для меню */
QMenuBar {
    background-color: #333;
    color: white;
}
QMenuBar::item {
    background-color: #333;
    color: white;
    padding: 5px 10px;
}
QMenuBar::item:selected {
    background-color: #555;
}

/* Стиль для полей ввода */
QLineEdit {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 6px;
    min-width: 200px;
    background-color: #fff;
}
QLineEdit:focus {
    border: 1px solid #4CAF50;
}

/* Стиль для таблицы */
QTableView {
    border: 1px solid #ccc;
    gridline-color: #ccc;
    background-color: #fff;
    selection-background-color: #e0e0e0;
}
QTableView::item {
    padding: 5px;
}
QHeaderView::section {
    background-color: #e0e0e0;
    border: 1px solid #ccc;
    padding: 5px;
}

/* Стиль для выпадающего списка */
QComboBox {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 6px;
    min-width: 220px;
    background-color: #fff;
}
QComboBox::drop-down {
    width: 20px;
}
QComboBox::down-arrow {
    width: 10px;
    height: 10px;
}
QComboBox:focus {
    border: 1px solid #4CAF50;
}

/* Стиль для поля даты */
QDateEdit {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 6px;
    min-width: 200px;
    background-color: #fff;
}
QDateEdit:focus {
    border: 1px solid #4CAF50;
}

/* Стиль для меток в QFormLayout */
QFormLayout QLabel {
    min-width: 120px;
    font-size: 14px;
    color: #333;
}

/* Стиль для боковой панели */
QWidget#sidebar {
    background-color: #e0e0e0;
    border-right: 1px solid #ccc;
}

/* Стиль для QStackedWidget */
QStackedWidget {
    background-color: #ffffff;
    border: 1px solid #ccc;
}

/* Стиль для QTextEdit в ReportsForm */
QTextEdit {
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #fff;
    padding: 5px;
}
"""