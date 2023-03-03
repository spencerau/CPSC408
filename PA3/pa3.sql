/*
Spencer Au
CPSC 408 Assignment 3
Using the Chinook Database
*/

/* SET 1 */
/* 1) Write a query to return the average duration of tracks (in milliseconds) for each composer. */
SELECT Composer,
       AVG(Milliseconds) AS AvgDuration
FROM tracks
GROUP BY Composer;

/* 2) Write a query to return the total number of unique customers. */
SELECT DISTINCT COUNT(*) AS numUnique
FROM customers;

/* 3) Write a query to get the total number of records and the max unit price for each media type,
genre combination. */
SELECT MediaTypeId,
       GenreId,
       COUNT(*) AS Total,
       MAX(UnitPrice) AS MaxUnitPrice
FROM tracks
GROUP BY tracks.MediaTypeId, tracks.GenreId;

/* 4) Write a query to get the average duration of tracks (in milliseconds) for each genre. Must have
genre name in the result. */
SELECT g.Name,
       AVG(Milliseconds) AS AvgDuration
FROM tracks AS t
INNER JOIN genres AS g
ON t.GenreId = g.GenreId
GROUP BY t.GenreId;


/* 5) Write a query to show the total number of albums per artist name. */

/* 6) Write a query to return the total number of invoices per billing city, billed in USA. */

/* SET 2 */

/* 1) Write a query to return the average duration of tracks (in milliseconds) for each composer, for tracks with a
   duration shorter than 375000 milliseconds. */

/* 2) Write a query to return the average duration of tracks (in milliseconds) for each composer, where the average
   duration is less than 375000 milliseconds. */

/* 3) Find the names of all billing countries that have fewer than 10 records. */


/* 4) Find the name of the billing country that has 8 cities in the invoices table. */

/* 5) Write a query to find billing countries and the sum of their totals, that have more than 5 records
each, from the year 2010. */