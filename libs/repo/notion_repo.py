
from libs.notion_api.notion_api import NotionAPI


class NotionRepo(object):
    def __init__(self):

        self.notion_api = NotionAPI()

    def query_database(self):
        rows = self.notion_api.query_rows_from_database()
        ret = []

        for row in rows:
            tmp = {}
            tmp['row_id'] = row['id']
            if row['properties']['連結']['rich_text']:
                tmp['google_link_of_page'] = (
                    row['properties']['連結']
                    ['rich_text'][0]['text']['content']
                )
            tmp['properties'] = row['properties']
            ret.append(tmp)

        return ret
