# Create DB
CREATE DATABASE road_runner;
USE road_runner;


# Create and fill cargo table

CREATE TABLE cargo_types (
    id CHAR(4) NOT NULL PRIMARY KEY,
    cargo_name VARCHAR(255) NOT NULL,
    cargo_type VARCHAR(255) NOT NULL
);

INSERT INTO cargo_types (id, cargo_name, cargo_type) VALUES
('0000', 'General Merchandise', 'Dry Goods'),
('0001', 'Perishable Goods', 'Temperature-Controlled'),
('0002', 'Refrigerated Foods', 'Temperature-Controlled'),
('0003', 'Livestock', 'Live Cargo'),
('0004', 'Hazardous Materials', 'Dangerous Goods'),
('0005', 'Automotive Parts', 'Industrial Goods'),
('0006', 'Construction Materials', 'Building Supplies'),
('0007', 'Heavy Machinery', 'Industrial Equipment'),
('0008', 'Electronics', 'Fragile Goods'),
('0009', 'Medical Supplies', 'Healthcare Products'),
('0010', 'Chemicals', 'Hazardous Materials'),
('0011', 'Textiles & Apparel', 'Consumer Goods'),
('0012', 'Furniture', 'Consumer Goods'),
('0013', 'Household Goods', 'Consumer Goods'),
('0014', 'Beverages', 'Temperature-Controlled'),
('0015', 'Frozen Foods', 'Temperature-Controlled'),
('0016', 'Agricultural Produce', 'Fresh Produce'),
('0017', 'Raw Materials', 'Industrial Goods'),
('0018', 'Petroleum Products', 'Hazardous Materials'),
('0019', 'Dairy Products', 'Temperature-Controlled'),
('0020', 'Tobacco Products', 'Consumer Goods'),
('0021', 'Paper & Printing Materials', 'Dry Goods'),
('0022', 'E-commerce Parcels', 'Small Package Freight'),
('0023', 'Bulk Liquids', 'Liquid Cargo'),
('0024', 'Bulk Dry Goods', 'Dry Bulk Cargo'),
('0025', 'Military Equipment', 'Special Cargo'),
('0026', 'Pharmaceuticals', 'Healthcare Products'),
('0027', 'Livestock Feed', 'Agricultural Goods'),
('0028', 'Logging & Timber', 'Raw Materials'),
('0029', 'Waste & Recycling Materials', 'Specialized Cargo');



# Create and fill Truck table

CREATE TABLE trucks (
    id CHAR(4) NOT NULL PRIMARY KEY,
    brand varchar(255),
    name varchar(255),
    fuel_tank int,
    liters_per_100km int,
    max_weight int,
    horsepower int
);


INSERT INTO trucks (id, brand, name, fuel_tank, liters_per_100km, max_weight, horsepower)
VALUES
    ('0000', 'Scania', 'R2016', 350, 30, 25500, 730),
    ('0001', 'Volvo', 'FH16 2016', 300, 25, 26000, 750),
    ('0002', 'Mercedes', 'Actrod', 325, 35, 24000, 625),
    ('0003', 'MAN', 'TGX EURO 6', 275, 28, 24500, 640),
    ('0004', 'Renault', 'T', 250, 32, 23000, 520);


# Create owned trucks table

CREATE TABLE owned_trucks (
    id CHAR(4) NOT NULL PRIMARY KEY,
    truck_id CHAR(4),
    Current_Driver varchar(255) NULL
);


CREATE TABLE drivers (
    id CHAR(4) NOT NULL PRIMARY KEY,
    name varchar(255),
    free_drive_time INT,
    available_for_next_job DATE NULL
);

CREATE TABLE employees (
    id int NOT NULL PRIMARY KEY,
    user_name varchar(255),
    password varchar(255),
    role varchar(50)
);

INSERT INTO employees (id, user_name, password, role)
VALUES (1, "lorenzo@roadrunner.com", "$2a$12$wgDQurvFlCAca40IgHUguOmmoK0oJTjvynU1.ZSk/PnG01wsf8wVK", "driver");

CREATE TABLE routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    from_location VARCHAR(255) NOT NULL,
    to_location VARCHAR(255) NOT NULL,
    cargo_weight INT NOT NULL,
    deadline VARCHAR(100) NOT NULL,
    truck VARCHAR(100) NOT NULL,
    cargo VARCHAR(100) NOT NULL,
    distance VARCHAR(50) NOT NULL,
    duration VARCHAR(100) NOT NULL
);

