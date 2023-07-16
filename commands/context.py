'''
Set system root path for all test program which import this file
in order to import other libs successfully
'''

from pathlib import Path
import sys

PROJECT_ROOT_PATH = str(Path(__file__).parents[2])

# Append ROOT_PATH_module to system path
if PROJECT_ROOT_PATH not in sys.path:
    # Avoid to append duplicated path to system path.
    sys.path.append(PROJECT_ROOT_PATH)

sys.path.append(str(Path(PROJECT_ROOT_PATH).joinpath('commands')))

