from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


from oauth2client.client import SignedJwtAssertionCredentials


import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/admin.directory.user.readonly']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    from oauth2client.client import SignedJwtAssertionCredentials
    client_email = 'one-on-one-account@windy-raceway-118617.iam.gserviceaccount.com'
    with open("ConvertedPrivateKey.pem") as f:
        private_key = f.read()
    credentials = SignedJwtAssertionCredentials(client_email,
                                                private_key,
                                                ['https://www.googleapis.com/auth/calendar',
                                                 'https://www.googleapis.com/auth/admin.directory.user.readonly'],
                                                 sub='kristin@gc.com')
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service1 = discovery.build('calendar', 'v3', http=http)
    service2 = discovery.build('admin', 'directory_v1', http=http)
    results = results = service2.users().list(customer='my_customer', query="name:Alex Etling").execute()
    print results
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service1.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
