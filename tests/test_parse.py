from dateparser.dateparse import (
    parse,
    subDate,
    addDate,
    getDelimeters,
    getDate,
    snapDate,
    getSnapDict,
    format,
)
import datetime
from dateutil.relativedelta import relativedelta


def test_addDay():
    case = "now()+1d"
    expected = datetime.datetime.now()
    expected += datetime.timedelta(days=1)
    actual = parse(case)

    assert actual == expected.strftime("%Y-%m-%dT%H:%M:%SZ")


def test_subDay():
    case = "now()-1d"
    expected = datetime.datetime.now()
    expected -= datetime.timedelta(days=1)
    actual = parse(case)

    assert actual == expected.strftime("%Y-%m-%dT%H:%M:%SZ")


def test_snapDown():
    case = "now()@mon"
    expected = datetime.datetime.now()
    expected = expected.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    actual = parse(case)

    assert actual == expected.strftime("%Y-%m-%dT%H:%M:%SZ")


def testGetDelimeters():
    case = "now()+1d-123y"
    expected = [
        {"sign": "+", "quantity": "1", "unit": "d"},
        {"sign": "-", "quantity": "123", "unit": "y"},
    ]
    actual = getDelimeters(case)
    assert actual == expected


def testGetDate():
    case = "now()@mon"
    expected = datetime.datetime.now()
    actual = getDate(case)
    assert actual.strftime("%Y-%m-%dT%H:%M:%SZ") == expected.strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def testAddDate():
    date = datetime.datetime.now()
    expected = date + datetime.timedelta(days=1)

    unit = "d"
    value = "1"
    actual = addDate(date, unit, value)

    assert actual == expected


def testSubDate():
    date = datetime.datetime.now()
    expected = date + datetime.timedelta(days=-1)

    unit = "d"
    value = "1"

    actual = subDate(date, unit, value)

    assert actual == expected


def testSnapDate():
    date = datetime.datetime.now()
    unit = "mon"

    actual = snapDate(date, unit)
    expected = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    assert actual == expected


def testGetSnapDict():
    unit = "mon"
    expected = {"day": 1, "hour": 0, "minute": 0, "second": 0, "microsecond": 0}
    actual = getSnapDict(unit)

    assert actual == expected


def testFormat():
    date = datetime.datetime.now()
    expected = date.strftime("%Y-%m-%dT%H:%M:%SZ")

    actual = format(date)

    assert actual == expected


def testExamples():
    now = datetime.datetime.now()
    cases = ["now()+1d", "now()-1d", "now()@d", "now()-1y@mon", "now()+10d+12h"]
    addoneday = now + datetime.timedelta(days=1)
    suboneday = now + datetime.timedelta(days=-1)
    snapday = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yearmonth = now - relativedelta(years=1)
    yearmonth = yearmonth.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    addDayHour = now + datetime.timedelta(days=10, hours=12)

    expected = [
        addoneday.strftime("%Y-%m-%dT%H:%M:%SZ"),
        suboneday.strftime("%Y-%m-%dT%H:%M:%SZ"),
        snapday.strftime("%Y-%m-%dT%H:%M:%SZ"),
        yearmonth.strftime("%Y-%m-%dT%H:%M:%SZ"),
        addDayHour.strftime("%Y-%m-%dT%H:%M:%SZ"),
    ]

    for i, case in enumerate(cases):
        actual = parse(case)
        assert actual == expected[i]
