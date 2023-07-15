import pytest
import datetime
from tests import context
from libs.service.calendar_to_notion_service import (
    CalendarToNotionService
)


def get_event_list():
    event_list = [
        {
            'start': '2023-07-04T20:00:00+08:00',
            'end': '2023-07-04T21:00:00+08:00',
            'title': '剪頭髮',
            'status': 'confirmed',
            'updated': datetime.datetime(2023, 7, 3, 11, 43, 5, 609000),
            'link': 'https://www.google.com/calendar/event?eid=cjhyNzFsMWMyMG4xZ3N2NDQxNHFvamo0cTQgYXk4NTI4NTJAbQ',
            'description': None
        },
        {
            'start': '2023-07-07',
            'end': '2023-07-08',
            'title': '婉琦生日',
            'status': 'confirmed',
            'updated': datetime.datetime(2021, 7, 23, 6, 15, 43, 428000),
            'link': 'https://www.google.com/calendar/event?eid=M2M1cG84bGFva3J0MGVlaDBscWN1bGx2MmFfMjAyMzA3MDcgYXk4NTI4NTJAbQ',
            'description': '讚讚'
        },
        {
            'start': '2023-07-07',
            'end': '2023-07-08',
            'title': '小牛晨瑞生日',
            'status': 'confirmed',
            'updated': datetime.datetime(2021, 7, 23, 6, 16, 21, 89000),
            'link': 'https://www.google.com/calendar/event?eid=NHI2ZHI1Mm03aXJrbWFnNmNxc2tzaTI1bjRfMjAyMzA3MDcgYXk4NTI4NTJAbQ',
            'description': None
        }
    ]
    return event_list


def get_notion_rows():
    notion_rows = [
        {
            "row_id": "a13f17a0-e1c6-4a3f-a21f-345ce5a1b875",
            "properties": {
                "連結": {
                    "id": "%60Zfm",
                    "type": "rich_text",
                    "rich_text": [

                    ]
                },
                "Tags":{
                    "id": "iq%3A%40",
                    "type": "multi_select",
                    "multi_select": [

                    ]
                },
                "Date":{
                    "id": "tGzW",
                    "type": "date",
                    "date": "None"
                },
                "Name": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": "321",
                                "link": "None"
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": "321",
                            "href": "None"
                        }
                    ]
                }
            }
        },
        {
            "row_id": "dd24788b-2e60-49da-a9fb-b8d1990ed58b",
            "google_link_of_page": "https://www.google.com/calendar/event?eid=NHI2ZHI1Mm03aXJrbWFnNmNxc2tzaTI1bjRfMjAyMzA3MDcgYXk4NTI4NTJAbQ",
            "properties": {
                "連結": {
                    "id": "%60Zfm",
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "https://www.google.com/calendar/event?eid=NHI2ZHI1Mm03aXJrbWFnNmNxc2tzaTI1bjRfMjAyMzA3MDcgYXk4NTI4NTJAbQ",
                                "link": {
                                    "url": "https://www.google.com/calendar/event?eid=NHI2ZHI1Mm03aXJrbWFnNmNxc2tzaTI1bjRfMjAyMzA3MDcgYXk4NTI4NTJAbQ"
                                }
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": "https://www.google.com/calendar/event?eid=NHI2ZHI1Mm03aXJrbWFnNmNxc2tzaTI1bjRfMjAyMzA3MDcgYXk4NTI4NTJAbQ",
                            "href": "https://www.google.com/calendar/event?eid=NHI2ZHI1Mm03aXJrbWFnNmNxc2tzaTI1bjRfMjAyMzA3MDcgYXk4NTI4NTJAbQ"
                        }
                    ]
                },
                "Tags": {
                    "id": "iq%3A%40",
                    "type": "multi_select",
                    "multi_select": [
                        {
                            "id": "419159b7-dcec-4187-b25c-a2e60e37a7b4",
                            "name": "123",
                            "color": "default"
                        }
                    ]
                },
                "Date": {
                    "id": "tGzW",
                    "type": "date",
                    "date": {
                        "start": "2023-06-12T00:00:00.000+08:00",
                        "end": "2023-06-12T13:00:00.000+08:00",
                        "time_zone": "None"
                    }
                },
                "Name": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": "濾水器",
                                "link": "None"
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": "濾水器",
                            "href": "None"
                        }
                    ]
                }
            }
        }
    ]
    return notion_rows


def get_expected_result():
    excepted_new_result = [
        {
            'description': None,
            "properties": {
                "連結": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": 'https://www.google.com/calendar/event?eid=cjhyNzFsMWMyMG4xZ3N2NDQxNHFvamo0cTQgYXk4NTI4NTJAbQ',
                                "link": {
                                    "url": 'https://www.google.com/calendar/event?eid=cjhyNzFsMWMyMG4xZ3N2NDQxNHFvamo0cTQgYXk4NTI4NTJAbQ',
                                }
                            }
                        }
                    ]
                },
                "Tags": {
                    
                    "multi_select": [
                        {
                            "name": "confirmed"
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": "2023-07-04T20:00:00+08:00",
                        "end": "2023-07-04T21:00:00+08:00",
                    }
                },
                'Name': {
                    'title': [
                        {
                            'text': {
                                'content': '剪頭髮',
                            },
                        },
                    ],
                },
            }
        },
        {
            'description': '讚讚',
            "properties": {
                "連結": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": 'https://www.google.com/calendar/event?eid=M2M1cG84bGFva3J0MGVlaDBscWN1bGx2MmFfMjAyMzA3MDcgYXk4NTI4NTJAbQ',
                                "link": {
                                    "url": 'https://www.google.com/calendar/event?eid=M2M1cG84bGFva3J0MGVlaDBscWN1bGx2MmFfMjAyMzA3MDcgYXk4NTI4NTJAbQ',
                                }
                            }
                        }
                    ]
                },
                "Tags": {
                    
                    "multi_select": [
                        {
                            "name": "confirmed"
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": "2023-07-07",
                        "end": "2023-07-08",
                    }
                },
                'Name': {
                    'title': [
                        {
                            'text': {
                                'content': '婉琦生日',
                            },
                        },
                    ],
                },
            }
        },

    ]
    expected_updated_result = [
        {
            "row_id": "dd24788b-2e60-49da-a9fb-b8d1990ed58b",
            "properties": {
                "連結": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": 'https://www.google.com/calendar/event?eid=NHI2ZHI1Mm03aXJrbWFnNmNxc2tzaTI1bjRfMjAyMzA3MDcgYXk4NTI4NTJAbQ',
                                "link": {
                                    "url": 'https://www.google.com/calendar/event?eid=NHI2ZHI1Mm03aXJrbWFnNmNxc2tzaTI1bjRfMjAyMzA3MDcgYXk4NTI4NTJAbQ'
                                }
                            }
                        }
                    ]
                },
                "Tags": {
                    
                    "multi_select": [
                        {
                            "name": "confirmed"
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": "2023-07-07",
                        "end": "2023-07-08",
                    }
                },
                'Name': {
                    'title': [
                        {
                            'text': {
                                'content': '小牛晨瑞生日',
                            },
                        },
                    ],
                },
            }
        },
        
    ]
    return excepted_new_result, expected_updated_result


def test_grouping_event_list():
    event_list = get_event_list()
    notion_rows = get_notion_rows()
    service = CalendarToNotionService()
    excepted_new_result, expected_updated_result = get_expected_result()
    new_event, updated_event = service._grouping_event_list(event_list, notion_rows)
    print('new_event\n\n')
    print(new_event)

    print('excepted_new_result\n\n')
    print(excepted_new_result)
    assert new_event == excepted_new_result
    assert updated_event == expected_updated_result
