CREATE TABLE trucks (
    id CHAR(4) NOT NULL PRIMARY KEY,
    brand varchar(255),
    name varchar(255),
    fuel_tank int,
    liters_per_100km int,
    max_weight int,
    horsepower int
);


INSERT INTO trucks (id, brand, name, fuel_tank, liters_per_100km, max_weight)
VALUES
    ('0000', 'Scania', 'R2016', 700, 30, 25500, 730),
    ('0001', 'Volvo', 'FH16 2016', 600, 25, 26000, 750),
    ('0002', 'Mercedes', 'Actrod', 650, 35, 24000, 625),
    ('0003', 'MAN', 'TGX EURO 6', 550, 28, 24500, 640),
    ('0004', 'Renault', 'T', 500, 32, 23000, 520)