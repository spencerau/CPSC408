
class customer:

    cursor = None
    conn = None

    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn
    
    def createTable(self):
        # Customer(CustomerID, Name, Email, #ofVisits, Address)
        # C_ID is an unique INT
        # Name, Email, Address are Strings, #ofVisits is an INT
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS
                            Customer (
                            CustomerID INT NOT NULL AUTO_INCREMENT,
                            Name VARCHAR(255),
                            Email VARCHAR(255),
                            Address VARCHAR(255),
                            PRIMARY KEY (CustomerID))
                            ''')
    def createViews(self):
        # Assuming you have already established a connection and created a cursor object
        view_name = 'customer_view'

        # Execute the query to check if the view exists
        self.cursor.execute(f'''SELECT COUNT(*) 
                                FROM INFORMATION_SCHEMA.VIEWS 
                                WHERE TABLE_NAME = '{view_name}' AND TABLE_SCHEMA = 'MadeInChinaYelp' ''')

        # Retrieve the result
        result = self.cursor.fetchone()

        # Check if the count = 0
        if result[0] == 0:
            self.cursor.execute('''CREATE VIEW customer_view AS
                                SELECT CustomerID, Name, Email, Address
                                FROM Customer
                                ''')

    def insertCustomer(self, name, email, address):
        self.cursor.execute('''INSERT INTO Customer 
                            (Name, Email, Address) 
                            VALUES (%s, %s, %s)''', 
                            (name, email, address))
        self.conn.commit()
        return self.cursor.lastrowid


    def updateCustomer(self, customerID, column, value):
        query = f'''
            UPDATE Customer
            SET {column} = %s
            WHERE CustomerID = %s
        '''
        self.cursor.execute(query, (value, customerID))
        # Commit the changes
        self.conn.commit()


    def deleteCustomer(self, customerID):
        try:
            # Start the transaction
            self.cursor.execute("START TRANSACTION")
            # Delete orders associated with the restaurant
            self.cursor.execute('''DELETE 
                                FROM Orders
                                WHERE Customer_ID = %s
                                ''', (customerID,))

            # Delete reservations associated with the restaurant
            self.cursor.execute('''DELETE 
                                FROM Reservation
                                WHERE Customer_ID = %s
                                ''', (customerID,))

            # Delete reviews associated with the restaurant
            self.cursor.execute('''DELETE 
                                FROM Review
                                WHERE Customer_ID = %s
                                ''', (customerID,))

            # Delete the restaurant from the Restaurant table
            self.cursor.execute('''DELETE 
                                FROM Customer
                                WHERE CustomerID = %s
                                ''', (customerID,))
            # Commit the transaction
            self.conn.commit()
            print("Deletion completed successfully.")
        except Exception as e:
            # Rollback the transaction in case of an error
            self.conn.rollback()
            print(f"An error occurred: {e}. Transaction rolled back.")

    def selectCustomer(self, customerID):
        self.cursor.execute('''SELECT * 
                            FROM customer_view 
                            WHERE CustomerID = %s
                            ''', (customerID,))
        return self.cursor.fetchall()
    
    def selectAllCustomers(self):
        self.cursor.execute('''SELECT * 
                            FROM customer_view''')
        return self.cursor.fetchall()

    

