# google_calendar_to_notion
Auto sync event of google calendar to notion database



## build command 
python3 -m PyInstaller --add-data "docs/auth.json:docs" --add-data "docs/config.ini:docs"  --hidden-import libs --add-data "commands/context.py:commands" --distpath exec commands/sync_event_to_notion.py