-- ==========================================
-- INSERT DATA
-- ==========================================

-- Menu Items
INSERT INTO MenuItems (item_name, price, category) VALUES
('Butter Chicken', 16.99, 'Main Course'),
('Paneer Tikka', 12.99, 'Appetizer'),
('Masala Dosa', 9.99, 'Main Course'),
('Biryani', 14.99, 'Main Course'),
('Gulab Jamun', 5.99, 'Dessert'),
('Mango Lassi', 3.99, 'Beverage'),
('Garlic Naan', 3.99, 'Side Dish'),
('Chicken 65', 11.99, 'Appetizer');

-- Staff
INSERT INTO Staff (first_name, last_name, role) VALUES
('Amit', 'Sharma', 'Manager'),
('Priya', 'Patel', 'Waiter'),
('Rajesh', 'Kumar', 'Chef'),
('Neha', 'Singh', 'Waiter'),
('Vikram', 'Reddy', 'Chef');

-- Tables
INSERT INTO `Tables` (table_number, capacity) VALUES
(1, 2),
(2, 4),
(3, 6),
(4, 8),
(5, 2),
(6, 4);

-- Customers
INSERT INTO Customers (first_name, last_name, phone, email) VALUES
('Arjun', 'Mehta', '98765-1001', 'arjun@email.com'),
('Divya', 'Sharma', '98765-1002', 'divya@email.com'),
('Rohan', 'Verma', '98765-1003', 'rohan@email.com'),
('Kavya', 'Nair', '98765-1004', 'kavya@email.com'),
('Siddharth', 'Joshi', '98765-1005', 'sid@email.com');

-- Orders
INSERT INTO Orders (customer_id, table_id, staff_id, total_amount, order_status) VALUES
(1, 1, 2, 24.97, 'Completed'),
(2, 2, 4, 29.97, 'Completed'),
(NULL, 5, 2, 20.98, 'Preparing'),
(4, 3, 4, 21.98, 'Served'),
(5, 4, 2, 49.94, 'Pending');

-- Order Items
INSERT INTO OrderItems (order_id, item_id, quantity, price) VALUES
(1, 1, 1, 16.99),
(1, 6, 2, 3.99),
(2, 2, 2, 12.99),
(2, 7, 1, 3.99),
(3, 4, 1, 14.99),
(3, 5, 1, 5.99),
(4, 8, 1, 11.99),
(4, 3, 1, 9.99),
(5, 1, 2, 16.99),
(5, 6, 4, 3.99);

-- Reservations
INSERT INTO Reservations (customer_id, table_id, reservation_date, guests) VALUES
(1, 1, '2026-04-10', 2),
(3, 3, '2026-04-10', 4),
(4, 4, '2026-04-11', 6),
(2, 2, '2026-04-09', 3);