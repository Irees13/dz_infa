-- SQLite
-- Производители
CREATE TABLE IF NOT EXISTS Manufacturers (
    manufacturer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Модели автомобилей
CREATE TABLE IF NOT EXISTS CarModels (
    model_id INTEGER PRIMARY KEY,
    manufacturer_id INTEGER,
    name TEXT NOT NULL,
    body_type TEXT,
    FOREIGN KEY(manufacturer_id) REFERENCES Manufacturers(manufacturer_id)
);

-- Автомобили
CREATE TABLE IF NOT EXISTS Cars (
    car_id INTEGER PRIMARY KEY,
    model_id INTEGER,
    vin_code TEXT UNIQUE NOT NULL,
    color TEXT,
    year INTEGER,
    price REAL,
    in_stock BOOLEAN DEFAULT TRUE,
    FOREIGN KEY(model_id) REFERENCES CarModels(model_id)
);


-- Клиенты
CREATE TABLE IF NOT EXISTS Clients (
    client_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT
);

-- Сотрудники
CREATE TABLE IF NOT EXISTS Employees (
    employee_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    position TEXT,
    phone TEXT,
    hire_date DATE
);


-- Продажи
CREATE TABLE IF NOT EXISTS Sales (
    sale_id INTEGER PRIMARY KEY,
    car_id INTEGER,
    client_id INTEGER,
    employee_id INTEGER,
    sale_date DATE,
    total_price REAL,
    payment_method TEXT,
    FOREIGN KEY(car_id) REFERENCES Cars(car_id),
    FOREIGN KEY(client_id) REFERENCES Clients(client_id),
    FOREIGN KEY(employee_id) REFERENCES Employees(employee_id)
); 


-- Поставки
CREATE TABLE IF NOT EXISTS Supplies (
    supply_id INTEGER PRIMARY KEY,
    manufacturer_id INTEGER,
    count INTEGER,
    supply_date DATE,
    FOREIGN KEY(manufacturer_id) REFERENCES Manufacturers(manufacturer_id)
);
