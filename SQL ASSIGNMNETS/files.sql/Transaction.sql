-- This will work 100%
START TRANSACTION;
INSERT INTO Orders (customer_id, table_id, staff_id, total_amount, order_status) 
VALUES (1, 1, 2, 35.00, 'Pending');
SET @test_id = LAST_INSERT_ID();
INSERT INTO OrderItems (order_id, item_id, quantity, price) VALUES (@test_id, 1, 2, 16.99);
COMMIT;
SELECT CONCAT('Order ', @test_id, ' created successfully!') AS Message;
DELETE FROM OrderItems WHERE order_id = @test_id;
DELETE FROM Orders WHERE order_id = @test_id;