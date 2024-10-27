# Code Used from Google workspace quick start: https://developers.google.com/calendar/api/quickstart/python
# Code Used from create event devlopers guide: https://developers.google.com/calendar/api/guides/create-events


import datetime
import os.path
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next N events on the user's calendar.
    """
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
    return creds

def all_Events(creds):
    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults= 100,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        total_events = len(events)
        # Th
        number = input("How many Events? (Total:" + str(total_events) +")") 
        # Call the Calendar API
        print("Getting the upcoming " + str(number) + " events")
        events = events[0:int(number)]
        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            year = start[0:4]
            day = start [8:10]
            if int(start[5:7]) == 1:
                month = "January"
            elif int(start[5:7]) == 2:
                month = "February"
            elif int(start[5:7]) == 3:
                month = "March"
            elif int(start[5:7]) == 4:
                month = "April"
            elif int(start[5:7]) == 5:
                month = "May"
            elif int(start[5:7]) == 6:
                month = "June"
            elif int(start[5:7]) == 7:
                month = "July"
            elif int(start[5:7]) == 8:
                month = "August"
            elif int(start[5:7]) == 9:
                month = "September"
            elif int(start[5:7]) == 10:
                month = "October"
            elif int(start[5:7]) == 11:
                month = "November"
            elif int(start[5:7]) == 12:
                month = "December"
            if int(start[11:13]) > 12:
                num = int(start[11:13])
                value = num % 12
                actual = month+ " " + day + ", " + year + " at " + str(value) + start[13:16] + " PM:"
            elif int(start[11:13]) < 1:
                actual = month+ " " + day + ", " + year + " at " + str(12) + start[13:16] + " AM:"
            else:
                actual = month+ " " + day + ", " + year + " at " + start[12:16] + " AM:"

            print(actual, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")

def checkEvent(creds):
    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults= 100,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
        events = events_result.get("items", [])
        time = input("What day would you like to check? [YEAR-MONTH-DAY]")
        check = 0
        for event in events:
            if time == event['start']['dateTime'][0:10]:
                print(time, event["summary"])
                check += 1
        if check < 1:
            print("No Events Found")

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

def remove_Event(creds):
    service = build("calendar", "v3", credentials=creds)
    now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults= 100,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    summary = input("What is the name of the event?")
    month = input("What Month is the event? (Include 0 before single digit months)")
    day = input("What Day is the event?")
    year = input("What Year is the event?")
    date = str(year) +"-" + str(month) + "-" + str(day)
    check = 0
    for event in events:
        if summary == event["summary"] and date == event['start']['dateTime'][0:10]:
            service.events().delete(calendarId='primary', eventId=event.get('id')).execute()
            print("Event Removed")
            check += 1
    if check < 1:
        print("No Events Found")


if __name__ == "__main__":
  creds = main()
  query = input("What can I help you with?")
  if query == "Check Events":
    all_Events(creds)
  if query == "Check Event":
    checkEvent(creds)
  elif query == "Add Event":
    addEvent(creds)
  elif query == "Quick Add":
    quickAddEvent(creds)
  elif query == "Remove Event":
    remove_Event(creds)
  else:
    print("Invalid input. Try asking to 'Check Events' or 'Add Event'.")
    os.system('ipython actual_api.py')