import pytest
from tests import context
from libs.repo.google_repo import GoogleCalendarRepo


def test_transfer_future_range_to_days():
    g = GoogleCalendarRepoTest()

    ret = g._transfer_future_range_to_days('30days')
    assert ret == 30

    ret = g._transfer_future_range_to_days('7days')
    assert ret == 7

    with pytest.raises(Exception) as excinfo:
        ret = g._transfer_future_range_to_days('days')

    error_message = ("invalid literal for int() with base 10: ''")
    assert str(excinfo.value) == error_message

    with pytest.raises(Exception) as excinfo:
        ret = g._transfer_future_range_to_days('7day')

    error_message = ("invalid literal for int() with base 10: '7day'")
    assert str(excinfo.value) == error_message


class GoogleCalendarRepoTest(GoogleCalendarRepo):

    def _init_google_calendar_api(self):
        pass