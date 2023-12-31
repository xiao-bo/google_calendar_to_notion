
from libs.notion_api.notion_api import NotionAPI


class NotionRepo(object):
    def __init__(self):

        self.notion_api = NotionAPI(page_size=2)

    def query_database_where_has_link(self):
        rows = self.notion_api.query_rows_from_database()
        ret = []

        for row in rows:
            tmp = {}
            if row['properties']['連結']['rich_text']:
                tmp['row_id'] = row['id']
                tmp['google_link_of_page'] = (
                    row['properties']['連結']
                    ['rich_text'][0]['text']['content']
                )
                tmp['properties'] = row['properties']
                ret.append(tmp)

        return ret

    def update_row_in_database(self, updated_event):
        for event in updated_event:
            page_id = event.pop('row_id')
            response = self.notion_api.updatePage(
                page_id,
                event
            )
            print(f'update page_id and '
                  f'get response = {response} '
                  )

    def insert_row_to_database(self, new_event: list):
        for event in new_event:
            response = self.notion_api.insert_page(
                event['properties']
            )
            print(f'insert page_id and '
                  f'get response = {response} '
                  )

            if event.get('description'):
                # 如果有備註，拿page_id，新增備註
                self.__insert_content_of_page(response, event)

    def __insert_content_of_page(self, response: dict, event: dict):
        data = {
            'children': [
                {
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'rich_text': [
                            {
                                'type': 'text',
                                'text': {
                                    'content': event['description'],
                                },
                            },
                        ],
                    },
                }
            ]
        }
        page_id = response.json()['id']
        response = self.notion_api.insert_content_of_page(
            page_id, data
        )
        print(response)

    def transfer_new_event(self, new_event: list) -> list:
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

    def transfer_updated_event(
        self, updated_event: list, notion_rows: list
    ) -> list:
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
