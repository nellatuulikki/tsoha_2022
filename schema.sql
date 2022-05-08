
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
    owner_id INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE amenities (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels ON DELETE CASCADE,
    amenity TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels ON DELETE CASCADE,
    customer_id INTEGER REFERENCES users ON DELETE CASCADE,
    rating INTEGER
);

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels ON DELETE CASCADE,
    room_description TEXT,
    guests INTEGER,
    square_meters INTEGER,
    number_of_rooms INTEGER,
    price FLOAT
);

CREATE TABLE reservations (
    reservation_id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms ON DELETE CASCADE,
    hotel_id INTEGER REFERENCES hotels ON DELETE CASCADE,
    customer_id INTEGER REFERENCES users ON DELETE CASCADE,
    check_in DATE,
    check_out DATE,
    guests INTEGER
);

CREATE TABLE calendar (
    id SERIAL PRIMARY KEY,
    reservation_date DATE,
    room_id INTEGER REFERENCES rooms ON DELETE CASCADE,
    available_rooms INTEGER
);
