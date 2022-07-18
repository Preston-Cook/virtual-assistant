import smtplib
import sqlite3
import ssl
from email.message import EmailMessage

from twilio.rest import Client

from api_secrets import email_creds, twilio_creds
from tts import speak

# Connect to sqlite databse
conn = sqlite3.connect('contacts.db')

# Define a cursor
cur = conn.cursor()

# Initialize Account SID and Auth_Token
account_sid = twilio_creds['account_sid']
auth_token = twilio_creds['auth_token']


def send_text(prompt):

    # Convert prompt to list
    pieces = prompt.split()[::-1]

    # Pick subject from prompt searching for keyword "to"
    subject = pieces[pieces.index('to') - 1].lower()

    # Retrieve contact's information from database
    cur.execute("SELECT * FROM contacts WHERE name LIKE ?", (f'{subject}%',))
    contact_data = cur.fetchall()

    user_selection = 0
    
    if not contact_data:
        speak(f"I do not have a contact named {subject} inside my internal database")
        return None

    # Check if there are multiple rows with the same name
    elif len(contact_data) > 1:
        
        # Gather repeated names
        names = [entry[1].title() for entry in contact_data]

        # Notify user of repeates
        speak(f"There are multiple people in my internal database named {subject}. Please specify which contact you would like to text in the terminal")
        
        # Prompt user for choice
        print('\n--Repeated Names--\n')
        for count, name in enumerate(names, start=1):
            print(f'{count}: {name}')
        speak("Enter the number corresponding with your contact")
        user_selection = int(input("\nSelection: ")) - 1

        # Input validation
        while user_selection not in range(len(names)):
            user_selection = int(input("\nSelection: ")) - 1
        
    subject_phone = contact_data[user_selection][-1]
    subject = contact_data[user_selection][1]

    if subject_phone is None:
        speak(f"I do not have a phone number for {subject} inside my internal database")
        return None
    
    # Prompt user for text body in terminal
    speak("\nPlease specify your text message within the terminal")

    # Retrieve message from user
    message_text = input("\nEnter your message: ")

    # Confirm user selection
    confirmation = None
    while confirmation not in ['y','n','yes','no']:
        print("\n--Your Message--\n", message_text, sep='\n')
        speak("Does the message above appear valid?")
        confirmation = input("\nDoes the message above appear valid? (Y/N): ").lower()
    
    # Do not send text message if user chooses no
    if confirmation in ['n','no']:
        speak("Okay, I will not send the text message")
        return None

    # Initialize client object
    client = Client(account_sid,auth_token)

    # Create message using API call
    message = client.messages.create(
        to=subject_phone,
        from_=twilio_creds['my_twilio'],
        body=message_text
    )

    speak(f"I successfully sent your text message to {subject}")


def send_email(prompt):

    # Convert prompt to list
    pieces = prompt.split()[::-1]

    # Pick subject from prompt searching for keyword "to"
    receiver = pieces[pieces.index('to') - 1].lower()

    # Retrieve contact's information from database
    cur.execute("SELECT * FROM contacts WHERE name LIKE ?", (f'{receiver}%',))
    contact_data = cur.fetchall()

    user_selection = 0
    
    if not contact_data:
        speak(f"I do not have a contact named {receiver} inside my internal database")
        return None

    # Check if there are multiple rows with the same name
    elif len(contact_data) > 1:
        
        # Gather repeated names
        names = [entry[1].title() for entry in contact_data]

        # Notify user of repeates
        speak(f"There are multiple people in my internal database named {receiver}. Please specify which contact you would like to email in the terminal")
        
        # Prompt user for choice
        print('\n--Repeated Names--\n')
        for count, name in enumerate(names, start=1):
            print(f'{count}: {name}')
        speak("Enter the number corresponding with your contact")
        user_selection = int(input("\nSelection: ")) - 1

        # Input validation
        while user_selection not in range(len(names)):
            user_selection = int(input("\nSelection: ")) - 1

    subject_email = contact_data[user_selection][-2]
    subject = contact_data[user_selection][1]

    if not subject_email or '@' not in subject_email:
        speak(f"I do not have an email for {subject} inside my internal database")
        return None

    # Prompt user to Define subject
    speak("\nPlease enter the subject and content of your email in the terminal\n")

    # Prompt user for subject and body
    email_subject = input("Enter Email Subject: ")
    email_body = input("Enter Email Content: ")

    # User confirmation
    confirmation = None
    while confirmation not in ['y','n','yes','no']:
        print("\n--Your Message--\n", email_subject, email_body, sep='\n')
        speak("Does your email above appear valid?")
        confirmation = input("\nDoes the message above appear valid? (Y/N): ").lower()
    
    # Do not send text message if user chooses no
    if confirmation in ['n','no']:
        speak("Okay, I will not send the text message")
        return None

    # Initialize message object and specifications
    em = EmailMessage()
    em['From'] = email_creds['sender']
    em['To'] = subject_email
    em['Subject'] = email_subject
    em.set_content(email_body)

    # Create default context to avoid ssl cert errors
    context = ssl.create_default_context()

    # Connect to email server and send message
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_creds['sender'], email_creds['password'])
        smtp.sendmail(email_creds['sender'], subject_email, em.as_string())
    
    speak(f"I successfully sent an email to {receiver}")