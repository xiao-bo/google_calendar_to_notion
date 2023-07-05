import context

from libs.service.calendar_to_notion_service import CalendarToNotionService


def main():
    print('main')
    cns = CalendarToNotionService()
    cns.handle()


if __name__ == '__main__':
    main()
