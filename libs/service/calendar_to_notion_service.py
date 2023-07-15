# 同步calendar event 至notion
from datetime import datetime
from configobj import ConfigObj
import context
from libs.repo.google_repo import GoogleCalendarRepo
from libs.repo.notion_repo import NotionRepo


class CalendarToNotionService(object):

    def __init__(self):
        self.config = ConfigObj(
            f'{context.PROJECT_ROOT_PATH}/docs/config.ini',
            encoding='utf-8'
        )

    def handle(self):
        last_updated_time = self.__get_last_updated_time()
        future_range = self.__get_future_range()

        # 1. 根據config.ini的timestamp，
        # 讀取google 日曆的最後更新時間到未來近一個月的所有活動，
        # 得到日曆的title, url, content, date, updated_time。

        event_list = self.__get_event_from_google_calendar(
            last_updated_time, future_range)
        print(event_list)
        '''
        # event is list of object
        # event_list = [{
            "title":xx, 
            "url":xx
        },

        ]
        '''

        # 2. 使用notion api，get database rows
        notion_rows = self.__get_rows_from_notion_database(
            last_updated_time)

        # 3.拿到url和page_id後，跟日曆的url做比較，得到待新增的page，
        # 和待更新的page（待更新的page包含哪些page的tag要改成取消）

        new_event_list, updated_event_list = \
            self._grouping_event_list(
                event_list, notion_rows)

        
        # 4. 更新row of notion
        #self.__update_row_in_notion_database(
        #    updated_event_list)
        
        # 5. 新增row of notion，包含內文
        self.__append_row_to_notion_database(
            new_event_list)
        '''
        # 5. 更新設定檔
        self.__update_last_updated_time_at_config()
        '''

    def __get_last_updated_time(self):
        last_updated_time = self.config['system_info']['last_updated']
        return datetime.strptime(
            last_updated_time, '%Y/%m/%d %H:%M:%S'
        )

    def __get_future_range(self):
        return self.config['system_info']['google_calendar_future_range']

    def __get_event_from_google_calendar(
            self, last_updated_time: datetime, future_range: str) -> list:
        # 讀取google 日曆的最後更新時間到未來近一個月的所有活動，
        # 得到日曆的title, url, content, date, updated_time。
        google_calendar_repo = GoogleCalendarRepo()
        events = google_calendar_repo.query_calendar(
            last_updated_time, future_range)
        return events

    def __get_rows_from_notion_database(
            self, last_updated_time: str) -> list:
        print('__get_rows_from_notion_database')
        notion_repo = NotionRepo()
        rows = notion_repo.query_database_where_has_link()
        return rows

    def _grouping_event_list(
            self, event_list: list, notion_rows: list) -> list:
        # 將event list分兩群：待更新跟待新增的事件
        notion_links = []
        for element in notion_rows:
            notion_links.append(element.get('google_link_of_page'))

        new_event = []
        updated_event = []
        for element in event_list:
            if element['link'] in notion_links:
                updated_event.append(element)
            else:
                new_event.append(element)

        new_event_for_notion_format = \
            self.__transfer_new_event(new_event)
        updated_event_for_notion_format = \
            self.__transfer_updated_event(updated_event, notion_rows)

        print(updated_event_for_notion_format)
        return new_event_for_notion_format, updated_event_for_notion_format

    def __transfer_new_event(self, new_event:list) -> list:
        ret = []

        for event in new_event:
            tmp = {}
            tmp['description'] = event.get('description')
            tmp['properties'] = {
                '連結': {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": event['link'],
                                "link": {
                                    "url": event['link']
                                }
                            }
                        }
                    ]
                },
                'Tags': {
                    "multi_select": [
                        {
                            "name": event['status']
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": event['start'],
                        "end": event['end']
                    }
                },
                'Name': {
                    'title': [
                        {
                            'text': {
                                'content': event['title']
                            },
                        },
                    ],
                },
            }
            ret.append(tmp)

        return ret

    def __transfer_updated_event(
            self, updated_event: list, notion_rows: list) -> list:
        ret = []
        for event in updated_event:
            tmp = {}
            tmp['row_id'] = self.__get_row_id(event, notion_rows)
            tmp['properties'] = {
                '連結': {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": event['link'],
                                "link": {
                                    "url": event['link']
                                }
                            }
                        }
                    ]
                },
                'Tags': {
                    "multi_select": [
                        {
                            "name": event['status']
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": event['start'],
                        "end": event['end']
                    }
                },
                'Name': {
                    'title': [
                        {
                            'text': {
                                'content': event['title']
                            },
                        },
                    ],
                },
            }
            ret.append(tmp)
        return ret

    def __get_row_id(self, event: list, notion_rows: list) -> str:
        for row in notion_rows:
            if event['link'] == row.get('google_link_of_page'):
                return row['row_id']

    def __update_row_in_notion_database(
            self, event_list: list):
        # 更新page in database
        print('__update_row_in_notion_database')
        print(f'updated event list = {event_list}')
        notion_repo = NotionRepo()
        notion_repo.update_row_in_database(event_list)


    def __append_row_to_notion_database(
            self, event_list: list):
        # 新增page in database
        print('__append_row_to_notion_database')
        print(event_list)
        notion_repo = NotionRepo()
        notion_repo.insert_row_to_database(event_list)

    def __update_last_updated_time_at_config(self):
        # 更新設定檔的時間，設定成現在
        print("__update_last_updated_time_at_config")
