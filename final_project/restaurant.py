
class restaurant:

    #create cursor object
    cursor = None
    conn = None

    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def createTable(self):

         # operatingTime(operatingTimeID, Monday, Tuesday, Wednesday, etc)
        # operatingTime_ID is a unique INT primary key
        # Monday, Tuesday, Wednesday, etc are columns with the rows being the operating times, 
        # opening times and closing times are stored in the same column as TIME
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS OperatingTime (
                            OperatingTimeID INT NOT NULL AUTO_INCREMENT,
                            MondayOpen TIME,
                            MondayClose TIME,
                            TuesdayOpen TIME,
                            TuesdayClose TIME,
                            WednesdayOpen TIME,
                            WednesdayClose TIME,
                            ThursdayOpen TIME,
                            ThursdayClose TIME,
                            FridayOpen TIME,
                            FridayClose TIME,
                            SaturdayOpen TIME,
                            SaturdayClose TIME,
                            SundayOpen TIME,
                            SundayClose TIME,
                            PRIMARY KEY (OperatingTimeID))
                            ''')

        # Specialty(Specialty_ID, Specialty)
        # Food/Specialty(FoodID, Name, Culture) F_ID is a unique INT
        # Name and Culture are Strings
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS
                            Specialty(SpecialtyID INT NOT NULL AUTO_INCREMENT,
                            Specialty VARCHAR(255),
                            Culture VARCHAR(255),
                            PRIMARY KEY (SpecialtyID))
                            ''')

        # Restaurant(RestaurantID, Score, Price, Address, Culture, OpenTime, CloseTime, Website, SpecialtyID*)
        # R_ID and S_ID are unique INTs
        # Score, price are DECIMAL or DOUBLEs
        # Address, Culture, and Website are Strings
        # OperatingTimeID is a foreign key to OperatingTime
        # SpecialtyID is a foreign key to Specialty
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Restaurant (
                            RestaurantID INT NOT NULL AUTO_INCREMENT, 
                            Name VARCHAR(255),
                            Score DECIMAL(2,1) DEFAULT 5.0, 
                            Price ENUM('1', '2', '3', '4', '5'),
                            Address VARCHAR(255), 
                            Website VARCHAR(255),
                            OperatingTime_ID INT,
                            Specialty_ID INT,
                            PRIMARY KEY (RestaurantID),
                            FOREIGN KEY (OperatingTime_ID) REFERENCES OperatingTime(OperatingTimeID),
                            FOREIGN KEY (Specialty_ID) REFERENCES Specialty(SpecialtyID))
                            ''')
    
    # insert a new operating time into the database using an array of times as parameter
    def insertOperatingTime(self, times):
        try:
            self.cursor.execute('''INSERT INTO OperatingTime (
                                MondayOpen, MondayClose, 
                                TuesdayOpen, TuesdayClose, 
                                WednesdayOpen, WednesdayClose, 
                                ThursdayOpen, ThursdayClose, 
                                FridayOpen, FridayClose, 
                                SaturdayOpen, SaturdayClose, 
                                SundayOpen, SundayClose) 
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                (times[0] if times[0] is not None else None,
                                times[1] if times[1] is not None else None,
                                times[2] if times[2] is not None else None,
                                times[3] if times[3] is not None else None,
                                times[4] if times[4] is not None else None,
                                times[5] if times[5] is not None else None,
                                times[6] if times[6] is not None else None,
                                times[7] if times[7] is not None else None,
                                times[8] if times[8] is not None else None,
                                times[9] if times[9] is not None else None,
                                times[10] if times[10] is not None else None,
                                times[11] if times[11] is not None else None,
                                times[12] if times[12] is not None else None,
                                times[13] if times[13] is not None else None))
            self.cursor.commit()
            return self.cursor.lastrowid
        except:
            self.cursor.rollback()
            return -1
    
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
        
    def insertRestaurant(self, name, price, address, website, operatingTimeID, specialtyID):
        # insert a restaurant into the database
        self.cursor.execute('''INSERT INTO Restaurant(Name, Price, Address, Website, OperatingTime_ID, Specialty_ID)
                            VALUES (%s, %s, %s, %s, %s, %s)''', (name, price, address, website, operatingTimeID, specialtyID))
        self.conn.commit()
        return self.cursor.lastrowid

    # delete a restaurant via restaurant ID
    def deleteRestaurant(self, r_id):
        # delete the restaurant with the given ID
        self.cursor.execute('''DELETE 
                            FROM Restaurant 
                            WHERE RestaurantID = %s
                            ''', (r_id,))
        # commit the changes
        self.conn.commit()
    
    # update a restaurant via restaurant ID
    def updateRestaurant(self, r_id, column, value):
        # update the restaurant with the given ID
        query = f'''UPDATE Restaurant 
                SET {column} = %s 
                WHERE RestaurantID = %s '''
        self.cursor.execute(query, (value, r_id))
        self.cursor.execute(query)
        # commit the changes
        self.conn.commit()

    def selectRestaurant(self, r_id):
        # view the restaurant with the given ID
        self.cursor.execute('''SELECT * 
                            FROM Restaurant 
                            WHERE RestaurantID = %s
                            ''', (r_id,))
        return self.cursor.fetchall()

    def selectAllRestaurants(self):
        # view all restaurants
        self.cursor.execute('''SELECT * 
                            FROM Restaurant
                            ''')
        return self.cursor.fetchall()

    def selectByCity(self, city):
        # view all restaurants in a given city
        self.cursor.execute('''SELECT * 
                            FROM Restaurant
                            WHERE Address LIKE %s
                            ''', (city,))
        return self.cursor.fetchall()
    

