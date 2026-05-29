-- ==========================================
-- INDEXES for Simple Restaurant Database
-- ==========================================

-- MenuItems indexes
CREATE INDEX idx_menu_name ON MenuItems(item_name);
CREATE INDEX idx_menu_category ON MenuItems(category);
CREATE INDEX idx_menu_price ON MenuItems(price);

-- Customers indexes
CREATE INDEX idx_customer_name ON Customers(first_name, last_name);
CREATE INDEX idx_customer_phone ON Customers(phone);
CREATE INDEX idx_customer_email ON Customers(email);

-- Staff indexes
CREATE INDEX idx_staff_name ON Staff(first_name, last_name);
CREATE INDEX idx_staff_role ON Staff(role);

-- Orders indexes
CREATE INDEX idx_order_date ON Orders(order_date);
CREATE INDEX idx_order_status ON Orders(order_status);
CREATE INDEX idx_order_customer ON Orders(customer_id);
CREATE INDEX idx_order_staff ON Orders(staff_id);
CREATE INDEX idx_order_table ON Orders(table_id);

-- OrderItems indexes
CREATE INDEX idx_orderitems_order ON OrderItems(order_id);
CREATE INDEX idx_orderitems_item ON OrderItems(item_id);

-- Tables indexes
CREATE INDEX idx_table_number ON `Tables`(table_number);
CREATE INDEX idx_table_capacity ON `Tables`(capacity);

-- Reservations indexes
CREATE INDEX idx_reservation_date ON Reservations(reservation_date);
CREATE INDEX idx_reservation_customer ON Reservations(customer_id);
CREATE INDEX idx_reservation_table ON Reservations(table_id);