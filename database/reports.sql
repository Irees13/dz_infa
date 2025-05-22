-- database/reports.sql
-- SQL-запросы для генерации отчетов в базе данных автосалона

-- 1. Общая сумма продаж по датам
SELECT strftime('%Y-%m-%d', sale_date) AS sale_date, 
       CAST(SUM(total_price) AS DECIMAL(15, 2)) AS total_sales
FROM Sales
WHERE sale_date BETWEEN :start_date AND :end_date
GROUP BY sale_date
ORDER BY sale_date;

-- 2. Самые активные клиенты
SELECT 
    c.client_id,
    c.full_name,
    COUNT(s.sale_id) AS purchase_count,
    CAST(SUM(s.total_price) AS DECIMAL(15, 2)) AS total_spent
FROM Sales s
JOIN Clients c ON s.client_id = c.client_id
WHERE s.sale_date BETWEEN :start_date AND :end_date
GROUP BY c.client_id, c.full_name
ORDER BY purchase_count DESC
LIMIT 5;

-- 3. Топ проданных автомобилей
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
WHERE s.sale_date BETWEEN :start_date AND :end_date
GROUP BY c.car_id, cm.name, m.name
ORDER BY sales_count DESC
LIMIT 5;

-- 4. Количество и детали поставок
SELECT 
    s.supply_id,
    m.name AS manufacturer_name,
    s.count,
    s.supply_date
FROM Supplies s
JOIN Manufacturers m ON s.manufacturer_id = m.manufacturer_id
WHERE s.supply_date BETWEEN :start_date AND :end_date
ORDER BY s.supply_date;

-- 5. Средняя цена автомобиля по марке
SELECT 
    m.name AS manufacturer_name,
    CAST(AVG(c.price) AS DECIMAL(15, 2)) AS avg_price
FROM Cars c
JOIN CarModels cm ON c.model_id = cm.model_id
JOIN Manufacturers m ON cm.manufacturer_id = m.manufacturer_id
GROUP BY m.manufacturer_id, m.name
ORDER BY avg_price DESC;

-- 6. Статистика по типам оплаты
SELECT 
    s.payment_method,
    COUNT(s.sale_id) AS transaction_count,
    CAST(SUM(s.total_price) AS DECIMAL(15, 2)) AS total_amount
FROM Sales s
WHERE s.sale_date BETWEEN :start_date AND :end_date
GROUP BY s.payment_method
ORDER BY transaction_count DESC;

-- 7. Автомобили в наличии
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
ORDER BY c.car_id;

-- 8. Эффективность сотрудников
SELECT 
    e.employee_id,
    e.full_name,
    e.position,
    COUNT(s.sale_id) AS sales_count,
    CAST(SUM(s.total_price) AS DECIMAL(15, 2)) AS total_sales
FROM Employees e
LEFT JOIN Sales s ON e.employee_id = s.employee_id
WHERE s.sale_date BETWEEN :start_date AND :end_date OR s.sale_date IS NULL
GROUP BY e.employee_id, e.full_name, e.position
ORDER BY total_sales DESC;