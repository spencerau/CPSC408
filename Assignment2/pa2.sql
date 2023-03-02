/*
 Spencer Au
 */

/*
 1. Create a table Patient(patientID, name, dob, phone)
Note that patientID is the primary key of the table. Use appropriate data
types. patientID and name need to have the NOT NULL constraint.
 */
CREATE TABLE Patient(
    patientID INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    dob DATE,
    phone VARCHAR(10)
);
/*
 2. Alter the Patient table and add a new column address to it.
 */
ALTER TABLE Patient
ADD COLUMN address VARCHAR(40);
/*
 3. Drop the Patient table.
 */
DROP TABLE Patient;
/*
 4. Write a query to retrieve the first name, last name, and email from the employees
 table.
 */
SELECT FirstName, LastName, Email
FROM employees;
/*
 5. Write a query to retrieve the IDs of employees who were hired in 2004.
 */
SELECT EmployeeId
FROM employees
WHERE HireDate BETWEEN '2004-01-01' AND '2004-12-31';
/* WHERE date BETWEEN '2004%';
/*
 6. Write a query to retrieve all records of employees who are a manager (i.e., manager
 is in their job title).
 */
SELECT *
FROM employees
WHERE Title LIKE '%manager%';
/*
 7. Write a query to return the unique billing cities from the invoices table.
 */
SELECT DISTINCT BillingCity
FROM invoices;
/*
 8. Write a query to return the unique billing countries where the invoice total is
 greater than 10 and invoice Date is from 2013.
 */
SELECT DISTINCT BillingCountry
FROM invoices
WHERE Total > 10
AND InvoiceDate BETWEEN '2013-01-01' AND '2013-12-31';





