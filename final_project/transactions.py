# file for transactions: reviews, orders, and reservations tables

class transactions:

    cursor = None
    conn = None

    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def createTables(self):
        # Order(OrderID, Price, Date, Time, RestaurantID*, CustomerID*)
        # O_ID, R_ID, and C_ID are unique INTS Price is a DOUBLE or DECIMAL
        #Date uses a DATE type, and Time uses a TIME type
        # RestaurantID is a foreign key to Restaurant
        # CustomerID is a foreign key to Customer
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                            OrderID INT NOT NULL AUTO_INCREMENT,
                            Price DECIMAL,
                            Date DATE,
                            Time TIME,
                            Restaurant_ID INT,
                            Customer_ID INT,
                            PRIMARY KEY (OrderID),
                            FOREIGN KEY (Restaurant_ID) REFERENCES Restaurant(RestaurantID),
                            FOREIGN KEY (Customer_ID) REFERENCES Customer(CustomerID))
                            ''')
        
        # Review(ReviewID, Score, Website, RestaurantID*, CustomerID*)
        # Rev_ID, Res_ID, and C_ID are unique INTs Score is a DOUBLE or DECIMAL
        # Website is a String
        # RestaurantID is a foreign key to Restaurant
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
        
        # Reservation(ReservationID, Date, Time, PartySize, RestaurantID*, CustomerID*)
        # Reservation_ID, R_ID, and C_ID are unique INTs Date is a DATE
        # Time is a TIME, PartySize is an INT
        # RestaurantID is a foreign key to Restaurant
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
        
    def insertOrder(self, price, RestaurantID, customerID):
        self.cursor.execute('''INSERT INTO Orders(Price, Date, Time, Restaurant_ID, Customer_ID)
                            VALUES (%s, NOW(), NOW(), %s, %s)''', 
                            (price, RestaurantID, customerID))
        self.conn.commit()

    def insertReview(self, score, website, RestaurantID, customerID):
        self.cursor.execute('''INSERT INTO Review(Score, Website, Restaurant_ID, Customer_ID)
                            VALUES (%s, %s, %s, %s)''', (score, website, RestaurantID, customerID))
        self.conn.commit()
    
    def insertReservation(self, partySize, RestaurantID, customerID):
        self.cursor.execute('''INSERT INTO Reservation(Date, Time, PartySize, Restaurant_ID, Customer_ID)
                            VALUES (NOW(), NOW(), %s, %s, %s)''', (partySize, RestaurantID, customerID))
        self.conn.commit()

    def deleteOrder(self, orderID):
        self.cursor.execute('''DELETE 
                            FROM Order 
                            WHERE OrderID = %s''', (orderID,))
        self.conn.commit()
    
    def deleteReview(self, reviewID):
        self.cursor.execute('''DELETE 
                            FROM Review 
                            WHERE ReviewID = %s''', (reviewID,))
        self.conn.commit()
    
    def deleteReservation(self, reservationID):
        self.cursor.execute('''DELETE 
                            FROM Reservation 
                            WHERE ReservationID = %s''', (reservationID))
        self.conn.commit()

    def updateOrder(self, column, value, orderID):
        self.cursor.execute('''UPDATE Orders 
                            SET %s = %s 
                            WHERE OrderID = %s
                            ''', (column, value, orderID))
        self.conn.commit()

    def updateReview(self, column, value, reviewID):
        self.cursor.execute('''UPDATE Review 
                            SET %s = %s 
                            WHERE ReviewID = %s
                            ''', (column, value, reviewID))
        self.conn.commit()
    
    def updateReservation(self, column, value, reservationID):
        self.cursor.execute('''UPDATE Reservation 
                            SET %s = %s 
                            WHERE ReservationID = %s
                            ''', (column, value, reservationID))
        self.conn.commit()
    
    def selectOrder(self, orderID):
        self.cursor.execute('''SELECT * 
                            FROM Orders 
                            WHERE OrderID = %s
                            ''', (orderID,))
        return self.cursor.fetchall()

    def selectReview(self, reviewID):
        self.cursor.execute('''SELECT * 
                            FROM Review 
                            WHERE ReviewID = %s
                            ''', (reviewID,))
        return self.cursor.fetchall()

    def selectReservation(self, reservationID):
        self.cursor.execute('''SELECT * 
                            FROM Reservation 
                            WHERE ReservationID = %s
                            ''', (reservationID,))
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
                            WHERE Customer_ID = %s
                            ''', (customerID,))
        return self.cursor.fetchall()
    
    def selectReviewsByCustomer(self, customerID):
        self.cursor.execute('''SELECT * 
                            FROM Review 
                            WHERE Customer_ID = %s
                            ''', (customerID,))
        return self.cursor.fetchall()
    
    def selectReservationsByCustomer(self, customerID):
        self.cursor.execute('''SELECT * 
                            FROM Reservation 
                            WHERE Customer_ID = %s
                            ''', (customerID,))
        return self.cursor.fetchall()
    
    def selectOrdersByRestaurant(self, RestaurantID):
        self.cursor.execute('''SELECT * 
                            FROM Orders 
                            WHERE Restaurant_ID = %s
                            ''', (RestaurantID,))
        return self.cursor.fetchall()
    
    def selectReviewsByRestaurant(self, RestaurantID):
        self.cursor.execute('''SELECT * 
                            FROM Review 
                            WHERE Restaurant_ID = %s
                            ''', (RestaurantID,))
        return self.cursor.fetchall()
    
    def selectReservationsByRestaurant(self, RestaurantID):
        self.cursor.execute('''SELECT * 
                            FROM Reservation 
                            WHERE Restaurant_ID = %s
                            ''', (RestaurantID,))
        return self.cursor.fetchall()
    
    # subquery to get the average price of all orders made by a customer, where the customer has made at least 3 orders:
    def selectAvgPriceOrders(self):
        self.cursor.execute('''SELECT Customer_ID, AVG(Price) AS AveragePrice
                            FROM Orders
                            WHERE Customer_ID IN (
                                SELECT Customer_ID
                                FROM Orders
                                GROUP BY Customer_ID
                                HAVING COUNT(*) >= 3
                            )
                            GROUP BY Customer_ID;
                            ''' )
        return self.cursor.fetchall()
    


    

    
