# 同步calendar event 至notion
from configobj import ConfigObj
import context
from libs.repo.google_repo import GoogleCalendarRepo


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
        '''
        # event is list of object
        # event_list = [{
            "title":xx, 
            "url":xx
        },

        ]
        '''
        # 1.1. 若活動的lasted_edited_time小於最後更新時間，則跳過此活動（因為沒更新）
        # 1.2. 若活動的lasted_edited_time大於最後更新時間，則此活動（因為有更新）

        # 2. 使用notion api，get database rows
        #notion_rows = self.__get_rows_from_notion_database(last_updated_time)

        # 3.拿到url和page_id後，跟日曆的url做比較，得到待新增的page，
        # 和待更新的page（待更新的page包含哪些page的tag要改成取消）
        '''
        be_updated_event_list, be_appended_event_list = \
            self.__grouping_event_list(
                event_list, notion_rows)
        '''
        '''
        # 新增page_id
        be_updated_event_list = [{
            "page_id":'xxx'
            "title":xxx
            }
        ],
        # 沒有page_id
        be_appended_event_list = [{
            "title":xxx
            }
        ]
        '''
        '''
        # 4. 更新notion, 新增notion
        self.__update_row_in_notion_database(
            be_updated_event_list)
        self.__append_row_to_notion_database(
            be_appended_event_list)

        # 5. 更新設定檔
        self.__update_last_updated_time_at_config()
        '''

    def __get_last_updated_time(self):

        return self.config['system_info']['last_updated']

    def __get_future_range(self):
        return self.config['system_info']['google_calendar_future_range']

    def __get_event_from_google_calendar(
            self, last_updated_time: str, future_range: str) -> list:
        # 讀取google 日曆的最後更新時間到未來近一個月的所有活動，
        # 得到日曆的title, url, content, date, updated_time。
        # 1.1. 若活動的lasted_edited_time小於最後更新時間，則跳過此活動（因為沒更新）
        # 1.2. 若活動的lasted_edited_time大於最後更新時間，則此活動（因為有更新）

        print('__get_event_from_google_calendar')
        print(f'last_updated_time = {last_updated_time}')
        print(f'future_range = {future_range}')
        google_calendar_repo = GoogleCalendarRepo()
        events = google_calendar_repo.query_calendar(
            last_updated_time, future_range)

    def __get_rows_from_notion_database(
            self, last_updated_time: str) -> list:
        print('__get_rows_from_notion_database')

    def __grouping_event_list(
            self, event_list: list, notion_rows: list) -> list:
        # 將event list分兩群：待更新跟待新增的事件
        #
        print("__grouping_event_list")
        return 1, 2

    def __update_row_in_notion_database(
            self, event_list):
        # 更新page in database

        print('__update_row_in_notion_database')

    def __append_row_to_notion_database(
            self, event_list):
        # 新增page in database
        print('__append_row_to_notion_database')

    def __update_last_updated_time_at_config(self):
        # 更新設定檔的時間，設定成現在
        print("__update_last_updated_time_at_config")
