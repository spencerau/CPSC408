import tkinter as tk
import tkinter.font as tkFont
import mysql.connector
from restaurant import restaurant
from customer import customer
from transactions import transactions

class App:

    conn = mysql.connector.connect(host="localhost",
                                user="root",
                                password="cpsc408",
                                auth_plugin='mysql_native_paclssword')
                                #database="MadeInChinaYelp")
    
    #create cursor object
    cursor = conn.cursor()

    restaurant = restaurant(cursor)
    customer = customer(cursor)
    transactions = transactions(cursor)

    # create database and table objects
    def createDatabase(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS MadeInChinaYelp")
        self.cursor.execute("USE MadeInChinaYelp")
        self.restaurant.createTable()
        self.customer.createTable()
        self.transactions.createTables()
        self.conn.commit()

    def __init__(self, root):
        self.createDatabase()

        self.root = root  # store root as an instance variable so other methods can access it
        #setting title
        root.title("Made in China Yelp")
        #setting window size
        self.width=500
        self.height=435
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # create main menu buttons        
        RestMenu=tk.Button(root)
        RestMenu["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        RestMenu["font"] = ft
        RestMenu["fg"] = "#000000"
        RestMenu["justify"] = "center"
        RestMenu["text"] = "Restaurants"
        RestMenu.place(x=210,y=80,width=100,height=35)
        RestMenu["command"] = self.open_restaurants_menu

        CustMenu=tk.Button(root)
        CustMenu["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        CustMenu["font"] = ft
        CustMenu["fg"] = "#000000"
        CustMenu["justify"] = "center"
        CustMenu["text"] = "Customers"
        CustMenu.place(x=210,y=140,width=100,height=35)
        CustMenu["command"] = self.open_cust_menu

        OrdMenu=tk.Button(root)
        OrdMenu["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        OrdMenu["font"] = ft
        OrdMenu["fg"] = "#000000"
        OrdMenu["justify"] = "center"
        OrdMenu["text"] = "Orders"
        OrdMenu.place(x=210,y=200,width=100,height=35)
        OrdMenu["command"] = self.open_order_menu

        RevMenu=tk.Button(root)
        RevMenu["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        RevMenu["font"] = ft
        RevMenu["fg"] = "#000000"
        RevMenu["justify"] = "center"
        RevMenu["text"] = "Reviews"
        RevMenu.place(x=210,y=260,width=100,height=35)
        RevMenu["command"] = self.open_review_menu

        ReservMenu=tk.Button(root)
        ReservMenu["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        ReservMenu["font"] = ft
        ReservMenu["fg"] = "#000000"
        ReservMenu["justify"] = "center"
        ReservMenu["text"] = "Reservations"
        ReservMenu.place(x=210,y=320,width=100,height=35)
        ReservMenu["command"] = self.open_reserv_menu

    def open_restaurants_menu(self):
        self.create_new_window("Restaurants Menu", [self.viewRestMenu, addRestMenu, modifyRestMenu, self.delete(0)], "View Restaurants", "Add Restaurant", "Modify Restaurant", "Delete Restaurant")
        
        def addRestMenu(self):
            pass

        def modifyRestMenu(self):
            pass

    def viewRestMenu(self):
        self.create_new_window("View Restaurants", [self.viewByID(0), self.ViewAll(0), ViewByCity(0), self.ExportToCSV(0)], "View by ID", "View All", "View by City", "Export to CSV")
        
        def ViewByCity(self):
            query_window = tk.Toplevel()
            query_window.title("View by ID")

            # Label for ID entry
            id_label = tk.Label(query_window, text="Enter ID:")
            id_label.pack()

            # Entry widget to input ID
            city_entry = tk.Entry(query_window)
            city_entry.pack()

            # create a Text widget to display the results
            results_text = tk.Text(query_window)
            results_text.pack()

            def run_query():
                city = city_entry.get()
                # Perform query using the provided ID
                # Display the results
                results = self.restaurant.selectByCity(city)
                # Clear the Text widget
                results_text.delete('1.0', tk.END)
                # Insert the results into the Text widget
                for result in results:
                    results_text.insert(tk.END, f"{result}\n")

            # Button to run the query
            query_button = tk.Button(query_window, text="Run Query", command=run_query)
            query_button.pack()

    def open_cust_menu(self):
        self.create_new_window("Customers Menu", [self.viewCustMenu, addCustMenu, modifyCustMenu, self.delete(1)], "View Customer", "Add Customer", "Modify Customer", "Delete Customer")

        def addCustMenu(self):
            pass

        def modifyCustMenu(self):
            pass

    def viewCustMenu(self):
            self.create_new_window("View Customers", [self.viewByID(1), self.ViewAll(1), self.ExportToCSV(1)], "View by ID", "View All", "Export to CSV")

    def open_order_menu(self):
        self.create_new_window("Orders Menu", [self.viewOrderMenu, addOrderMenu, modifyOrderMenu, self.delete(2)], "View Orders", "Add Order", "Modify Order", "Delete Order")

        def addOrderMenu(self):
            pass

        def modifyOrderMenu(self):
            pass

    def viewOrderMenu(self):
        self.create_new_window("View Orders", [self.viewByID(2), self.viewTransByID(2, 1), self.viewTransByID(2, 0), self.ViewAll(2), self.ExportToCSV(2)], "View by ID", "View by Customer ID", "View by Restaurant ID", "View All", "Export to CSV")

    def open_review_menu(self):
        self.create_new_window("Reviews Menu", [self.viewReviewMenu, addReviewMenu, modifyReviewMenu, self.delete(3)], "View Reviews", "Add Review", "Modify Review", "Delete Review")

        def addReviewMenu(self):
            pass

        def modifyReviewMenu(self):
            pass
    
    def viewReviewMenu(self):
        self.create_new_window("View Reviews", [self.viewByID(3), self.viewTransByID(3, 1), self.viewTransByID(3, 0), self.ViewAll(3), self.ExportToCSV(3)], "View by ID", "View by Customer ID", "View by Restaurant ID", "View All", "Export to CSV")

    def open_reserv_menu(self):
        self.create_new_window("Reservations Menu", [self.viewReservMenu, addReservMenu, modifyReservMenu, self.delete(4)], "View Reservations", "Add Reservation", "Modify Reservation", "Delete Reservation")

        def addReservMenu(self):
            pass

        def modifyReservMenu(self):
            pass

    def viewReservMenu(self):
        self.create_new_window("View Reservations", [self.viewByID(4), self.viewTransByID(4, 1), self.viewTransByID(4, 0), self.ViewAll(4), self.ExportToCSV(4)], "View by ID", "View by Customer ID", "View by Restaurant ID", "View All", "Export to CSV")

    # table flag; 0 = Restaurant, 1 = Customer, 2 = orders, 3 = reviews, 4 = reservations
    def viewByID(self, table):
        query_window = tk.Toplevel()
        query_window.title("View by ID")

        # Label for ID entry
        id_label = tk.Label(query_window, text="Enter ID:")
        id_label.pack()

        # Entry widget to input ID
        id_entry = tk.Entry(query_window)
        id_entry.pack()

        # create a Text widget to display the results
        results_text = tk.Text(query_window)
        results_text.pack()

        def run_query():
            id_value = id_entry.get()
            # Perform query using the provided ID
            # Display the results
            if table == 0:
                results = self.restaurant.selectRestaurant(id_value)
            elif table == 1:
                results = self.customer.selectCustomer(id_value)
            elif table == 2:
                results = self.transactions.selectOrder(id_value)
            elif table == 3:
                results = self.transactions.selectReview(id_value)
            elif table == 4:
                results = self.transactions.selectReservation(id_value)
            else:
                print("Invalid table flag")
                return
            # Clear the Text widget
            results_text.delete('1.0', tk.END)
            # Insert the results into the Text widget
            for result in results:
                results_text.insert(tk.END, f"{result}\n")

        # Button to run the query
        query_button = tk.Button(query_window, text="Run Query", command=run_query)
        query_button.pack()
    
    # table flag: 2 = orders, 3 = reviews, 4 = reservations
    # if flag == 0 use restaurant table, if flag == 1 use customer table
    def viewTransByID(self, table, flag):
        query_window = tk.Toplevel()
        query_window.title("View by ID")

        # Label for ID entry
        id_label = tk.Label(query_window, text="Enter ID:")
        id_label.pack()

        # Entry widget to input ID
        id_entry = tk.Entry(query_window)
        id_entry.pack()

        # create a Text widget to display the results
        results_text = tk.Text(query_window)
        results_text.pack()

        def run_query():
            id_value = id_entry.get()
            # Perform query using the provided ID
            # Display the results
            if flag == 0:
                if table == 2:
                    results = self.transactions.selectOrdersByCustomer(id_value)
                elif table == 3:
                    results = self.transactions.selectReviewsByCustomer(id_value)
                elif table == 4:
                    results = self.transactions.selectReservationsByCustomer(id_value)
            elif flag == 1:
                if table == 2:
                    results = self.transactions.selectOrdersByRestaurant(id_value)
                elif table == 3:
                    results = self.transactions.selectReviewsByRestaurant(id_value)
                elif table == 4:
                    results = self.transactions.selectReservationsByRestaurant(id_value)
            # Clear the Text widget
            results_text.delete('1.0', tk.END)
            # Insert the results into the Text widget
            for result in results:
                results_text.insert(tk.END, f"{result}\n")

        # Button to run the query
        query_button = tk.Button(query_window, text="Run Query", command=run_query)
        query_button.pack()

    # table flag: 0 = Restaurant, 1 = Customer, 2 = orders, 3 = reviews, 4 = reservations
    def ViewAll(self, table):
        query_window = tk.Toplevel()
        query_window.title("View by ID")

        # Label for ID entry
        id_label = tk.Label(query_window, text="Enter ID:")
        id_label.pack()

        # Entry widget to input ID
        id_entry = tk.Entry(query_window)
        id_entry.pack()

        # create a Text widget to display the results
        results_text = tk.Text(query_window)
        results_text.pack()

        def run_query():
            id_value = id_entry.get()
            # Perform query using the provided ID
            # Display the results
            if table == 0:
                results = self.restaurant.selectAllRestaurants(id_value)
            elif table == 1:
                results = self.customer.selectAllCustomers(id_value)
            elif table == 2:
                results = self.transactions.selectAllOrders(id_value)
            elif table == 3:
                results = self.transactions.selectAllReviews(id_value)
            elif table == 4:
                results = self.transactions.selectAllReservations(id_value)
            else:
                print("Invalid table flag")
                return
            # Clear the Text widget
            results_text.delete('1.0', tk.END)
            # Insert the results into the Text widget
            for result in results:
                results_text.insert(tk.END, f"{result}\n")

        # Button to run the query
        query_button = tk.Button(query_window, text="Run Query", command=run_query)
        query_button.pack()

    # table flag: 0 = Restaurant, 1 = Customer, 2 = orders, 3 = reviews, 4 = reservations
    def ExportToCSV(self, table):
        pass

    # table flag = 0 = Restaurant, 1 = Customer, 2 = orders, 3 = reviews, 4 = reservations
    def modify(self, table):
        # get column names from table
        if (table == 0):
            type = "Restaurant"
        elif (table == 1):
            type = "Customer"
        elif (table == 2):
            type = "Orders"
        elif (table == 3):
            type = "Review"
        elif (table == 4):
            type = "Reservation"

        def get_column_names(self, type):
            # Execute SQL query to get column names of table
            query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{type}'"        
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            # Return list of column names
            return [x[0] for x in result]
        
        


    # table flag: 0 = Restaurant, 1 = Customer, 2 = orders, 3 = reviews, 4 = reservations
    def delete(self, table):
        pass

    def create_new_window(self, title, buttons, *button_texts):
        # create new window
        new_window = tk.Toplevel()
        new_window.title(title)
        
        # set properties of the new window as desired
        width = self.width
        height = self.height
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        new_window.geometry(alignstr)
        new_window.resizable(width=False, height=False)

        # create a "Back" button
        back_button = tk.Button(new_window, text="Back", command=lambda: self.show_root(new_window))
        back_button.place(x=10, y=10, width=50, height=25)
        
        # create the buttons
        for i, button_text in enumerate(button_texts):
            button = tk.Button(new_window, text=button_text, command=buttons[i])
            button.place(x=200, y=100 + i*60, width=120, height=35)
        
        # hide the root window
        self.root.withdraw()
        
        # show the new window
        new_window.mainloop()

    def show_root(self, window):
        # destroy the current window and show the root window
        window.destroy()
        self.root.deiconify()


root = tk.Tk()
app = App(root)
root.mainloop()
