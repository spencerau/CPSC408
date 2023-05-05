# file for transactions: reviews, orders, and reservations tables

class transactions:

    cursor = None

    def __init__(self, cursor):
        self.cursor = cursor

    def createTables(self):
        # Order(OrderID, Price, Date, Time, RestaurauntID*, CustomerID*)
        # O_ID, R_ID, and C_ID are unique INTS Price is a DOUBLE or DECIMAL
        #Date uses a DATE type, and Time uses a TIME type
        # RestaurauntID is a foreign key to Restauraunt
        # CustomerID is a foreign key to Customer
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                            OrderID INT NOT NULL AUTO_INCREMENT,
                            Price DECIMAL(2,1),
                            Date DATE,
                            Time TIME,
                            Restaurant_ID INT,
                            Customer_ID INT,
                            PRIMARY KEY (OrderID),
                            FOREIGN KEY (Restaurant_ID) REFERENCES Restaurant(RestaurantID),
                            FOREIGN KEY (Customer_ID) REFERENCES Customer(CustomerID))
                            ''')
        
        # Review(ReviewID, Score, Website, RestaurauntID*, CustomerID*)
        # Rev_ID, Res_ID, and C_ID are unique INTs Score is a DOUBLE or DECIMAL
        # Website is a String
        # RestaurauntID is a foreign key to Restauraunt
        # CustomerID is a foreign key to Customer
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Review (
                            ReviewID INT NOT NULL AUTO_INCREMENT,
                            Score DECIMAL(2,1),
                            Website VARCHAR(255),
                            Restaurant_ID INT,
                            Customer_ID INT,
                            PRIMARY KEY (ReviewID),
                            FOREIGN KEY (Restaurant_ID) REFERENCES Restaurant(RestaurantID),
                            FOREIGN KEY (Customer_ID) REFERENCES Customer(CustomerID))
                            ''')
        
        # Reservation(ReservationID, Date, Time, PartySize, RestaurauntID*, CustomerID*)
        # Reservation_ID, R_ID, and C_ID are unique INTs Date is a DATE
        # Time is a TIME, PartySize is an INT
        # RestaurauntID is a foreign key to Restauraunt
        # CustomerID is a foreign key to Customer
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Reservation (
                            ReservationID INT NOT NULL AUTO_INCREMENT,
                            Date DATE,
                            Time TIME,
                            PartySize INT,
                            Restaurant_ID INT,
                            Customer_ID INT,
                            PRIMARY KEY (ReservationID),
                            FOREIGN KEY (Restaurant_ID) REFERENCES Restaurant(RestaurantID),
                            FOREIGN KEY (Customer_ID) REFERENCES Customer(CustomerID))
                            ''')
        
    def insertOrder(self, price, date, time, restaurauntID, customerID):
        self.cursor.execute('''INSERT INTO Orders(Price, Date, Time, RestaurauntID, CustomerID)
                            VALUES (%s, %s, %s, %s, %s)''', (price, date, time, restaurauntID, customerID))
        self.cursor.commit()

    def insertReview(self, score, website, restaurauntID, customerID):
        self.cursor.execute('''INSERT INTO Review(Score, Website, RestaurauntID, CustomerID)
                            VALUES (%s, %s, %s, %s)''', (score, website, restaurauntID, customerID))
        self.cursor.commit()
    
    def insertReservation(self, date, time, partySize, restaurauntID, customerID):
        self.cursor.execute('''INSERT INTO Reservation(Date, Time, PartySize, RestaurauntID, CustomerID)
                            VALUES (%s, %s, %s, %s, %s)''', (date, time, partySize, restaurauntID, customerID))
        self.cursor.commit()

    def deleteOrder(self, orderID):
        self.cursor.execute('''DELETE 
                            FROM Order 
                            WHERE OrderID = %s''', (orderID))
        self.cursor.commit()
    
    def deleteReview(self, reviewID):
        self.cursor.execute('''DELETE 
                            FROM Review 
                            WHERE ReviewID = %s''', (reviewID))
        self.cursor.commit()
    
    def deleteReservation(self, reservationID):
        self.cursor.execute('''DELETE 
                            FROM Reservation 
                            WHERE ReservationID = %s''', (reservationID))
        self.cursor.commit()

    def updateOrder(self, column, value, orderID):
        self.cursor.execute('''UPDATE Orders 
                            SET %s = %s 
                            WHERE OrderID = %s
                            ''', (column, value, orderID))
        self.cursor.commit()

    def updateReview(self, column, value, reviewID):
        self.cursor.execute('''UPDATE Review 
                            SET %s = %s 
                            WHERE ReviewID = %s
                            ''', (column, value, reviewID))
        self.cursor.commit()
    
    def updateReservation(self, column, value, reservationID):
        self.cursor.execute('''UPDATE Reservation 
                            SET %s = %s 
                            WHERE ReservationID = %s
                            ''', (column, value, reservationID))
        self.cursor.commit()
    
    def selectOrder(self, orderID):
        self.cursor.execute('''SELECT * 
                            FROM Orders 
                            WHERE OrderID = %s
                            ''', (orderID))
        return self.cursor.fetchall()

    def selectReview(self, reviewID):
        self.cursor.execute('''SELECT * 
                            FROM Review 
                            WHERE ReviewID = %s
                            ''', (reviewID))
        return self.cursor.fetchall()

    def selectReservation(self, reservationID):
        self.cursor.execute('''SELECT * 
                            FROM Reservation 
                            WHERE ReservationID = %s
                            ''', (reservationID))
        return self.cursor.fetchall()
    
    def selectAllOrders(self):
        self.cursor.execute('''SELECT * FROM Orders''')
        return self.cursor.fetchall()
    
    def selectAllReviews(self):
        self.cursor.execute('''SELECT * FROM Review''')
        return self.cursor.fetchall()
    
    def selectAllReservations(self):
        self.cursor.execute('''SELECT * FROM Reservation''')
        return self.cursor.fetchall()
    
    def selectOrdersByCustomer(self, customerID):
        self.cursor.execute('''SELECT * 
                            FROM Orders 
                            WHERE CustomerID = %s
                            ''', (customerID))
        return self.cursor.fetchall()
    
    def selectReviewsByCustomer(self, customerID):
        self.cursor.execute('''SELECT * 
                            FROM Review 
                            WHERE CustomerID = %s
                            ''', (customerID))
        return self.cursor.fetchall()
    
    def selectReservationsByCustomer(self, customerID):
        self.cursor.execute('''SELECT * 
                            FROM Reservation 
                            WHERE CustomerID = %s
                            ''', (customerID))
        return self.cursor.fetchall()
    
    def selectOrdersByRestauraunt(self, restaurauntID):
        self.cursor.execute('''SELECT * 
                            FROM Orders 
                            WHERE RestaurauntID = %s
                            ''', (restaurauntID))
        return self.cursor.fetchall()
    
    def selectReviewsByRestauraunt(self, restaurauntID):
        self.cursor.execute('''SELECT * 
                            FROM Review 
                            WHERE RestaurauntID = %s
                            ''', (restaurauntID))
        return self.cursor.fetchall()
    
    def selectReservationsByRestauraunt(self, restaurauntID):
        self.cursor.execute('''SELECT * 
                            FROM Reservation 
                            WHERE RestaurauntID = %s
                            ''', (restaurauntID))
        return self.cursor.fetchall()
    
