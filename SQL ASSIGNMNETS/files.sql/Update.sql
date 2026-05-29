-- ==========================================
-- UPDATE STATEMENTS
-- ==========================================

-- ==========================================
-- MENUITEMS UPDATES
-- ==========================================

-- Update 1: Change price of Butter Chicken
UPDATE MenuItems SET price = 18.99 WHERE item_id = 1;

-- Update 2: Change price of Paneer Tikka
UPDATE MenuItems SET price = 13.99 WHERE item_id = 2;

-- Update 3: Increase all Main Course prices by 10%
UPDATE MenuItems SET price = ROUND(price * 1.10, 2) WHERE category = 'Main Course';

-- Update 4: Change category of Chicken 65 to 'Starters'
UPDATE MenuItems SET category = 'Starters' WHERE item_id = 8;

-- ==========================================
-- CUSTOMERS UPDATES
-- ==========================================

-- Update 1: Update phone number for Arjun
UPDATE Customers SET phone = '99888-1001' WHERE customer_id = 1;

-- Update 2: Update email for Divya
UPDATE Customers SET email = 'divya.new@email.com' WHERE customer_id = 2;

-- Update 3: Update phone number for Rohan
UPDATE Customers SET phone = '99999-1003' WHERE customer_id = 3;

-- Update 4: Update first name of Siddharth
UPDATE Customers SET first_name = 'Sid' WHERE customer_id = 5;

-- ==========================================
-- STAFF UPDATES
-- ==========================================

-- Update 1: Change role of Priya
UPDATE Staff SET role = 'Senior Waiter' WHERE staff_id = 2;

-- Update 2: Change role of Vikram
UPDATE Staff SET role = 'Head Chef' WHERE staff_id = 5;

-- ==========================================
-- TABLES UPDATES
-- ==========================================

-- Update 1: Increase capacity of table 5
UPDATE `Tables` SET capacity = 4 WHERE table_number = 5;

-- Update 2: Update table number 6 capacity
UPDATE `Tables` SET capacity = 6 WHERE table_number = 6;

-- ==========================================
-- ORDERS UPDATES
-- ==========================================

-- Update 1: Mark order as completed
UPDATE Orders SET order_status = 'Completed' WHERE order_id = 5;

-- Update 2: Update total amount for order 3
UPDATE Orders SET total_amount = 25.98 WHERE order_id = 3;

-- Update 3: Change order status for Preparing orders
UPDATE Orders SET order_status = 'Ready' WHERE order_status = 'Preparing';

-- ==========================================
-- ORDERITEMS UPDATES
-- ==========================================

-- Update 1: Update quantity for order item
UPDATE OrderItems SET quantity = 3, price = price WHERE order_item_id = 5;

-- Update 2: Update price for order item
UPDATE OrderItems SET price = 17.99 WHERE order_item_id = 1;

-- ==========================================
-- RESERVATIONS UPDATES
-- ==========================================

-- Update 1: Update number of guests
UPDATE Reservations SET guests = 4 WHERE reservation_id = 1;

-- Update 2: Update reservation date
UPDATE Reservations SET reservation_date = '2026-04-15' WHERE reservation_id = 3;