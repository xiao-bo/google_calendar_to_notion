from datetime import datetime
import traceback
import logging
from libs.google_api.google_calendar_api import GoogleCalendarAPI


class GoogleCalendarRepo(object):
    def __init__(self):
        self._init_google_calendar_api()

    def _init_google_calendar_api(self):
        self.cal = GoogleCalendarAPI()

    def query_calendar(
            self, last_updated_time: str, future_range: str):
        last_updated_time = datetime.strptime(
            last_updated_time, '%Y/%m/%d %H:%M:%S'
        )
        days = self._transfer_future_range_to_days(future_range)
        events = self.cal.query_event_from_calendar(
            last_updated_time,
            days
        )
        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            print(f'title = {event["summary"]},'
                  f'狀態:{event["status"]} '
                  f'開始時間:{start}, 結束時間: {end} '
                  f'更新時間:{event["updated"]} '
                  f'link:{event["htmlLink"]}'
                  )
            try:
                print(event['description'])
            except:
                continue

        return events

    def _transfer_future_range_to_days(
        self, future_range: str
    ) -> int:
        # transfer {%d}days to {%d}, 
        # like 3days -> 3

        sp = future_range.split('days')
        try:
            ret = int(sp[0])
        except Exception as e:
            print(
                f'_transfer_future_range_to_days has error:'
                f'future_range格式有錯，請輸入 %ddays'
            )
            raise 
        return ret
