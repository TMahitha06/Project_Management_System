-- ==========================================
-- EXPLAIN QUERIES (Query Optimization)
-- ==========================================

-- 1. EXPLAIN simple SELECT with WHERE
EXPLAIN SELECT * FROM MenuItems WHERE price > 10;

-- 2. EXPLAIN with category filter
EXPLAIN SELECT item_name, price FROM MenuItems WHERE category = 'Main Course';

-- 3. EXPLAIN with JOIN
EXPLAIN SELECT o.order_id, c.first_name, o.total_amount
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id;

-- 4. EXPLAIN with GROUP BY
EXPLAIN SELECT category, COUNT(*) FROM MenuItems GROUP BY category;

-- 5. EXPLAIN with subquery
EXPLAIN SELECT item_name FROM MenuItems 
WHERE price > (SELECT AVG(price) FROM MenuItems);

-- 6. EXPLAIN with ORDER BY
EXPLAIN SELECT * FROM Orders ORDER BY total_amount DESC;

-- 7. EXPLAIN with multiple JOINs
EXPLAIN SELECT o.order_id, c.first_name, m.item_name, oi.quantity
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN MenuItems m ON oi.item_id = m.item_id;