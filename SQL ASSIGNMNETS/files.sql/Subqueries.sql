-- ==========================================
-- SUBQUERY QUERIES (FIXED)
-- ==========================================

-- 1. Items priced above average
SELECT item_name, price
FROM MenuItems
WHERE price > (SELECT AVG(price) FROM MenuItems);

-- 2. Customers who placed orders
SELECT first_name, last_name
FROM Customers
WHERE customer_id IN (SELECT DISTINCT customer_id FROM Orders WHERE customer_id IS NOT NULL);

-- 3. Items that have been ordered
SELECT item_name, price
FROM MenuItems
WHERE item_id IN (SELECT DISTINCT item_id FROM OrderItems);

-- 4. Orders above average amount
SELECT order_id, total_amount
FROM Orders
WHERE total_amount > (SELECT AVG(total_amount) FROM Orders);

-- 5. Each item's total quantity ordered (FIXED - shows 0 instead of NULL)
SELECT 
    item_name,
    COALESCE((SELECT SUM(quantity) FROM OrderItems WHERE item_id = m.item_id), 0) AS total_ordered
FROM MenuItems m
ORDER BY total_ordered DESC;

-- 6. Customers who never placed orders
SELECT first_name, last_name
FROM Customers c
WHERE NOT EXISTS (SELECT 1 FROM Orders o WHERE o.customer_id = c.customer_id);