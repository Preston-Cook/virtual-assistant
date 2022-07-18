import sqlite3
from tts import speak

# Connect to sqlite databse
conn = sqlite3.connect('contacts.db')

# Define a cursor
cur = conn.cursor()

def add_contact():

    # Create contacts table if it doesn't exist
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        email TEXT, 
        phone TEXT
    );""")

    # Commit changes
    conn.commit()

    # Notify user that they must enter information in the terminal
    speak("Please Enter the New Contact Information in the Terminal")

    # Prompt the user for the contact information
    confirmation = None

    while confirmation not in ['y','yes']:
        print('\n--New Contact Information Prompt--\n')
        name = [word.strip().lower() for word in input("Contact Name: ").strip().split()]
        email = input("Contact Email Address: ").strip()
        phone = '+1' + input("Contact Phone Number: ").replace("-",'').replace('(','').replace(')','').strip()

        while len(name) == 1:
            speak("Please enter the contact's first and last name")
            name = [word.strip().lower() for word in input("Contact Name: ").strip().split()]

        name = ' '.join(name)
        
        # Preview data for user confirmation
        print(f"""\n--Add Contact--\n
Contact Name: {name}
Contact Email: {email}
Contact Phone Number: {phone}
\n""")

        # Ensure contact information is valid 
        speak("Does the contact information above appear valid?: ")
        confirmation = input("Does the contact information above appear valid? (Y/N): ").lower()
        
        # Input validation
        while confirmation not in ['y','n','yes','no']:
            print("ERROR: Invalid input")
            confirmation = input("Does the following contact information appear valid? (Y/N): ").lower()
    
    cur.execute("SELECT * FROM contacts WHERE name = ?", (name.lower(),))
    conn.commit()

    in_database = cur.fetchone()
    if in_database is not None:
        speak(f"{name}'s contact information is already present inside my internal database")
        return None

    # Insert new entry into the contacts database file and commit changes
    cur.execute("INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?);", (name.lower(), email.lower(), phone))
    conn.commit()

    # Notify User of Success
    speak(f"I successfully added {name}'s contact information inside my internal database.")


def update_contact():

    # Create contacts table if it doesn't exist
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        email TEXT, 
        phone TEXT
    );""")

    # Commit changes
    conn.commit()

    # Query databse for contacts data and commit execution
    cur.execute("SELECT * FROM contacts;")
    contacts_data = cur.fetchall()
    conn.commit()

    # Check if databse is empty
    if not contacts_data:
        speak("I do not currently have any contacts data inside my internal database")
        return None
    
    # Ask user to input person whose information they wish to update
    speak("Please enter the contact's name whose contact information you would like to update in the Terminal")
    
    # Prompt user for contact name
    print('\n--Contact Update Prompt--\n')
    name = [word.strip().lower() for word in input("Contact Name: ").strip().split()]
    
    while len(name) == 1:
            speak("Please enter the contact's first and last name")
            name = [word.strip().lower() for word in input("Contact Name: ").strip().split()]

    # Initialize row_num variable
    row_num = None

    # Search data for contact name's row number
    for row, entry in enumerate(contacts_data):
        entry_name = entry[1]
        if name[0] in entry_name and name[1] in entry_name:
            row_num = row
            break
    
    name = ' '.join(name)

    # Notify user if computer unable to find entry inside internal databse
    if row_num is None:
        speak(f"I'm unable to find a contact named {name} inside my internal database")
        return None
    
    speak(f"I have successfully located {name}'s contact information inside my internal database. Please enter the new information below. If you would not like to alter a field, leave it blank")

    # Select current values for user from contacts_data
    id = contacts_data[row_num][0]
    cur_name = contacts_data[row_num][1]
    cur_email = contacts_data[row_num][2]
    cur_phone = contacts_data[row_num][3]

    print(cur_phone)

    confirmation = None

    while confirmation not in ['y','yes']:
        
        # Display Current Contact information to user
        print(f"""\n---Current Information---\n
Current Contact Name: {cur_name}
Current Contact Email: {cur_email}
Current Contact Phone Number: {cur_phone}
\n""")
    
        # Prompt user for new contact information
        print('\n--Updated Information Prompt--\n')
        name_field = [word.strip().lower() for word in input("Contact Name: ").strip().split()]
        email_field = input("Updated Contact Email: ").strip()
        phone_field = '+1' + input("Updated Contact Phone Number: ").replace("-",'').replace('(','').replace(')','').strip()

        while len(name_field) == 1:
            speak("Please enter the contact's first and last name")
            name_field = [word.strip().lower() for word in input("Contact Name: ").strip().split()]
        
        name_field = ' '.join(name_field)


        # Check which information the user would like to update
        new_name = name_field if name_field != '' else cur_name
        new_email = email_field if email_field != '' else cur_email
        new_phone = phone_field if phone_field != '+1' else cur_phone

        # Preview Updated Contact Information for User
        print(f"""\n---Updated Contact Information---\n
Updated Contact Name: {new_name}
Updated Contact Email: {new_email}
Updated Contact Phone Number: {new_phone}
\n""")

        # Ensure contact information is valid 
        speak("Does the contact information above appear valid?: ")
        confirmation = input("Does the contact information above appear valid? (Y/N): ").lower()
        
        # Input validation
        while confirmation not in ['y','n','yes','no']:
            confirmation = input("Does the following contact information appear valid? (Y/N): ").lower()

    # Update information inside database
    cur.execute("UPDATE contacts SET name = ?, email = ?, phone = ? WHERE id = ?;", (new_name.lower(), new_email.lower(), new_phone, id))
    conn.commit()

    # Notify User of Success
    speak(f"I have successfully updated {new_name}'s contact information inside my internal database")

def delete_contact():
     # Create contacts table if it doesn't exist
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        email TEXT, 
        phone TEXT
    );""")

    # Commit changes
    conn.commit()

    # Query databse for contacts data and commit execution
    cur.execute("SELECT * FROM contacts;")
    contacts_data = cur.fetchall()
    conn.commit()


    # Prompt user for which user they would like to delete
    speak("Please enter the contact's name whose contact information you would like to delete in the terminal)")
    
    print('\n--Contact Deletion Prompt--\n')
    name = [word.strip().lower() for word in input("Contact Name: ").strip().split()]

    # Ensure user inputs first and last name
    while len(name) == 1:
        speak("Please enter the contact's first and last name")
        name = [word.strip().lower() for word in input("Contact Name: ").strip().split()]

    # Initialize row_num variable
    row_num = None

    # Search data for contact name's row number
    for row, entry in enumerate(contacts_data):
        entry_name = entry[1]
        if name[0] in entry_name and name[1] in entry_name:
            row_num = row
            break
    
    name = ' '.join(name)
    id = contacts_data[row_num][0]

    # Notify user if computer unable to find entry inside internal databse
    if row_num is None:
        speak(f"I'm unable to find a contact named {name} inside my internal database.")
        return None
    
    # Notify user that contact was located within internal database
    speak(f"I successfully located {name}'s contact information inside my internal database.")

    # Ensure user wants to delete the user
    speak(f"Are you sure you would like me to delete {name}'s contact information?")
    
    confirmation = input(f"Are you sure you would like me to delete {name}'s contact information? (Y/N): ").lower()

    while confirmation not in ['y','n','no','yes']:
        confirmation = input(f"Are you sure you would like me to delete {name}'s contact information? (Y/N): ").lower()
    
    if confirmation in ['n','no']:
        speak(f"Okay, I will not delete {name}'s contact information")
        return None

    # Delete contact's row from database 
    cur.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()

    # Notify user of success
    speak(f"I have successfully deleted {name}'s contact information from my internal database")