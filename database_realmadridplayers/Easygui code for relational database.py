import easygui as eg
import sqlite3

# --- Database Setup and Functions ---
def setup_database():
    """
    Connects to the SQLite database and ensures the contacts table exists.
    If the database file doesn't exist, SQLite will create it.
    This function returns the connection and cursor objects for later use.
    """
    try:
        # Connect to the database file named 'contacts.db'.
        # This will create the file if it doesn't exist.
        conn = sqlite3.connect('relational_database.db')

        # Create a cursor object to execute SQL commands.
        cursor = conn.cursor()
        
        # SQL command to create the 'contacts' table if it doesn't already exist.
        # This prevents an error if you run the script multiple times.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT
            )
        ''')
    
        # Another table is created 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
            )
        ''')

        # Commit the changes to save the table creation to the database file.
        conn.commit()

        # Return the connection and cursor for use in other functions.
        return conn, cursor
        
    except sqlite3.Error as e:
        # Use EasyGui to show an error message if the database connection fails.
        eg.exceptionbox(msg=f"A database error occurred: {e}", title="Database Error")
        # Return None to signal that a fatal error occurred.
        return None, None

# --- Database Add customer and Functions ---
def add_customer(conn, cursor):
    """
    Prompts the user for a new customer's details and inserts them into the Customers table.
    """
    msg = "Enter new customer information"
    title = "Add Customer"
    fieldNames = ["customer_id", "first_name", "last_name"]

    fieldValues = eg.multenterbox(msg, title, fieldNames)

    if fieldValues is None:
        return

    customer_id, first_name, last_name = fieldValues

    # Checks if any input is empty; shows error and stops if so
    if not customer_id or not first_name or not last_name:
        eg.msgbox("All boxes need to be filled!", "Input Erroe")
        return

    # Tries to add a new row to the Customers table with the provided values
    try:
        cursor.execute("INSERT INTO Customers VALUES (?, ?, ?)",
            (customer_id, first_name, last_name))

        conn.commit()
        eg.msgbox(f"Customer '{first_name}' added successfully!", "Success")

    except sqlite3.IntegrityError:
        eg.msgbox(f"Error: Customer ID '{customer_id}' already exists.", "Database Error")
        
    except sqlite3.Error as e:
        eg.exceptionbox(msg=f"Failed to add customer: {e}", title="Database Error")

def show_customers(cursor):
    # Gets all rows from the Customers table and stores them in 'rows'
    cursor.execute("SELECT * FROM Customers")
    rows = cursor.fetchall()

    # If no customers are found, show a message and exit the function
    if not rows:
        eg.msgbox("No customers found.")
        return

    # Creates a formatted text list of all customers for display
    text = "Customer ID\tFirst Name\tLast Name\n" + "="*60 + "\n"
    for customer_id, first_name, last_name in rows:
        text += f"{customer_id}\t{first_name}\t{last_name}\n"

    eg.codebox("Customers", "Customers List", text)

def add_order(conn, cursor):
    """
    Prompts the user for a new customer's details and inserts them into the Customers table.
    """
    msg = "Enter new order details"
    title = "Add Order"
    fieldNames = ["order_id", "customer_id", "order_date", "total_amount"]

    fieldValues = eg.multenterbox(msg, title, fieldNames)

    if fieldValues is None:
        return

    order_id, customer_id, order_date, total_amount = fieldValues

    # Checks if any input is empty; shows error and stops if so
    if not order_id or not customer_id or not order_date or not total_amount:
        eg.msgbox("All fields are required.", "Input Error")
        return
    
    # Tries to add a new row to the order table with the provided values
    try:
        cursor.execute("INSERT INTO Orders VALUES (?, ?, ?, ?)",
                       (order_id, customer_id, order_date, total_amount))
        conn.commit()
        eg.msgbox("Order was added successfully!", "Success")

    except sqlite3.IntegrityError:
        eg.msgbox(f"Error: Order ID '{order_id}' already exists.", "Database Error")

    except sqlite3.Error as e:
        eg.exceptionbox(msg=f"Failed to add order: {e}", title="Database Error")

def show_orders(cursor):
    # Gets all rows from the Orders table and stores them in 'rows'
    cursor.execute("SELECT * FROM Orders")
    rows = cursor.fetchall()

    # If no orders are found, show a message and exit the function
    if not rows:
        eg.msgbox("No orders found.")
        return

    # Creates a formatted text list of all orders for display
    text = "Order ID\tCustomer ID\tDate\tAmount\n" + "="*60 + "\n"
    for order_id, customer_id, order_date, total_amount in rows:
        text += f"{order_id}\t{customer_id}\t{order_date}\t{total_amount}\n"

    eg.codebox("Orders", "Orders List", text)

# --- Main Program Logic ---
if __name__ == "__main__":
    # Initialize the database connection and cursor.
    conn, cursor = setup_database()
    
    # Exit if the database setup failed.
    if not conn:
        exit()

    while True:
        # Use EasyGui's buttonbox to create a main menu for the user.
        # This function returns the text of the button that was clicked.
        choice = eg.buttonbox(
            "What would you like to do?",
            "Main Menu",
            choices=["Add Customer", "Add Order", "Show Customers", "Show Orders", "Exit"]
        )

        # Handle the user's choice.
        if choice == "Add Customer":
            add_customer(conn, cursor)
        elif choice == "Add Order":
            add_order(conn, cursor)
        elif choice == "Show Customers":
            show_customers(cursor)
        elif choice == "Show Orders":
            show_orders(cursor)
        # The loop breaks if the user clicks 'Exit' or closes the window ('None').
        else:
            break
    
    # Closes the database connection when the program's main loop ends.
    conn.close()
    eg.msgbox("Goodbye!", "Exiting Program")