from datetime import datetime

import pytest
import pytz

from app import get_localized_times


def test_get_localized_times():
    utc_time = datetime(2025, 12, 31, 12, 0, 0, tzinfo=pytz.UTC)

    times = get_localized_times(utc_time)

    assert times["utc"] == "2025-12-31 12:00:00.000+00:00"
    assert times["europe"] == "2025-12-31 12:00:00.000+00:00"  # London (GMT)
    assert times["us_east"] == "2025-12-31 07:00:00.000-05:00"  # EST is UTC-5
    assert times["us_west"] == "2025-12-31 04:00:00.000-08:00"  # PST is UTC-8
    assert times["japan"] == "2025-12-31 21:00:00.000+09:00"  # JST is UTC+9
    assert times["taipei"] == "2025-12-31 20:00:00.000+08:00"  # Taipei is UTC+8


def test_summer_time_conversion():
    summer_utc = datetime(2025, 7, 1, 12, 0, 0, tzinfo=pytz.UTC)
    times = get_localized_times(summer_utc)

    assert times["europe"] == "2025-07-01 13:00:00.000+01:00"  # London BST (GMT+1)
    assert times["us_east"] == "2025-07-01 08:00:00.000-04:00"  # EDT is UTC-4
    assert times["us_west"] == "2025-07-01 05:00:00.000-07:00"  # PDT is UTC-7
