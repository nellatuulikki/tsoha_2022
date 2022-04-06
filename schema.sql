CREATE TABLE hotels (
    id SERIAL PRIMARY KEY,
    hotel_name TEXT,
    hotel_address TEXT,
    stars INTEGER
);

CREATE TABLE amenities (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels,
    amenity TEXT
);

CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    hotel_id TEXT,
    reviewer TEXT,
    rating INTEGER,
    comment TEXT
);

CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    hotel_id TEXT,
    guest_number INTEGER,
    square_meters INTEGER,
    number_of_rooms INTEGER
);

CREATE TABLE reservations (
    reservation_id SERIAL PRIMARY KEY,
    hotel_id TEXT,
    room_id TEXT,
    check_in TEXT,
    check_out TEXT,
    customer TEXT,
);

CREATE TABLE calendar (
    id SERIAL PRIMARY KEY,
    reservation_date TEXT,
    room_id TEXT,
    reservation_id TEXT,
    available_rooms INTEGER,
);