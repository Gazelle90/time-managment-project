/*CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE
);

CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL
);

CREATE TABLE times_daily (
    id SERIAL PRIMARY KEY,
    person_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    lunch_break INTEGER DEFAULT 0,
    hours NUMERIC(6,2),

    FOREIGN KEY (person_id)
        REFERENCES person(id),

    FOREIGN KEY (company_id)
        REFERENCES company(id)
);
*/

/*INSERT INTO person (name, email) VALUES
('Anna Andersson', 'anna@example.com'),
('Erik Svensson', 'erik@example.com'),
('Sara Lindberg', 'sara@example.com'),
('Johan Karlsson', 'johan@example.com'),
('Maria Nilsson', 'maria@example.com'),
('Ali Hassan', 'ali@example.com'),
('Emma Berg', 'emma@example.com'),
('David Johansson', 'david@example.com'),
('Sofia Persson', 'sofia@example.com'),
('Daniel Eriksson', 'daniel@example.com');*/

/*INSERT INTO company (name) VALUES
('IKEA'),
('Volvo'),
('Spotify'),
('Ericsson'),
('H&M');*/

CREATE VIEW view_weekly AS
SELECT
    c.id AS company_id,
    c.name AS company_name,
    DATE_TRUNC('week', t.date)::date AS week_start,
    (DATE_TRUNC('week', t.date) + INTERVAL '6 days')::date AS week_end,
    SUM(ROUND(EXTRACT(EPOCH FROM (t.end_time - t.start_time - t.lunch_break)) / 3600.0, 2)) AS total_hours
FROM company c
JOIN times_daily t ON c.id = t.company_id
GROUP BY
    c.id,
    c.name,
    DATE_TRUNC('week', t.date);

SELECT * from person;

SELECT * FROM company;
