
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
                            NumVisits INT DEFAULT 0,
                            Address VARCHAR(255),
                            PRIMARY KEY (CustomerID))
                            ''')
        
    def insertCustomer(self, name, email, address):
        self.cursor.execute('''INSERT INTO Customer 
                            (Name, Email, Address) 
                            VALUES (%s, %s, %s)''', 
                            (name, email, address))
        self.conn.commit()
        return self.cursor.lastrowid


    def updateCustomer(self, column, value, customerID):
        self.cursor.execute('''UPDATE Customer
                            SET {} = '{}'
                            WHERE CustomerID = %s'''.format(column, value), (customerID,))
        self.conn.commit()


    def deleteCustomer(self, customerID):
        self.cursor.execute('''DELETE 
                            FROM Customer 
                            WHERE CustomerID = %s''', (customerID,))
        self.conn.commit()

    def selectCustomer(self, customerID):
        self.cursor.execute('''SELECT * 
                            FROM Customer 
                            WHERE CustomerID = %s
                            ''', (customerID,))
        return self.cursor.fetchall()
    
    def selectAllCustomers(self):
        self.cursor.execute('''SELECT * 
                            FROM Customer''')
        return self.cursor.fetchall()

    

