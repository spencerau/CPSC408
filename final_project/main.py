from tkinter import * 
import mysql.connector
from mysql.connector import errorcode
from restaurant import restaurant
from customer import customer
from transactions import transactions


conn = mysql.connector.connect(host="localhost",
                                user="root",
                                password="cpsc408",
                                auth_plugin='mysql_native_password',
                                database="MadeInChinaYelp")
    
#create cursor object
cursor = conn.cursor()

restaurant = restaurant(cursor)
customer = customer(cursor)
transactions = transactions(cursor)

def createTables():
    restaurant.createTable()
    customer.createTable()
    transactions.createTables()

# add a new restaurant option is chose in TKinter GUI
def addRestaurant():
    pass

def main():
    createTables()
