# Code Used from Google workspace quick start: https://developers.google.com/calendar/api/quickstart/python
# Code Used from create event devlopers guide: https://developers.google.com/calendar/api/guides/create-events

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    queries = {
        "Add Event": "Add a detailed new event to your calendar.",
        "Quick Add Event": "Add an event based on a simple text string for fast entry.",
        "Remove Event": "Removes an event from your calendar.",
        "Check Event": "Checks an upcoming event's details from your calendar."
    }

    print("Welcome to [YOUR NAME]'s personalized script. Below is the list of commands accepted:\n")
    for command, description in queries.items():
        print(f"    {command}: {description}")

    # cleans user's input
    query = input("\nWhat can I help you with?\n").lower().strip().replace(" ", "")
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    if query == "checkevent":
        checkEvent(creds) 

    elif query == "addevent":
        addEvent(creds)

    elif query == "quickaddevent":
        quickAddEvent(creds)

    else:
        print("Invalid input. Try again.\n")
        main()

def checkEvent(creds):
    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


def addEvent(creds):
    service = build("calendar", "v3", credentials=creds)
    summary = input("Enter the event name:\n")
    location = input("Enter the event location (or leave blank):\n")
    description = input("Enter a description for the event (or leave blank):\n")

    # Ask if the event is a multiple-day event
    is_multiple_day = input("Is this a multiple-day event? (yes/no):\n").lower().strip()

    if is_multiple_day == "yes":
        start_date = input("Enter the start date (format: YYYY-MM-DD):\n")
        start_time = input("Enter the start time (format: HH:MM, 24-hour format):\n")
    
        end_date = input("Enter the end date (format: YYYY-MM-DD):\n")
        end_time = input("Enter the end time (format: HH:MM, 24-hour format):\n")
    else:
        start_date = input("Enter the event date (format: YYYY-MM-DD):\n")
        start_time = input("Enter the start time (format: HH:MM, 24-hour format):\n")

        end_date = start_date
        end_time = input("Enter the end time (format: HH:MM, 24-hour format):\n")
        
    start_datetime = f"{start_date}T{start_time}:00"
    end_datetime = f"{end_date}T{end_time}:00"

    start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")
    end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")

    # Ask if they want to invite people 
    has_attendees = input("Do you want to invite people to the event? (yes/no):\n").lower().strip()
    attendees = []
    if has_attendees == "yes":
        attendee_emails = input("Enter emails of attendees (separate list with commas):\n").strip()
        attendees = [{'email': email.strip()} for email in attendee_emails.split(",")]
        
        attendee_emails.split(",")

    event = {
        'summary': summary,
        'location': location if location else None,
        'description': description if description else None,
        'start': {
            'dateTime': start_datetime.isoformat(), 
            'timeZone': 'America/Los_Angeles', # change time zone as needed
        },
        'end': {
            'dateTime': end_datetime.isoformat(), 
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': attendees,
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
    print('Event created: %s' % (event.get('htmlLink')))

def quickAddEvent(creds):
    service = build("calendar", "v3", credentials=creds)
    summary = input("Enter a quick description of the event:\n")

    event = service.events().quickAdd(
        calendarId='primary',
        text=summary).execute()
    
    print('Event created: %s' % (event.get('htmlLink')))

if __name__ == "__main__":
    main()