from __future__ import print_function

import datetime
import os.path
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = None
now = datetime.datetime.utcnow().isoformat() + 'Z'

def getCredential():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    global service
    try:
        service = build('calendar', 'v3', credentials=creds)
    except HttpError as error:
        print('An error occurred: %s' % error)

def listEvents(calendarId):
    events_result = service.events().list(
        calendarId=calendarId, 
        timeMin=now,
        maxResults=250, 
        singleEvents=True,
        orderBy='startTime'
        ).execute()
    events = events_result.get('items', [])

    if not events:
        print('Nenhum evento futuro encontrado.')
        return
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def listCalendars():
    page_token = None
    print(service.calendarList())
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            # listEvents(calendar_list_entry['id'])
            # print(calendar_list_entry)
            print(calendar_list_entry['summary'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

def listCalendarsAndEvents():
    try:
        maxResults = 250
        print('Exibindo no máximo até '+str(maxResults)+' eventos futuros.')

        # listCalendars()
        
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=250, 
            singleEvents=True,
            orderBy='startTime'
            ).execute()
        events = events_result.get('items', [])

        if not events:
            print('Nenhum evento futuro encontrado.')
            return
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # print(event)
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)

"""
referencias de cores disponíveis no Google Calendar
index - hex - nome da cor
0 - #039BE5 - Pavão
1 - #7986CB - Lavanda
2 - #33B679 - Sálvia
3 - #8E24AA - Uva
4 - #E67C73 - Flamingo
5 - #F6BF26 - Banana
6 - #F4511E - Tangerina
7 - #039BE5 - Pavão
8 - #616161 - Grafite
9 - #3F51B5 - Mirtilo
10 - #0B8043 - Manjericão
11 - #D50000 - Tomate
"""

"""
    eventBody = {
        'summary': 'Google I/O 2015',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': '2023-05-28T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2023-05-28T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'background':eventToAdd,
        'foreground':eventToAdd,
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
    }
"""

def insertEvent(eventToAdd):
    eventBody = {
        'summary': 'Título de teste',
        'description': 'Paciente quer procedimento não convencional',
        'colorId':str(eventToAdd),
        'start': {
            'dateTime': '2023-05-30T09:00:00-07:00'
        },
        'end': {
            'dateTime': '2023-05-30T17:00:00-07:00'
        },
    }

    event = service.events().insert(calendarId='primary', body=eventBody).execute()
    print('Evento criado: %s' % (event.get('htmlLink')))
    print(event)
    print(event['id'])

def updateEvent(eventToUpdate, eventId):
    event_result = service.events().update(
        calendarId='primary',
        eventId=eventId,
        body={
        "summary": 'Updated Automating calendar',
        "description": 'This is a tutorial example of automating google calendar with python, updated time.',
        "start": {"dateTime": '2023-05-30T09:00:00-07:00'},
        "end": {"dateTime": '2023-05-30T10:00:00-07:00'},
        },
    ).execute()

def main():
    getCredential()
    listCalendarsAndEvents()
    sysArgs = sys.argv
    rangeOfArg = range(1, len(sysArgs))
    for i in rangeOfArg:
        insertEvent(sysArgs[i])

    

if __name__ == '__main__':
    main()