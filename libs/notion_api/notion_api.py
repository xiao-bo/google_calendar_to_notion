import requests
from requests.auth import HTTPBasicAuth
import os
from notion_client import Client
import json
from configobj import ConfigObj
import context


class NotionAPI(object):
    def __init__(self, page_size: int):
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
        self.__page_size = page_size

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

    def updatePage(self, pageId:str, updateData:dict) -> dict:
        updateUrl = f"https://api.notion.com/v1/pages/{pageId}"
        data = json.dumps(updateData)

        response = requests.request(
            "PATCH", updateUrl, headers=self.headers, data=data
        )
        return response


    def insert_page(self, insertData):
        json_data = {
            'parent': {
                'database_id': self.__DATABASE_ID
            },

            'properties': insertData
        }
        response = requests.post(
            'https://api.notion.com/v1/pages',
            headers=self.headers, json=json_data
        )
        return response


    def insert_content_of_page(self, page_id, row):

        response = requests.patch(
            f'https://api.notion.com/v1/blocks/{page_id}/children',
            headers=self.headers, json=row)

        return response





