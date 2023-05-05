
class restaurant:

    #create cursor object
    cursor = None

    def __init__(self, cursor):
        self.cursor = cursor

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
                            Score DECIMAL(2,1) DEFAULT 5.0, 
                            Price DECIMAL(2,1), 
                            Address VARCHAR(255), 
                            Culture VARCHAR(255), 
                            Website VARCHAR(255),
                            OperatingTime_ID INT,
                            Specialty_ID INT,
                            PRIMARY KEY (RestaurantID),
                            FOREIGN KEY (OperatingTime_ID) REFERENCES OperatingTime(OperatingTimeID),
                            FOREIGN KEY (Specialty_ID) REFERENCES Specialty(SpecialtyID))
                            ''')

    # add a restaurant to the database via user input
    def addRestaurantManual(self):
        # prompt for user input
        print("Please enter the following information about the restaurant you would like to add:")
        # get user input for price
        try:
            price = int(input("Enter in the price range between 1 and 5: "))
            if price >= 1 and price <= 5:
                # do nothing
                pass
            else:
                print("Input is out of range. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer between 1 and 5.")
        price = input()

        # get user input for address
        addr = input("Enter in the address of the restaurant: ")

    # delete a restaurant via restaurant ID
    def deleteRestaurant(self, r_id):
        # delete the restaurant with the given ID
        self.cursor.execute('''DELETE 
                            FROM Restaurant 
                            WHERE Restauraunt_ID = %s
                            ''', (r_id,))
        # commit the changes
        self.cursor.commit()
    
    # update a restaurant via restaurant ID
    def updateRestaurant(self, r_id):
        pass

    def selectRestaurant(self, r_id):
        # view the restaurant with the given ID
        self.cursor.execute('''SELECT * 
                            FROM Restaurant 
                            WHERE Restauraunt_ID = %s
                            ''', (r_id,))
        # commit the changes
        self.cursor.commit()

    def selectAllRestaurants(self):
        # view all restaurants
        self.cursor.execute('''SELECT * 
                            FROM Restaurant
                            ''')
        # commit the changes
        self.cursor.commit()

    def selectByCity(self, city):
        # view all restaurants in a given city
        self.cursor.execute('''SELECT * 
                            FROM Restaurant
                            WHERE Address LIKE %s
                            ''', (city,))
        # commit the changes
        self.cursor.commit()
