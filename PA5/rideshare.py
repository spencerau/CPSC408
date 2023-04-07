# @author Spencer Au
# ID: 2385256
# spau@chapman.edu
# CPSC 408 - Section 2
# PA5 - Rideshare

import mysql.connector
import random


conn = mysql.connector.connect(host="localhost",
                               user="root",
                               password="cpsc408",
                               auth_plugin='mysql_native_password',
                               database="RideShare")

#create cursor object
cursor = conn.cursor()

# create the tables in MySQL
# Rider has the attributes of INTEGER userID, INTEGER lastRideID
# Driver has the attributes of INTEGER driverID, DOUBLE Rating, BOOL driverFlag
# Ride has the attributes of INT rideID, INT driverID, INT riderID, VARCHAR(20) startLoc, INTEGER endLoc
def createTable():
    # check if the table already exists
    cursor.execute("SHOW TABLES LIKE 'Rider'")
    if cursor.fetchone() is None:
        # create the Rider table
        query1 = '''
            CREATE TABLE Rider(
            userID INTEGER NOT NULL PRIMARY KEY, 
            lastRideID INTEGER
            );
        '''
        cursor.execute(query1)
        print("Rider Table Created")

    cursor.execute("SHOW TABLES LIKE 'Driver'")
    if cursor.fetchone() is None:
    # create the Driver table
        query2 = '''
            CREATE TABLE Driver(
            driverID INT NOT NULL PRIMARY KEY, 
            rating DOUBLE, 
            driverFlag BOOL
            );
        '''
        cursor.execute(query2)
        print("Driver Table Created")

    cursor.execute("SHOW TABLES LIKE 'Ride'")
    if cursor.fetchone() is None:
        # create the Ride table
        query3 = '''
        CREATE TABLE Ride(
            rideID INT NOT NULL PRIMARY KEY, 
            driverID INT NOT NULL, 
            riderID INT NOT NULL, 
            startLoc VARCHAR(20), 
            endLoc VARCHAR(20)
            );
        '''
        cursor.execute(query3)
        print("Ride Table Created")

# checks if the user is a rider or driver and if the id is valid
def checkUser():
    validID = False
    while (not validID):
        print("Enter in your ID")
        id = input()
        # check if the user is a rider or driver
        query = '''
        SELECT * FROM Rider WHERE userID = %s;
        '''
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        while cursor.nextset():
            pass

        if result is not None:
            print("You are a rider")
            validID = True
            return id, 0
        else:
            query = '''
            SELECT * FROM Driver WHERE driverID = %s;
            '''
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            while cursor.nextset():
                pass
            if result is not None:
                print("You are a driver")
                validID = True
                return id, 1
            else:
                print("Error: User not found")
                print("Please enter a valid ID")

# creates a new user, prompting user to choose between rider or driver
def newUser(id):
    # change so that it checks user/driver table for the id generated
    userType = -1
    print("Do you want to create a User or Driver account? U/D")
    choice = input().lower()
    if choice == 'u':
        # insert the new user into the Rider table
        cursor.execute('''
        INSERT INTO Rider VALUES(%s, NULL);
        ''', (id,))
        conn.commit()
        userType = 0
        print("User Created")
        return 0
    elif choice == 'd':
        # insert the new driver into the Driver table
        cursor.execute('''
        INSERT INTO Driver VALUES(%s, %s, TRUE);
        ''', (id, 5.0,))
        conn.commit()
        userType = 1
        print("Driver Created")
        return 1
    else:
        print("Error: Invalid Input")
    return userType

# runs the user interface for a rider
def runUser(id):
    cont = True
    while (cont):
        print("1. View Ride History")
        print("2. Find a Ride")
        print("3. Rate your Driver")
        print("4. Exit")
        choice = input()
        if choice == '1':
            viewRideHistory(id, 0)
        elif choice == '2':
            requestRide(id)
        elif choice == '3':
            rateDriver(id)
        elif choice == '4':
            print("Goodbye")
            cont = False
            break

# shows the ride history of the user
def viewRideHistory(id, userType):
    # userType = 0 for rider
    if userType == 0:
        query = '''
        SELECT *
        FROM Ride
        WHERE riderID = %s;
        '''
    elif userType == 1:
        query = '''
        SELECT *
        FROM Ride
        WHERE driverID = %s;
        '''
    cursor.execute(query, (id,))
    result = cursor.fetchall()
    if result is not None:
        print("Ride History:")
        print("RideID\tDriverID\tRiderID\tStartLoc\tEndLoc")
        for row in result:
            print(row)
    else:
        print("No rides found")

# requests a ride for a rider user
def requestRide(id):
    print("Enter in your pickup location")
    startLoc = input()
    print("Enter in your destination")
    endLoc = input()
    # check if there are any available drivers
    query = '''
    SELECT *
    FROM Driver
    WHERE driverFlag = TRUE
    ORDER BY RAND()
    LIMIT 1;
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    while cursor.nextset():
        pass

    if result is not None:
        # generate a random integer between 10000 and 99999 (inclusive)
        rideID = random.randint(10000, 99999)
        # insert the ride into the Ride table
        query = '''
        INSERT INTO Ride VALUES(%s, %s, %s, %s, %s);
        '''
        print("Your Driver ID is " + str(result[0]))
        print("Your Ride ID is " + str(rideID))
        cursor.execute(query, (rideID, result[0], id, startLoc, endLoc))
        
        conn.commit()
        print("Ride Requested")

        # update the rider's lastRideID
        query = '''
        UPDATE Rider
        SET lastRideID = %s
        WHERE userID = %s;
        '''
        cursor.execute(query, (rideID, id))
        conn.commit()
    else:
        print("No drivers available")

# Rate my driver:
# i. You will look up the rider’s last ride and get the driver’s ID
# ii. You will then print this information to the user and ask if it is the correct ride
# iii. If it is not the correct ride, you will have them enter the rideID of the ride
# they want to rate and confirm that information.
# iv. Then, calculate the driver’s new rating by taking their current rating +
# their new rating and dividing by 2.
def rateDriver(id):
    query = '''
    SELECT *
    FROM Rider
    WHERE userID = %s;
    '''
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    while cursor.nextset():
        pass

    if result is not None:
        # get the last rideID
        rideID = result[1]
        # get the driverID
        query = '''
        SELECT driverID
        FROM Ride
        WHERE rideID = %s;
        '''
        cursor.execute(query, (rideID,))
        result = cursor.fetchone()
        driverID = result[0]
        while cursor.nextset():
            pass

        print("Your last ride was with driver " + str(driverID))
        print("Is this correct? Y/N")
        choice = input().lower()
        if choice == 'n':
            print("Enter in the rideID of the ride you want to rate")
            rideID = input()
            # get the driverID
            query = '''
            SELECT driverID
            FROM Ride
            WHERE rideID = %s;
            '''
            cursor.execute(query, (rideID,))
            result = cursor.fetchone()
            driverID = result[0]
            while cursor.nextset():
                pass

        # get the driver's rating
        query = '''
        SELECT *
        FROM Driver
        WHERE driverID = %s;
        '''
        cursor.execute(query, (driverID,))
        result = cursor.fetchone()
        while cursor.nextset():
            pass

        if result is not None:
            driverID = result[0]
            print("Enter in your rating for the driver")
            rating = input()
            # update the driver's rating
            query = '''
            UPDATE Driver
            SET rating = %s
            WHERE driverID = %s;
            '''
            oldRating = float(result[1])
            inputRating = float(rating)
            rating = (inputRating + oldRating) /2
            cursor.execute(query, (rating, driverID))
            conn.commit()
            print("Rating submitted")
        else:
            print("No rides found")

# runs the user interface for a driver
def runDriver(id):
    cont = True
    while (cont):
        print("1. View Rating")
        print("2. View Ride History")
        print("3. Activate/Deactivate Driver Mode")
        print("4. Exit")
        choice = input()
        if choice == '1':
            viewRating(id)
        elif choice == '2':
            viewRideHistory(id, 1)
        elif choice == '3':
            changeDriverMode(id)
        elif choice == '4':
            print("Goodbye")
            cont = False
            break

# shows the rating of the driver
def viewRating(id):
    query = '''
    SELECT rating
    FROM Driver
    WHERE driverID = %s;
    '''
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    while cursor.nextset():
        pass
    if result is not None:
        print("Your rating is: " + str(result[0]))
    else:
        print("No rating found")

# changes the driver mode of the driver
def changeDriverMode(id):
    query = '''
    SELECT driverFlag
    FROM Driver
    WHERE driverID = %s;
    '''
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    while cursor.nextset():
        pass

    if result is not None:
        if result[0] == 1:
            query = '''
            UPDATE Driver
            SET driverFlag = FALSE
            WHERE driverID = %s;
            '''
            cursor.execute(query, (id,))
            conn.commit()
            print("Driver Mode Deactivated")
        else:
            query = '''
            UPDATE Driver
            SET driverFlag = TRUE
            WHERE driverID = %s;
            '''
            cursor.execute(query, (id,))
            conn.commit()
            print("Driver Mode Activated")
    else:
        print("Error: Driver not found")


def main():
    # check if tables already exist
    # if not, create them
    createTable()
    id = -1
    # flag that determines if the user is a rider or driver
    # 0 = rider, 1 = driver
    userType = -1
    print("Welcome to RideShare")
    print("Are you a new user? Y/N")
    choice = input().lower()
    if choice == 'y':
        # generate a random integer between 10000 and 99999 (inclusive)
        id = random.randint(10000, 99999)
        userType = newUser(id)
    elif choice == 'n':
        id, userType = checkUser()
        
    print("What would you like to do?")
    #print("Value of UserType: " + str(userType))
    # rider
    if (userType == 0):
        runUser(id)
    # driver
    elif (userType == 1):
        runDriver(id)
            
main()

#requestRide(77689)

#viewRideHistory(77689, 0)

#rateDriver(77689)

#viewRating(97831)

#changeDriverMode(97831)


        