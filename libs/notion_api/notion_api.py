import requests
from requests.auth import HTTPBasicAuth
import os
from notion_client import Client
import json
from configobj import ConfigObj
import context


class NotionAPI(object):
    def __init__(self):
        # to do
        # 讀設定檔
        self.config = ConfigObj(
            f'{context.PROJECT_ROOT_PATH}/docs/config.ini',
            encoding='utf-8'
        )
        self.__NOTION_TOKEN = self.config['system_info']['notion_token']

        self.__DATABASE_ID = self.config['system_info']['notion_database']

        self.headers = {
            "Authorization": "Bearer " + self.__NOTION_TOKEN,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.__page_size = 2

    def query_rows_from_database(self):
        url = f"https://api.notion.com/v1/databases/{self.__DATABASE_ID}/query"
        payload = {
            "page_size": self.__page_size,
        }
        ret = []
        while True:
            response = requests.post(
                url, json=payload, headers=self.headers)

            rows = response.json()
            ret.extend(rows['results'])
            if rows['next_cursor'] == None:
                print('no data in notion database')
                break

            payload = {
                "page_size": self.__page_size,
                "start_cursor": rows['next_cursor']
            }

        return ret
