-- ==========================================
-- SIMPLE GROUP BY & AGGREGATE QUERIES
-- ==========================================

-- 1. Count items by category
SELECT category, COUNT(*) AS total_items
FROM MenuItems
GROUP BY category;

-- 2. Total spent by each customer
SELECT c.first_name, SUM(o.total_amount) AS total_spent
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;

-- 3. Average price by category
SELECT category, AVG(price) AS average_price
FROM MenuItems
GROUP BY category;

-- 4. Customers who spent more than 30 (HAVING)
SELECT c.first_name, SUM(o.total_amount) AS total_spent
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING total_spent > 30;

-- 5. Overall stats
SELECT 
    COUNT(*) AS total_orders,
    SUM(total_amount) AS revenue,
    AVG(total_amount) AS avg_order
FROM Orders;