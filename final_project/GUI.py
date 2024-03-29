import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont
import mysql.connector
from restaurant import restaurant
from customer import customer
from transactions import transactions
import csv
import os


class App:

    conn = mysql.connector.connect(host="localhost",
                                user="root",
                                password="cpsc408",
                                auth_plugin='mysql_native_password')
                                #database="MadeInChinaYelp")
    
    #create cursor object
    cursor = conn.cursor()

    restaurant = restaurant(cursor, conn)
    customer = customer(cursor, conn)
    transactions = transactions(cursor, conn)

    new_window = None  # initialize new_window to None
    prev_window = None  # initialize prev_window to None


    # create database and table objects
    def createDatabase(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS MadeInChinaYelp")
        self.cursor.execute("USE MadeInChinaYelp")
        self.restaurant.createTable()
        self.restaurant.createViews()
        self.restaurant.createIndex()
        self.customer.createTable()
        self.customer.createViews()
        self.transactions.createTables()
        self.transactions.createViews()
        self.conn.commit()


    def __init__(self, root):
        self.createDatabase()

        self.root = root  # store root as an instance variable so other methods can access it
        #setting title
        root.title("Made in China Yelp")
        #setting window size
        self.width=500
        self.height=500
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
        RestMenu.place(x=210,y=20,width=100,height=35)
        RestMenu["command"] = self.open_restaurants_menu

        CustMenu=tk.Button(root)
        CustMenu["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        CustMenu["font"] = ft
        CustMenu["fg"] = "#000000"
        CustMenu["justify"] = "center"
        CustMenu["text"] = "Customers"
        CustMenu.place(x=210,y=80,width=100,height=35)
        CustMenu["command"] = self.open_cust_menu

        OrdMenu=tk.Button(root)
        OrdMenu["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        OrdMenu["font"] = ft
        OrdMenu["fg"] = "#000000"
        OrdMenu["justify"] = "center"
        OrdMenu["text"] = "Orders"
        OrdMenu.place(x=210,y=140,width=100,height=35)
        OrdMenu["command"] = self.open_order_menu

        RevMenu=tk.Button(root)
        RevMenu["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        RevMenu["font"] = ft
        RevMenu["fg"] = "#000000"
        RevMenu["justify"] = "center"
        RevMenu["text"] = "Reviews"
        RevMenu.place(x=210,y=200,width=100,height=35)
        RevMenu["command"] = self.open_review_menu

        ReservMenu=tk.Button(root)
        ReservMenu["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        ReservMenu["font"] = ft
        ReservMenu["fg"] = "#000000"
        ReservMenu["justify"] = "center"
        ReservMenu["text"] = "Reservations"
        ReservMenu.place(x=210,y=260,width=100,height=35)
        ReservMenu["command"] = self.open_reserv_menu

        # create a button for this One query must perform an aggregation/group-by clause
        # the button returns the average price for each restaurant, calling the ViewAvgPrice function
        AvgPrice=tk.Button(root)
        AvgPrice["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        AvgPrice["font"] = ft
        AvgPrice["fg"] = "#000000"
        AvgPrice["justify"] = "center"
        AvgPrice["text"] = "Get Num Orders by Restaurant"
        AvgPrice.place(x=140,y=320,width=230,height=35)
        AvgPrice["command"] = self.getOrdersByRestaurant

        # create a button for this Two queries must involve joins across at least 3 tables
        # calls findWeebs() and the button is located to the rigth of the Query 8 button
        AvgPrice=tk.Button(root)    
        AvgPrice["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        AvgPrice["font"] = ft
        AvgPrice["fg"] = "#000000"
        AvgPrice["justify"] = "center"
        AvgPrice["text"] = "Find New Restaurant by Culture"
        AvgPrice.place(x=140,y=380,width=230,height=35)
        AvgPrice["command"] = self.findByCulture

        AvgPrice=tk.Button(root)    
        AvgPrice["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        AvgPrice["font"] = ft
        AvgPrice["fg"] = "#000000"
        AvgPrice["justify"] = "center"
        AvgPrice["text"] = "Export All Data to CSV"
        AvgPrice.place(x=140,y=440,width=230,height=35)
        AvgPrice["command"] = self.ExportToCSV


    def findByCulture(self):
        query_window = tk.Toplevel()
        query_window.title("Try New Restaurants By Culture")

        # Label for ID entry
        id_label = tk.Label(query_window, text="Enter Customer ID:")
        id_label.pack()
        # Entry widget to input ID
        id_entry = tk.Entry(query_window)
        id_entry.pack()

        # Label for Culture entry
        culture_label = tk.Label(query_window, text="Enter Culture:")
        culture_label.pack()
        # Entry widget to input Culture
        culture_entry = tk.Entry(query_window)
        culture_entry.pack()

        # create a Treeview widget to display the results
        results_treeview = ttk.Treeview(query_window, show='headings')
        results_treeview.pack()

        # set properties of the new window as desired
        width = self.width * 2
        height = self.height * 2
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        query_window.geometry(alignstr)
        query_window.resizable(width=False, height=False)

        # create a "Back" button
        back_button = tk.Button(query_window, text="Back", command=lambda: self.show_root(query_window))
        back_button.place(x=10, y=10, width=50, height=25)

        # hide the root window
        self.root.withdraw()

        def run_query():
            id_value = id_entry.get()
            culture_value = culture_entry.get()
            # Perform query using the provided ID
            results = self.restaurant.findNewByCulture(id_value, culture_value)
            
            # Get the column names from the result set
            columns = [desc[0] for desc in self.transactions.cursor.description]

            # Clear the Treeview
            results_treeview.delete(*results_treeview.get_children())

            # Insert the columns into the Treeview
            results_treeview['columns'] = columns
            for col in columns:
                results_treeview.column(col, width=150)
                results_treeview.heading(col, text=col)

            # Insert the results into the Treeview
            for result in results:
                results_treeview.insert("", "end", values=result)

        # Button to run the query
        query_button = tk.Button(query_window, text="Run Query", command=run_query)
        query_button.pack()
        
        # create a "Back" button
        back_button = tk.Button(query_window, text="Back", command=lambda: self.show_root(query_window))
        back_button.pack(anchor='nw')

        # hide the previous window
        self.root.withdraw()
        

    def getOrdersByRestaurant(self):
        query_window = tk.Toplevel()
        query_window.title("View Number Orders by Restaurant")
         # create a Treeview widget to display the results
        results_treeview = ttk.Treeview(query_window, show='headings')
        results_treeview.pack()

        # set properties of the new window as desired
        width = self.width * 2
        height = self.height * 2
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        query_window.geometry(alignstr)
        query_window.resizable(width=False, height=False)

        # create a "Back" button
        back_button = tk.Button(query_window, text="Back", command=lambda: self.show_root(query_window))
        back_button.place(x=10, y=10, width=50, height=25)

        # hide the root window
        self.root.withdraw()

        # Perform query using the provided ID
        results = self.restaurant.getOrders()
        
        # Get the column names from the result set
        columns = [desc[0] for desc in self.transactions.cursor.description]

        # Clear the Treeview
        results_treeview.delete(*results_treeview.get_children())

        # Insert the columns into the Treeview
        results_treeview['columns'] = columns
        for col in columns:
            results_treeview.column(col, width=150)
            results_treeview.heading(col, text=col)

        # Insert the results into the Treeview
        for result in results:
            results_treeview.insert("", "end", values=result)


    def ExportToCSV(self):
        # Get the current directory path
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the CSV file path
        csv_file_path = os.path.join(current_directory, 'restaurant_data.csv')
        # Get the list of table names in the database
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()

        # Iterate over the table names
        for table in tables:
            table_name = table[0]
            # Construct the CSV file path for each table
            csv_file_path = os.path.join(current_directory, f'{table_name}.csv')

            # Execute the SQL query to fetch the data from the table
            query = f"SELECT * FROM {table_name}"
            self.cursor.execute(query)

            # Fetch all the rows returned by the query
            rows = self.cursor.fetchall()

            # Open the CSV file in write mode
            with open(csv_file_path, 'w', newline='') as csv_file:
                # Create a CSV writer object
                csv_writer = csv.writer(csv_file)

                # Write the column headers
                column_names = [desc[0] for desc in self.cursor.description]
                csv_writer.writerow(column_names)

                # Write the data rows
                csv_writer.writerows(rows)


    def searchByName(self):
        query_window = tk.Toplevel()
        query_window.title("Search Restaurants By Name")

        # Label for Name entry
        name_label = tk.Label(query_window, text="Enter Restaurant Name:")
        name_label.pack()
        # Entry widget to input Name
        name_entry = tk.Entry(query_window)
        name_entry.pack()

        # create a Treeview widget to display the results
        results_treeview = ttk.Treeview(query_window, show='headings')
        results_treeview.pack()

        # set properties of the new window as desired
        width = self.width * 2
        height = self.height * 2
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        query_window.geometry(alignstr)
        query_window.resizable(width=False, height=False)

        # create a "Back" button
        back_button = tk.Button(query_window, text="Back", command=lambda: self.show_root(query_window))
        back_button.place(x=10, y=10, width=50, height=25)

        # hide the root window
        self.root.withdraw()

        def run_query():
            name = name_entry.get()
            # Perform query using the provided ID
            results = self.restaurant.selectByName(name)
            
            # Get the column names from the result set
            columns = [desc[0] for desc in self.transactions.cursor.description]

            # Clear the Treeview
            results_treeview.delete(*results_treeview.get_children())

            # Insert the columns into the Treeview
            results_treeview['columns'] = columns
            for col in columns:
                results_treeview.column(col, width=150)
                results_treeview.heading(col, text=col)

            # Insert the results into the Treeview
            for result in results:
                results_treeview.insert("", "end", values=result)

        # Button to run the query
        query_button = tk.Button(query_window, text="Run Query", command=run_query)
        query_button.pack()

        # hide the previous window
        self.root.withdraw()


    def open_restaurants_menu(self):
        self.create_new_window("Restaurants Menu", 
                               [self.viewRestMenu, self.add_restaurant_window, lambda: self.modify(0), lambda: self.delete(0)], 
                               "View Restaurants", "Add Restaurant", "Modify Restaurant", "Delete Restaurant")

    def viewRestMenu(self):
        self.create_new_window("View Restaurants", 
                               [lambda: self.viewByID(0), lambda: self.ViewAll(0), lambda: self.searchByName()], 
                               "View by ID", "View All", "Search by Name")
        

    def open_cust_menu(self):
        self.create_new_window("Customers Menu", 
                               [self.viewCustMenu, self.add_customer_window, lambda: self.modify(1), lambda: self.delete(1)], 
                               "View Customer", "Add Customer", "Modify Customer", "Delete Customer")

    def viewCustMenu(self):
            self.create_new_window("View Customers", 
                                   [lambda: self.viewByID(1), lambda: self.ViewAll(1)], 
                                   "View by ID", "View All")


    def open_order_menu(self):
        self.create_new_window("Orders Menu", 
                               [self.viewOrderMenu, lambda: self.add("Orders"), lambda: self.modify(2), lambda: self.delete(2)], 
                               "View Orders", "Add Order", "Modify Order", "Delete Order")

    def viewOrderMenu(self):
        self.create_new_window("View Orders", 
                               [lambda: self.viewByID(2), lambda: self.viewTransByID(2, 1), lambda: self.viewTransByID(2, 0), 
                                lambda: self.ViewAll(2)], 
                               "View by ID", "View by C_ID", "View by R_ID", "View All")


    def open_review_menu(self):
        self.create_new_window("Reviews Menu", 
                               [self.viewReviewMenu, lambda: self.add("Review"), lambda: self.modify(3), lambda: self.delete(3)], 
                               "View Reviews", "Add Review", "Modify Review", "Delete Review")

    def viewReviewMenu(self):
        self.create_new_window("View Reviews", 
                                [lambda: self.viewByID(3), lambda: self.viewTransByID(3, 1), lambda: self.viewTransByID(3, 0), 
                                lambda: self.ViewAll(3)],
                                "View by ID", "View by C_ID", "View by R_ID", "View All")


    def open_reserv_menu(self):
        self.create_new_window("Reservations Menu", 
                               [self.viewReservMenu, lambda: self.add("Reservation"), lambda: self.modify(4), lambda: self.delete(4)], 
                               "View Reservations", "Add Reservation", "Modify Reservation", "Delete Reservation")

    def viewReservMenu(self):
        self.create_new_window("View Reservations", 
                               [lambda: self.viewByID(4), lambda: self.viewTransByID(4, 1), lambda: self.viewTransByID(4, 0), 
                                lambda: self.ViewAll(4)], 
                               "View by ID", "View by C_ID", "View by R_ID", "View All")


    # table flag; 0 = Restaurant, 1 = Customer, 2 = orders, 3 = reviews, 4 = reservations
    def viewByID(self, table):
        query_window = tk.Toplevel()
        if (table == 0):
            query_window.title("View Restaurant by ID")
        elif (table == 1):
            query_window.title("View Customer by ID")
        elif (table == 2):
            query_window.title("View Order by ID")
        elif (table == 3):
            query_window.title("View Review by ID")
        elif (table == 4):
            query_window.title("View Reservation by ID")

        # Label for ID entry
        id_label = tk.Label(query_window, text="Enter ID:")
        id_label.pack()

        # Entry widget to input ID
        id_entry = tk.Entry(query_window)
        id_entry.pack()

        # create a Treeview widget to display the results
        results_treeview = ttk.Treeview(query_window, show='headings')
        results_treeview.pack()

        # set properties of the new window as desired
        width = self.width * 2
        height = self.height * 2
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        query_window.geometry(alignstr)
        query_window.resizable(width=False, height=False)

        # create a "Back" button
        back_button = tk.Button(query_window, text="Back", command=lambda: self.show_root(query_window))
        back_button.place(x=10, y=10, width=50, height=25)

        # hide the root window
        self.root.withdraw()

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
            
            # Get the column names from the result set
            columns = [desc[0] for desc in self.transactions.cursor.description]

            # Clear the Treeview
            results_treeview.delete(*results_treeview.get_children())

            # Insert the columns into the Treeview
            results_treeview['columns'] = columns
            for col in columns:
                results_treeview.column(col, width=150)
                results_treeview.heading(col, text=col)

            # Insert the results into the Treeview
            for result in results:
                results_treeview.insert("", "end", values=result)

        # Button to run the query
        query_button = tk.Button(query_window, text="Run Query", command=run_query)
        query_button.pack()
    

    # table flag: 2 = orders, 3 = reviews, 4 = reservations
    # if flag == 0 use restaurant table, if flag == 1 use customer table
    def viewTransByID(self, table, flag):
        query_window = tk.Toplevel()
        if (table == 2):
            if (flag == 0):
                query_window.title("View Orders by RestaurantID")
            elif (flag == 1):
                query_window.title("View Orders by CustomerID")
        elif (table == 3):
            if (flag == 0):
                query_window.title("View Reviews by RestaurantID")
            elif (flag == 1):
                query_window.title("View Reviews by CustomerID")
        elif (table == 4):
            if (flag == 0):
                query_window.title("View Reservations by RestaurantID")
            elif (flag == 1):
                query_window.title("View Reservations by CustomerID")

        # set properties of the new window as desired
        width = self.width * 2
        height = self.height * 2
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        query_window.geometry(alignstr)
        query_window.resizable(width=False, height=False)

        # create a "Back" button
        back_button = tk.Button(query_window, text="Back", command=lambda: self.show_root(query_window))
        back_button.place(x=10, y=10, width=50, height=25)

        # hide the root window
        self.root.withdraw()

        # Label for ID entry
        id_label = tk.Label(query_window, text="Enter ID:")
        id_label.pack()

        # Entry widget to input ID
        id_entry = tk.Entry(query_window)
        id_entry.pack()

        # create a Text widget to display the results
        results_treeview = ttk.Treeview(query_window, show='headings')
        results_treeview.pack()

        def run_query():
            id_value = id_entry.get()
            # Perform query using the provided ID
            # Display the results
            if flag == 1:
                if table == 2:
                    results = self.transactions.selectOrdersByCustomer(id_value)
                elif table == 3:
                    results = self.transactions.selectReviewsByCustomer(id_value)
                elif table == 4:
                    results = self.transactions.selectReservationsByCustomer(id_value)
            elif flag == 0:
                if table == 2:
                    results = self.transactions.selectOrdersByRestaurant(id_value)
                elif table == 3:
                    results = self.transactions.selectReviewsByRestaurant(id_value)
                elif table == 4:
                    results = self.transactions.selectReservationsByRestaurant(id_value)
            # Get the column names from the result set
            columns = [desc[0] for desc in self.transactions.cursor.description]

            # Clear the Treeview
            results_treeview.delete(*results_treeview.get_children())

            # Insert the columns into the Treeview
            results_treeview['columns'] = columns
            for col in columns:
                results_treeview.column(col, width=150)
                results_treeview.heading(col, text=col)

            # Insert the results into the Treeview
            for result in results:
                results_treeview.insert("", "end", values=result)

        # Button to run the query
        query_button = tk.Button(query_window, text="Run Query", command=run_query)
        query_button.pack()


    # table flag: 0 = Restaurant, 1 = Customer, 2 = orders, 3 = reviews, 4 = reservations
    def ViewAll(self, table):
        query_window = tk.Toplevel()
        if (table == 0):
            query_window.title("View All Restaurants")
        elif (table == 1):
            query_window.title("View All Customers")
        elif (table == 2):
            query_window.title("View All Orders")
        elif (table == 3):
            query_window.title("View All Reviews")
        elif (table == 4):
            query_window.title("View All Reservations")

        # set properties of the new window as desired
        width = self.width * 2
        height = self.height * 2
        screenwidth = query_window.winfo_screenwidth()
        screenheight = query_window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        query_window.geometry(alignstr)
        query_window.resizable(width=False, height=False)

        # create a "Back" button
        back_button = tk.Button(query_window, text="Back", command=lambda: self.show_root(query_window))
        back_button.pack(anchor='nw')

        # create a Treeview widget to display the results
        results_treeview = ttk.Treeview(query_window, show='headings')
        results_treeview["height"] = 100
        results_treeview.pack()

        # hide the previous window
        self.prev_window.withdraw()

        #id_value = id_entry.get()
        # Perform query using the provided ID
        # Display the results
        if table == 0:
            results = self.restaurant.selectAllRestaurants()
        elif table == 1:
            results = self.customer.selectAllCustomers()
        elif table == 2:
            results = self.transactions.selectAllOrders()
        elif table == 3:
            results = self.transactions.selectAllReviews()
        elif table == 4:
            results = self.transactions.selectAllReservations()
        else:
            print("Invalid table flag")
            return
        
        # Get the column names from the result set
        columns = [desc[0] for desc in self.transactions.cursor.description]

        # Clear the Treeview
        results_treeview.delete(*results_treeview.get_children())

        # Insert the columns into the Treeview
        results_treeview['columns'] = columns
        for col in columns:
            results_treeview.column(col, width=150)
            results_treeview.heading(col, text=col)

        # Insert the results into the Treeview
        for result in results:
            results_treeview.insert("", "end", values=result)


    def add(self, table_name):
        # Get the column names for the specified table
        cursor = self.cursor
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [row[0] for row in cursor.fetchall()]

        # Create the window
        window = tk.Toplevel()
        window.title(f'Add {table_name.capitalize()}')

        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        window.geometry(alignstr)
        window.resizable(width=False, height=False)

        # Create a "Back" button
        back_button = tk.Button(window, text="Back", command=lambda: self.show_root(window))
        back_button.grid(row=0, column=0, sticky="nw")

        # hide the previous window
        #self.prev_window.withdraw()

        # Define a list of excluded column names
        excluded_columns = []
        if table_name == 'Orders':
            excluded_columns = ['Date', 'Time']

        # Remove the excluded columns from the list of columns
        columns = [col for col in columns if col not in excluded_columns]

        # Create the labels and entry boxes
        entries = []
        for i, column in enumerate(columns):
            if (i != 0):
                tk.Label(window, text=column.capitalize()).grid(row=i, column=0)
                entry = tk.Entry(window)
                entry.grid(row=i, column=1)
                entries.append(entry)

        # Function to submit new row to database
        def submit():
            values = []
            for entry in entries:
                values.append(entry.get())
            if table_name == 'Orders':
                transactions.insertOrder(self, *values)
            elif table_name == 'Review':
                transactions.insertReview(self, *values)
            elif table_name == 'Reservation':
                transactions.insertReservation(self, *values)
            window.destroy()
        
        # Create submit button
        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.grid(row=len(entries)+1, columnspan=2)

        # Hide the calling window
        self.root.withdraw()

        # Start the window
        window.protocol('WM_DELETE_WINDOW', lambda: self.root.deiconify())  # Show the calling window if the user clicks 'X'
        window.mainloop()


    def add_restaurant_window(self):
        # Create the window
        window = tk.Toplevel()
        window.title('Add Restaurant')

        # Set the new window size
        screenwidth = int(self.width * 1.5)
        screenheight = int(self.height * 1.5)
        x = (root.winfo_screenwidth() - screenwidth) // 2
        y = (root.winfo_screenheight() - screenheight) // 2
        alignstr = f"{screenwidth}x{screenheight}+{x}+{y}"
        window.geometry(alignstr)
        window.resizable(width=False, height=False)

        # Create a "Back" button
        #back_button = tk.Button(window, text="Back", command=lambda: self.show_root(window))
        #back_button.grid(row=0, column=0, sticky="nw")

        # hide the previous window
        #self.prev_window.withdraw()

        # Get the columns from the Restaurant table and exclude the excluded columns
        #self.cursor.execute(f"DESCRIBE Restaurant")
        # Get the column names for Restaurant and Specialty tables
        self.cursor.execute('''SELECT column_name
                            FROM information_schema.columns
                            WHERE table_name = 'Restaurant' OR table_name = 'Specialty' ''')
        columns = [row[0] for row in self.cursor.fetchall()]
        self.cursor.fetchall()

        # Define a list of excluded column names
        excluded_columns = ['RestaurantID', 'Score', 'Specialty_ID', 'SpecialtyID']

        # Remove the excluded columns from the list of columns
        columns = [col for col in columns if col not in excluded_columns]

        columns = ['Price'] + [col for col in columns if col not in excluded_columns and col != 'Price']
        columns = ['Name'] + [col for col in columns if col not in excluded_columns and col != 'Name']

        rest_entries = {}
        for i, col in enumerate(columns):
            tk.Label(window, text=col).grid(row=i, column=0)
            if col == 'Price':
                entry = tk.StringVar(window)
                entry.set('1')
                price_options = ['1', '2', '3', '4', '5']
                rest_dropdown = tk.OptionMenu(window, entry, *price_options)
                rest_dropdown.grid(row=i, column=1)
                rest_entries[col] = entry
            else:
                tk.Label(window, text=col).grid(row=i, column=0)
                entry = tk.Entry(window, name=f'{col.lower()}_entry')
                entry.grid(row=i, column=1)
                rest_entries[col] = entry

        # Create the 'Add Restaurant' button
        def add_restaurant():
            # insert a new operating table row
            #op_time_id = restaurant.insertOperatingTime(times)
            # insert a new specialty table row
            #specialty_id = restaurant.insertSpecialty(food[0], food[1])
            # insert a new restaurant table row

            rest_values = {}
            for col, entry in rest_entries.items():
                rest_values[col] = entry.get()

            name = rest_values['Name']
            price = rest_values['Price']
            address = rest_values['Address']
            website = rest_values['Website']
            specialty = rest_values['Specialty']
            culture = rest_values['Culture']
            specialtyID = restaurant.insertSpecialty(self, specialty, culture)

            rest_id = restaurant.insertRestaurant(self, name, price, address, website, specialtyID)

            window.destroy()

        add_button = tk.Button(window, text='Add Restaurant', command=add_restaurant)
        #add_button.grid(row=len(columns)+len(op_time_columns)+len(food_columns)+2, column=0, columnspan=2)
        add_button.grid(row=len(columns), column=0, columnspan=2)

        
    def add_customer_window(self):
        # Create the window
        window = tk.Toplevel()
        window.title('Add Customer')

        add_customer_width = 500
        add_customer_height = 300

        # Set the new window size
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = f"{add_customer_width}x{add_customer_height}+{int((screenwidth - add_customer_width) / 2)}+{int((screenheight - add_customer_height) / 2)}"
        window.geometry(alignstr)
        window.resizable(width=False, height=False)

        # Create a "Back" button
        #back_button = tk.Button(window, text="Back", command=lambda: self.show_root(window))
        #back_button.grid(row=0, column=0, sticky="nw")

        # hide the previous window
        #self.prev_window.withdraw()

        # Get the columns from the Customer table and exclude the excluded columns
        self.cursor.execute(f"DESCRIBE Customer")
        columns = [row[0] for row in self.cursor.fetchall()]

        # Define a list of excluded column names
        excluded_columns = ['CustomerID', 'NumVisits']

        # Remove the excluded columns from the list of columns
        columns = [col for col in columns if col not in excluded_columns]

        # Create the labels and entry boxes for the Customer table
        customer_entries = {}
        for i, col in enumerate(columns):
            tk.Label(window, text=col).grid(row=i, column=0)
            entry = tk.Entry(window, name=f'{col.lower()}_entry')
            entry.grid(row=i, column=1)
            customer_entries[col] = entry

        # Create the 'Add Customer' button
        def add_customer():
            # Get the values from the customer entries
            cust_values = {}
            for col, entry in customer_entries.items():
                cust_values[col] = entry.get()

            name = cust_values['Name']
            email = cust_values['Email']
            addr = cust_values['Address']

            # Insert the new customer and restaurant into the database
            customer_id = customer.insertCustomer(self, name, email, addr)
            
            # Close the window
            window.destroy()

        add_button = tk.Button(window, text='Add Customer', command=add_customer)
        add_button.grid(row=4, column=0, columnspan=2)


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
            query = f'''SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{type}' AND COLUMN_KEY = ''
            '''
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            # Return list of column names
            return [x[0] for x in result]
        
        mod = tk.Toplevel()
        mod.title("Modify")

        # set properties of the new window as desired
        width = self.width
        height = self.height
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        mod.geometry(alignstr)
        mod.resizable(width=False, height=False)

        # create a "Back" button
        back_button = tk.Button(mod, text="Back", command=lambda: self.show_root(mod))
        #back_button.place(x=10, y=10, width=50, height=25)
        back_button.pack(anchor='nw')

        # hide the previous window
        #self.prev_window.withdraw()

        # Label for ID entry
        id_label = tk.Label(mod, text="Enter ID:")
        id_label.pack()

        # Entry widget to input ID
        id_entry = tk.Entry(mod)
        id_entry.pack()

        # create drop down list of column names
        column_names = get_column_names(self, type)
        column_var = tk.StringVar(mod)
        column_var.set(column_names[0]) # set default value to first column name
        column_dropdown = ttk.Combobox(mod, textvariable=column_var, values=column_names)
        column_dropdown.pack()

        # create text box for entering value
        value_var = tk.StringVar(mod)
        value_entry = tk.Entry(mod, textvariable=value_var)
        value_entry.pack()

        def submit(self):
            id = id_entry.get()
            column_name = column_var.get()
            value = value_var.get()
            if (table == 0):
                restaurant.updateRestaurant(self, id, column_name, value)
            elif (table == 1):
                customer.updateCustomer(self, id, column_name, value)
            elif (table == 2):
                transactions.updateOrder(self, id, column_name, value)
            elif (table == 3):
                transactions.updateReview(self, id, column_name, value)
            elif (table == 4):
                transactions.updateReservation(self, id, column_name, value)
            mod.destroy()

        # create button to submit modifications
        submit_button = tk.Button(mod, text="Submit", command=lambda: submit(self))
        submit_button.pack()

        mod.mainloop()
        

    # table flag: 0 = Restaurant, 1 = Customer, 2 = orders, 3 = reviews, 4 = reservations
    def delete(self, table):
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

        # get ID from user
        # delete row with that ID
        window = tk.Toplevel(self.root)

         # set properties of the new window as desired
        width = self.width
        height = self.height
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        window.geometry(alignstr)
        window.resizable(width=False, height=False)

        # create a "Back" button
        back_button = tk.Button(window, text="Back", command=lambda: self.show_root(window))
        #back_button.place(x=10, y=10, width=50, height=25)
        back_button.pack(anchor='nw')

        # hide the previous window
        #self.prev_window.withdraw()

        # create a label and text box to get the ID from the user
        id_label = tk.Label(window, text="Enter ID to delete:")
        id_label.pack()
        id_entry = tk.Entry(window)
        id_entry.pack()

        # create a function to execute the SQL DELETE statement when the button is clicked
        def delete_row():
            id = id_entry.get()
            if table == 0:
                restaurant.deleteRestaurant(self, id)
            elif table == 1:
                customer.deleteCustomer(self, id)
            elif table == 2:
                transactions.deleteOrder(self, id)
            elif table == 3:
                transactions.deleteReview(self, id)
            elif table == 4:
                transactions.deleteReservation(self, id)
            window.destroy()

        # create a button to execute the delete_row function
        delete_button = tk.Button(window, text="Delete", command=delete_row)
        delete_button.pack()
        

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
        
        # hide the previous window
        self.prev_window.withdraw() if self.prev_window else self.root.withdraw()
        
        # store a reference to the new window
        self.prev_window = new_window

    def show_root(self, window):
        # destroy the current window
        window.destroy()
        
        # show the previous window
        self.prev_window = None
        self.root.deiconify() if not self.prev_window else self.prev_window.deiconify()


root = tk.Tk()
app = App(root)
root.mainloop()
