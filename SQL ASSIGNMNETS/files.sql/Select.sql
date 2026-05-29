-- ==========================================
-- SELECT QUERIES TO TEST
-- ==========================================

-- See all menu items
SELECT * FROM MenuItems;

-- See all customers
SELECT * FROM Customers;

-- See all orders with customer names
SELECT o.order_id, c.first_name, c.last_name, o.total_amount, o.order_status
FROM Orders o
LEFT JOIN Customers c ON o.customer_id = c.customer_id;

-- See order details with item names
SELECT o.order_id, c.first_name, m.item_name, oi.quantity, oi.price
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN MenuItems m ON oi.item_id = m.item_id;

-- Count items by category
SELECT category, COUNT(*) as total FROM MenuItems GROUP BY category;