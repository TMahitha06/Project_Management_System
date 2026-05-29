-- Disable safe mode
SET SQL_SAFE_UPDATES = 0;

-- Disable foreign key checks
SET FOREIGN_KEY_CHECKS = 0;

-- Now delete
SET @customer_id = 5;
DELETE FROM OrderItems WHERE order_id IN (SELECT order_id FROM (SELECT order_id FROM Orders WHERE customer_id = @customer_id) AS temp);
DELETE FROM Orders WHERE customer_id = @customer_id;
DELETE FROM Customers WHERE customer_id = @customer_id;

-- Re-enable
SET FOREIGN_KEY_CHECKS = 1;
SET SQL_SAFE_UPDATES = 1;