# 同步calendar event 至notion
from configobj import ConfigObj
import context 

class CalendarToNotionService(object):

    def __init__(self):
        self.config = ConfigObj(
            f'{context.PROJECT_ROOT_PATH}/docs/config.ini',
            encoding='utf-8'
        )

    def handle(self):
        last_updated_time = self.__get_last_updated_time()

        # 1. 讀取google 日曆的讀取config.ini的最後更新時間到未來近一個月的所有活動，
        # 得到日曆的title, url, content, date, updated_time。
        event_list = self.__get_event_from_google_calendar(last_updated_time)
        # 1.1. 若活動的lasted_edited_time小於最後更新時間，則跳過此活動（因為沒更新）
        # 1.2. 若活動的lasted_edited_time大於最後更新時間，則此活動（因為有更新）

        # 2. 使用notion api，get database rows
        notion_rows = self.__get_rows_from_notion_database(last_updated_time)
        # 3.拿到url和page_id後，跟日曆的url做比較，得到要更新的page_id，
        # 以及哪些活動要新增、哪些page的tag要改成取消

        be_updated_event_list, be_appended_event_list = \
            self.__grouping_event_list(
                event_list, notion_rows)

        # todo 
        # 待更新的事件，補上page_id

        # 4. 更新notion, 新增notion
        self.__update_row_in_notion_database(
            be_updated_event_list)
        self.__append_row_to_notion_database(be_appended_event_list)
        # 5. 更新設定檔

        self.__update_last_updated_time_at_config()

    def __get_last_updated_time(self):
        return self.config['system_info']['last_updated']

        # 5.config.ini設定成現在

    def __get_event_from_google_calendar(
        self, last_updated_time:str ) -> list:
        print('__get_event_from_google_calendar')

    def __get_rows_from_notion_database(
        self, last_updated_time:str ) -> list:
        print('__get_rows_from_notion_database')

    def __grouping_updated_page_id_from_event_list(
        self, event_list: list, notion_rows:list) -> list
        # 將event list分兩群：待更新跟待新增的事件
        # 
        print("__grouping_updated_page_id_from_event_list")


    def __update_last_updated_time_at_config(self):
        print("__update_last_updated_time_at_config")
