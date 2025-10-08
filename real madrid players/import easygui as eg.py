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
        conn = sqlite3.connect('contacts.db')
        
        # Create a cursor object to execute SQL commands.
        cursor = conn.cursor()
        
        # SQL command to create the 'contacts' table if it doesn't already exist.
        # This prevents an error if you run the script multiple times.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
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

def add_contact(conn, cursor):
    """
    Prompts the user for a new contact's details and inserts them into the database.
    """
    msg = "Enter new contact information"
    title = "Add Contact"
    fieldNames = ["Name", "Email"]
    
    # Use EasyGui's multenterbox to get multiple inputs from the user.
    # The return value is a list of strings, or None if the user clicks 'Cancel'.
    fieldValues = eg.multenterbox(msg, title, fieldNames)

    # Check if the user clicked 'Cancel'.
    if fieldValues is None:
        return

    # Unpack the list of values into separate variables.
    name, email = fieldValues
    
    # Validate that both fields have been filled in.
    if not name or not email:
        eg.msgbox("Both Name and Email are required.", "Input Error")
        return

    try:
        # Execute an INSERT SQL command using placeholders (?) to prevent SQL injection.
        # This is the safest way to insert user-provided data.
        cursor.execute("INSERT INTO contacts (name, email) VALUES (?, ?)", (name, email))
        
        # Commit the changes to the database to make the insertion permanent.
        conn.commit()
        
        # Show a success message to the user.
        eg.msgbox(f"Contact '{name}' added successfully!", "Success")
        
    except sqlite3.IntegrityError:
        # Catch a specific error if the email is not unique (due to the UNIQUE constraint).
        eg.msgbox(f"Error: The email '{email}' already exists.", "Database Error")
    except sqlite3.Error as e:
        # Catch any other database errors and display them.
        eg.exceptionbox(msg=f"Failed to add contact: {e}", title="Database Error")
        
def show_contacts(cursor):
    """
    Retrieves all contacts from the database and displays them in a formatted message box.
    """
    try:
        # Execute a SELECT query to get the name and email of all contacts.
        cursor.execute("SELECT name, email FROM contacts")
        
        # Fetch all the results from the query as a list of tuples.
        rows = cursor.fetchall()

        if not rows:
            # If the list is empty, there are no contacts.
            eg.msgbox("No contacts found in the database.", "Contact List")
            return

        # Prepare a header for the display text.
        contact_list = "Name\t\tEmail\n"
        contact_list += "=" * 40 + "\n"
        
        # Loop through the list of tuples and format each contact into a string.
        for name, email in rows:
            contact_list += f"{name}\t\t{email}\n"
            
        # Use EasyGui's textbox to show the formatted list. This widget is scrollable.
        eg.textbox("All Contacts", "Contact List", contact_list)
        
    except sqlite3.Error as e:
        # Catch and display any errors during the retrieval process.
        eg.exceptionbox(msg=f"Failed to retrieve contacts: {e}", title="Database Error")

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
            choices=["Add Contact", "Show All Contacts", "Exit"]
        )

        # Handle the user's choice.
        if choice == "Add Contact":
            add_contact(conn, cursor)
        elif choice == "Show All Contacts":
            show_contacts(cursor)
        elif choice == "Exit" or choice is None:
            # The loop breaks if the user clicks 'Exit' or closes the window ('None').
            break
    
    # Close the database connection when the program's main loop ends.
    conn.close()
    eg.msgbox("Goodbye!", "Exiting Program")