-- ==========================================
-- JOIN QUERIES
-- ==========================================

-- 1. INNER JOIN: Orders with customer details
SELECT o.order_id, c.first_name, c.last_name, o.total_amount, o.order_status
FROM Orders o
INNER JOIN Customers c ON o.customer_id = c.customer_id;

-- 2. LEFT JOIN: All customers and their orders (even customers with no orders)
SELECT c.first_name, c.last_name, o.order_id, o.total_amount, o.order_status
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id;

-- 3. RIGHT JOIN: All orders and their customers (even orders with no customer)
SELECT o.order_id, c.first_name, c.last_name, o.total_amount
FROM Orders o
RIGHT JOIN Customers c ON o.customer_id = c.customer_id;

-- 4. Multiple JOINs: Order details with customer and item information
SELECT o.order_id, c.first_name, m.item_name, oi.quantity, oi.price
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN MenuItems m ON oi.item_id = m.item_id;

-- 5. JOIN with WHERE clause: Find completed orders with customer names
SELECT o.order_id, c.first_name, c.last_name, o.total_amount
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'Completed';

-- 6. JOIN with ORDER BY: Orders sorted by total amount
SELECT o.order_id, c.first_name, o.total_amount
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
ORDER BY o.total_amount DESC;

-- 7. JOIN with GROUP BY: Total spent by each customer
SELECT c.first_name, c.last_name, SUM(o.total_amount) AS total_spent
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;

-- 8. LEFT JOIN with COUNT: Number of orders per customer
SELECT c.first_name, c.last_name, COUNT(o.order_id) AS order_count
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;

-- 9. Self JOIN: Not applicable in simple schema (no self-reference needed)

-- 10. JOIN across 4 tables: Complete order details
SELECT o.order_id, c.first_name, s.first_name AS waiter, t.table_number, m.item_name, oi.quantity
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Staff s ON o.staff_id = s.staff_id
JOIN `Tables` t ON o.table_id = t.table_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN MenuItems m ON oi.item_id = m.item_id
LIMIT 10;