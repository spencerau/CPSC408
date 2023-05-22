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
        
    def createViews(self):
        # Assuming you have already established a connection and created a cursor object
        view_name = 'order_view'
        # Execute the query to check if the view exists
        self.cursor.execute(f'''SELECT COUNT(*) 
                                FROM INFORMATION_SCHEMA.VIEWS 
                                WHERE TABLE_NAME = '{view_name}' AND TABLE_SCHEMA = 'MadeInChinaYelp' ''')
        # Retrieve the result
        result = self.cursor.fetchone()
        # Check if the count = 0
        if result[0] == 0:
            self.cursor.execute('''CREATE VIEW order_view AS
                                SELECT o.OrderID, o.Price, o.Date, o.Time, r.Name AS RestaurantName, c.Name AS CustomerName, o.Restaurant_ID, o.Customer_ID
                                FROM Orders o
                                JOIN Restaurant r ON o.Restaurant_ID = r.RestaurantID
                                JOIN Customer c ON o.Customer_ID = c.CustomerID;
                                ''')
        
        # Assuming you have already established a connection and created a cursor object
        view_name = 'review_view'
        # Execute the query to check if the view exists
        self.cursor.execute(f'''SELECT COUNT(*) 
                                FROM INFORMATION_SCHEMA.VIEWS 
                                WHERE TABLE_NAME = '{view_name}' AND TABLE_SCHEMA = 'MadeInChinaYelp' ''')
        # Retrieve the result
        result = self.cursor.fetchone()
        # Check if the count = 0
        if result[0] == 0:
            self.cursor.execute('''CREATE VIEW review_view AS
                                SELECT r.ReviewID, r.Score, r.Website, res.Name AS RestaurantName, c.Name AS CustomerName, r.Restaurant_ID, r.Customer_ID
                                FROM Review r
                                JOIN Restaurant res ON r.Restaurant_ID = res.RestaurantID
                                JOIN Customer c ON r.Customer_ID = c.CustomerID;
                                ''')
        
        # Assuming you have already established a connection and created a cursor object
        view_name = 'reservation_view'
        # Execute the query to check if the view exists
        self.cursor.execute(f'''SELECT COUNT(*) 
                                FROM INFORMATION_SCHEMA.VIEWS 
                                WHERE TABLE_NAME = '{view_name}' AND TABLE_SCHEMA = 'MadeInChinaYelp' ''')
        # Retrieve the result
        result = self.cursor.fetchone()
        # Check if the count = 0
        if result[0] == 0:
            self.cursor.execute('''CREATE VIEW reservation_view AS
                                SELECT res.ReservationID, res.Date, res.Time, res.PartySize, r.Name AS RestaurantName, c.Name AS CustomerName, res.Restaurant_ID, res.Customer_ID
                                FROM Reservation res
                                JOIN Restaurant r ON res.Restaurant_ID = r.RestaurantID
                                JOIN Customer c ON res.Customer_ID = c.CustomerID;
                                ''')
        
    def insertOrder(self, price, RestaurantID, customerID):
        self.cursor.execute('''INSERT INTO Orders(Price, Date, Time, Restaurant_ID, Customer_ID)
                            VALUES (%s, NOW(), NOW(), %s, %s)''', 
                            (price, RestaurantID, customerID))
        self.conn.commit()

    def insertReview(self, score, website, RestaurantID, customerID):
        self.cursor.execute('''INSERT INTO Review(Score, Website, Restaurant_ID, Customer_ID)
                            VALUES (%s, %s, %s, %s)''', (score, website, RestaurantID, customerID))
        # update the score for restaurant
        self.cursor.execute('''UPDATE Restaurant
                            SET Score = (SELECT AVG(Score) 
                                        FROM Review
                                        WHERE Restaurant_ID = %s) 
                            WHERE RestaurantID = %s
                            ''', (RestaurantID, RestaurantID))
        self.conn.commit()
    
    def insertReservation(self, date, time, partySize, RestaurantID, customerID):
        self.cursor.execute('''INSERT INTO Reservation(`Date`, `Time`, PartySize, Restaurant_ID, Customer_ID)
                       VALUES (%s, %s, %s, %s, %s)''', (date, time, partySize, RestaurantID, customerID))
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

    def updateOrder(self, orderID, column, value):
        query = f'''
            UPDATE Orders
            SET {column} = %s
            WHERE OrderID = %s
        '''
        self.cursor.execute(query, (value, orderID))
        # Commit the changes
        self.conn.commit()

    def updateReview(self, reviewID, column, value):
        query = f'''
            UPDATE Review
            SET {column} = %s
            WHERE ReviewID = %s
        '''
        self.cursor.execute(query, (value, reviewID))
        # Commit the changes
        self.conn.commit()
    
    def updateReservation(self, reservationID, column, value):
        query = f'''
            UPDATE Reservation
            SET {column} = %s
            WHERE ReservationID = %s
        '''
        self.cursor.execute(query, (value, reservationID))
        # Commit the changes
        self.conn.commit()
    
    def selectOrder(self, orderID):
        self.cursor.execute('''SELECT OrderID, RestaurantName, CustomerName, Price, Date, Time
                            FROM order_view 
                            WHERE OrderID = %s
                            ''', (orderID,))
        return self.cursor.fetchall()

    def selectReview(self, reviewID):
        self.cursor.execute('''SELECT ReviewID, RestaurantName, CustomerName  Score, Website
                            FROM review_view 
                            WHERE ReviewID = %s
                            ''', (reviewID,))
        return self.cursor.fetchall()

    def selectReservation(self, reservationID):
        self.cursor.execute('''SELECT ReservationID, Date, Time, PartySize, RestaurantName, CustomerName
                            FROM reservation_view 
                            WHERE ReservationID = %s
                            ''', (reservationID,))
        return self.cursor.fetchall()
    
    def selectAllOrders(self):
        self.cursor.execute('''SELECT OrderID, Price, Date, Time, RestaurantName, CustomerName
                            FROM order_view''')
        return self.cursor.fetchall()
    
    def selectAllReviews(self):
        self.cursor.execute('''SELECT ReviewID, Score, Website, RestaurantName, CustomerName 
                            FROM review_view''')
        return self.cursor.fetchall()
    
    def selectAllReservations(self):
        self.cursor.execute('''SELECT ReservationID, Date, Time, PartySize, RestaurantName, CustomerName
                            FROM reservation_view''')
        return self.cursor.fetchall()
    
    def selectOrdersByCustomer(self, customerID):
        self.cursor.execute('''SELECT OrderID, Price, Date, Time, RestaurantName, CustomerName
                            FROM order_view 
                            WHERE Customer_ID = %s
                            ''', (customerID,))
        return self.cursor.fetchall()
    
    def selectReviewsByCustomer(self, customerID):
        self.cursor.execute('''SELECT ReviewID, Score, Website, RestaurantName, CustomerName 
                            FROM review_view 
                            WHERE Customer_ID = %s
                            ''', (customerID,))
        return self.cursor.fetchall()
    
    def selectReservationsByCustomer(self, customerID):
        self.cursor.execute('''SELECT ReservationID, Date, Time, PartySize, RestaurantName, CustomerName
                            FROM reservation_view 
                            WHERE Customer_ID = %s
                            ''', (customerID,))
        return self.cursor.fetchall()
    
    def selectOrdersByRestaurant(self, RestaurantID):
        self.cursor.execute('''SELECT OrderID, Price, Date, Time, RestaurantName, CustomerName
                            FROM order_view 
                            WHERE Restaurant_ID = %s
                            ''', (RestaurantID,))
        return self.cursor.fetchall()
    
    def selectReviewsByRestaurant(self, RestaurantID):
        self.cursor.execute('''SELECT ReviewID, Score, Website, RestaurantName, CustomerName 
                            FROM review_view 
                            WHERE Restaurant_ID = %s
                            ''', (RestaurantID,))
        return self.cursor.fetchall()
    
    def selectReservationsByRestaurant(self, RestaurantID):
        self.cursor.execute('''SELECT ReservationID, Date, Time, PartySize, RestaurantName, CustomerName
                            FROM reservation_view 
                            WHERE Restaurant_ID = %s
                            ''', (RestaurantID,))
        return self.cursor.fetchall()
    