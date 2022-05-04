CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE hotels (
    id SERIAL PRIMARY KEY,
    hotel_name TEXT UNIQUE,
    hotel_address TEXT,
    stars INTEGER,
    owner_id INTEGER REFERENCES users
);

CREATE TABLE amenities (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels,
    amenity TEXT
);

CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels,
    reviewer TEXT,
    rating INTEGER,
    comment TEXT
);

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels,
    room_description TEXT,
    guests INTEGER,
    square_meters INTEGER,
    number_of_rooms INTEGER,
    price FLOAT
);

CREATE TABLE reservations (
    reservation_id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms,
    hotel_id INTEGER REFERENCES hotels,
    customer_id INTEGER REFERENCES users,
    check_in DATE,
    check_out DATE,
    guests INTEGER
);

CREATE TABLE calendar (
    id SERIAL PRIMARY KEY,
    reservation_date DATE,
    room_id INTEGER REFERENCES rooms,
    available_rooms INTEGER
);
