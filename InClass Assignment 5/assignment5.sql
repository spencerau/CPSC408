-- 1) Write a SQL query that adds the UNIQUE constraint to the title attribute of the film table.
ALTER TABLE film
ADD CONSTRAINT uniqueName UNIQUE (title);

-- 2) Write a query to remove this constraint from the table film.
ALTER TABLE film
DROP CONSTRAINT uniqueName;

-- 3) Create a view that shows all films released in 2006 whose title begins with A.
CREATE VIEW vFilmsBefore2006 AS
SELECT title, release_year
FROM film
WHERE release_year = 2006 AND title LIKE 'A%';

-- DROP VIEW if exists vfilmsbefore2006;

-- 4) Write a query that prints all records from the view created in question 3.
SELECT *
FROM vfilmsbefore2006;

-- 5) Using the below query, create a ratings log table in the Sakila DB. Then, using this log table, create a trigger
-- AFTER INSERT on the film table that warns us if a user inserts a movie with an R rating.
CREATE TABLE rating_log(
    user VARCHAR(50),
    action VARCHAR(120)
);

DELIMITER $$
CREATE TRIGGER ratingWarning
    AFTER INSERT ON film
    FOR EACH ROW
BEGIN
    if rating = 'R' THEN
        INSERT INTO rating_log
        VALUES(USER(), 'R movie inserted');
    END IF;
END $$

SHOW TRIGGERS FROM sakila LIKE 'film';

-- 6) Create a query to insert an R rated movie into the film table. What record is inserted into
-- the rating_log table?
INSERT INTO film(title, language_id, rating)
VALUES('R Movie', 1, 'R');

DESCRIBE film;

SHOW COLUMNS FROM film LIKE 'rating';

-- 7) Create a stored procedure that returns the release year of a movie as an OUT variable, using
-- the title of the movie as an IN variable.
DELIMITER $$
CREATE PROCEDURE getReleaseYear(
    IN title VARCHAR(128),
    OUT releaseYear year
)
BEGIN
    SELECT film.release_year INTO releaseYear
    FROM film
    WHERE title = film.title;
END $$

-- 8) Create a query to call your stored procedure and Select the result
CALL getReleaseYear('ACADEMY DINOSAUR', @releaseYear);
SELECT @releaseYear AS releaseYear;




