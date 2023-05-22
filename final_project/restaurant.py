
class restaurant:

    #create cursor object
    cursor = None
    conn = None

    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def createTable(self):
        # Specialty(Specialty_ID, Specialty)
        # Food/Specialty(FoodID, Name, Culture) F_ID is a unique INT
        # Name and Culture are Strings
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS
                            Specialty(SpecialtyID INT NOT NULL AUTO_INCREMENT,
                            Specialty VARCHAR(255),
                            Culture VARCHAR(255),
                            PRIMARY KEY (SpecialtyID))
                            ''')

        # Restaurant(RestaurantID, Score, Price, Address, Culture, Website, SpecialtyID*)
        # R_ID and S_ID are unique INTs
        # Score, price are DECIMAL or DOUBLEs
        # Address, Culture, and Website are Strings
        # SpecialtyID is a foreign key to Specialty
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Restaurant (
                            RestaurantID INT NOT NULL AUTO_INCREMENT, 
                            Name VARCHAR(255),
                            Score DECIMAL(2,1) DEFAULT 5.0, 
                            Price ENUM('1', '2', '3', '4', '5'),
                            Address VARCHAR(255), 
                            Website VARCHAR(255),
                            Specialty_ID INT,
                            PRIMARY KEY (RestaurantID),
                            FOREIGN KEY (Specialty_ID) REFERENCES Specialty(SpecialtyID))
                            ''')
        
    def createViews(self):
        # Assuming you have already established a connection and created a cursor object
        view_name = 'restaurant_view'

        # Execute the query to check if the view exists
        self.cursor.execute(f'''SELECT COUNT(*) 
                                FROM INFORMATION_SCHEMA.VIEWS 
                                WHERE TABLE_NAME = '{view_name}' AND TABLE_SCHEMA = 'MadeInChinaYelp' ''')

        # Retrieve the result
        result = self.cursor.fetchone()

        # Check if the count = 0
        if result[0] == 0:
            self.cursor.execute('''CREATE VIEW restaurant_view AS
                                SELECT RestaurantID, Name, Score, Price, Address, Website, s.Specialty, s.Culture
                                FROM Restaurant r
                                JOIN Specialty s ON r.Specialty_ID = s.SpecialtyID
                                ''')

    def createIndex(self):
        # Check if the index exists
        query = '''
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE TABLE_SCHEMA = 'MadeInChinaYelp'
                AND TABLE_NAME = 'Restaurant'
                AND INDEX_NAME = 'restaurant_name_index'
                '''
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]

        if result == 0:
            # Create the index
            create_index_query = '''
                CREATE INDEX restaurant_name_index ON Restaurant (Name)
            '''
            self.cursor.execute(create_index_query)
            self.conn.commit()
    
    def insertSpecialty(self, specialty, culture):
        # check if the specialty already exists
        self.cursor.execute('''SELECT *
                            FROM Specialty
                            WHERE Specialty = %s OR Culture = %s
                            ''', (specialty, culture))
        # if the specialty already exists, return the specialty ID
        if self.cursor.rowcount > 0:
            return self.cursor.fetchone()[0]

        self.cursor.fetchall()

        # insert a specialty into the database
        self.cursor.execute('''INSERT INTO Specialty(Specialty, Culture)
                            VALUES (%s, %s)''', (specialty, culture))
        self.conn.commit()
        return self.cursor.lastrowid
        
    def insertRestaurant(self, name, price, address, website, specialtyID):
        # insert a restaurant into the database
        self.cursor.execute('''INSERT INTO Restaurant(Name, Price, Address, Website, Specialty_ID)
                            VALUES (%s, %s, %s, %s, %s)''', (name, price, address, website, specialtyID))
        self.conn.commit()
        return self.cursor.lastrowid

    # delete a restaurant via restaurant ID
    def deleteRestaurant(self, r_id):
        try:
            # Start the transaction
            self.cursor.execute("START TRANSACTION")
            # Delete orders associated with the restaurant
            self.cursor.execute('''DELETE 
                                FROM Orders 
                                WHERE Restaurant_ID = %s
                                ''', (r_id,))

            # Delete reservations associated with the restaurant
            self.cursor.execute('''DELETE 
                            FROM Reservation
                            WHERE Restaurant_ID = %s
                            ''', (r_id,))

            # Delete reviews associated with the restaurant
            self.cursor.execute('''DELETE 
                                FROM Review
                                WHERE Restaurant_ID = %s
                                ''', (r_id,))

            # Delete the restaurant from the Restaurant table
            self.cursor.execute('''DELETE 
                                FROM Restaurant 
                                WHERE RestaurantID = %s
                                ''', (r_id,))
            # Commit the transaction
            self.conn.commit()
            print("Deletion completed successfully.")
        except Exception as e:
            # Rollback the transaction in case of an error
            self.conn.rollback()
            print(f"An error occurred: {e}. Transaction rolled back.")
    
    # update a restaurant via restaurant ID
    def updateRestaurant(self, r_id, column, value):
        try:
            # Update the restaurant with the given ID
            query = f'''
                UPDATE Restaurant
                SET {column} = %s
                WHERE RestaurantID = %s
            '''
            self.cursor.execute(query, (value, r_id))
            # Commit the changes
            self.conn.commit()
        except Exception as e:
            print(f"An error occurred while updating the restaurant: {e}")

    def selectRestaurant(self, r_id):
        # view the restaurant with the given ID
        self.cursor.execute('''SELECT * 
                            FROM restaurant_view 
                            WHERE RestaurantID = %s
                            ''', (r_id,))
        return self.cursor.fetchall()

    def selectAllRestaurants(self):
        # view all restaurants
        self.cursor.execute('''SELECT * 
                            FROM restaurant_view
                            ''')
        return self.cursor.fetchall()
    
    def selectBySpecialty(self, specialty):
        # view all restaurants with a given specialty
        self.cursor.execute('''SELECT * 
                            FROM restaurant_view
                            WHERE Specialty = %s
                            ''', (specialty,))
        return self.cursor.fetchall()
    
    def findNewByCulture(self, customer_id, culture):
        # Execute the SQL query to retrieve the restaurants the customer hasn't tried
        query = '''
            SELECT r.RestaurantID, r.Name, s.Specialty, r.Score, r.Price, r.Website
            FROM Restaurant r
            LEFT JOIN Orders o 
                ON r.RestaurantID = o.Restaurant_ID AND o.Customer_ID = %s
            LEFT JOIN Specialty s
                ON r.Specialty_ID = s.SpecialtyID
            WHERE o.OrderID IS NULL AND s.Culture = %s
        '''
        self.cursor.execute(query, (customer_id, culture))
        return self.cursor.fetchall()
    
    def getOrders(self):
        # Execute the SQL query to retrieve the aggregated information
        query = '''
                SELECT r.Name AS RestaurantName, COUNT(o.OrderID) AS OrderCount
                FROM Restaurant r
                INNER JOIN Orders o ON r.RestaurantID = o.Restaurant_ID
                GROUP BY r.RestaurantID, r.Name
                '''

        self.cursor.execute(query)

        # Fetch all the rows returned by the query
        return self.cursor.fetchall()
    
    def selectByName(self, name):
        # view all restaurants with a given name
        self.cursor.execute('''SELECT RestaurantID, Name, Score, Price, Address, Website, s.Specialty, s.Culture
                            FROM Restaurant USE INDEX (restaurant_name_index)
                            INNER JOIN Specialty s ON Restaurant.Specialty_ID = s.SpecialtyID
                            WHERE Name = %s
                            ''', (name,))
        return self.cursor.fetchall()
    