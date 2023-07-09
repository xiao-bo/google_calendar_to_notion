from __future__ import print_function

from datetime import datetime, timedelta
import os.path
import context
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class GoogleCalendarAPI(object):
    def __init__(self):
        self.__token_path = (
            f'{context.PROJECT_ROOT_PATH}/docs/token.json'
        )
        self.__auth_path = (
            f'{context.PROJECT_ROOT_PATH}/docs/auth.json'
        )
        self.__creds = self.__get_creds()

    def __get_creds(self) -> object:
        """
        creds = None
        # The file token.json stores the user's access
        # and refresh tokens, and is
        # created automatically when the authorization
        # flow completes for the first
        # time.
        """
        # todo 
        # token過期的作法

        if os.path.exists(self.__token_path):
            creds = Credentials.from_authorized_user_file(
                self.__token_path, SCOPES)
            return creds

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.__auth_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.__token_path, 'w') as token:
                token.write(creds.to_json())
            return creds

    def query_event_from_calendar(
        self,
        last_updated_time: datetime,
        future_days: int
    )->object: 
        print('query_calendar')

        try:
            service = build(
                'calendar',
                'v3',
                credentials=self.__creds
            )
            # Call the Calendar API
            time_min = last_updated_time.isoformat()+'Z'
            time_max = (datetime.utcnow()+timedelta(days=future_days)
                        ).isoformat()+'Z'
            events_result = service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                maxResults=5,
                singleEvents=True,
                showDeleted=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])
            return events

        except HttpError as error:
            print('Query_calendar: An error occurred: %s' % error)
