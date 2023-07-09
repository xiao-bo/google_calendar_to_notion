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
            self, last_updated_time: datetime, future_range: str
    ) -> list:

        days = self._transfer_future_range_to_days(future_range)
        events = self.cal.query_event_from_calendar(
            last_updated_time,
            days
        )

        ret_events = []

        if not events:
            print('No events found.')
            return

        for event in events:
            ret_dict = {}

            ret_dict['start'] = event['start'].get(
                'dateTime', event['start'].get('date'))
            ret_dict['end'] = event['end'].get(
                'dateTime', event['end'].get('date'))
            ret_dict['title'] = event.get("summary")
            ret_dict['status'] = event.get("status")
            ret_dict["updated"] = datetime.strptime(
                event.get("updated"), '%Y-%m-%dT%H:%M:%S.%fZ'
            )
            ret_dict["link"] = event.get("htmlLink")
            ret_dict["description"] = event.get("description")

            ret_events.append(ret_dict)

        return ret_events

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
