import datetime
from dateutil.relativedelta import relativedelta
import re


units = {
    "d": "days",
    "s": "seconds",
    "h": "hours",
    "m": "minutes",
    "mon": "months",
    "y": "years",
}


def parse(inputString):
    date = getDate(inputString)
    if date:
        delimeters = getDelimeters(inputString)
        print(delimeters)
        for delimeter in delimeters:
            date = applyDelimeter(date, delimeter)
    else:
        return "NA"
    return format(date)


def getDate(inputString):
    if "now()" in inputString:
        return datetime.datetime.now()
    else:
        return False


def getDelimeters(inputString):
    cases = []
    delim = {"sign": "", "quantity": "", "unit": ""}
    inprog = False
    for count, i in enumerate(inputString):
        if i in "+-@":
            if inprog:
                cases.append(delim)
                delim = resetDelim()
            inprog = True
            delim["sign"] = i
        elif i.isdecimal():
            delim["quantity"] += i
        elif inprog:
            delim["unit"] += i
        if count == len(inputString) - 1:
            cases.append(delim)
    return cases


def applyDelimeter(date, delimeter):
    if "+" in delimeter["sign"]:
        date = addDate(date, delimeter["unit"], delimeter["quantity"])
    if "-" in delimeter["sign"]:
        date = subDate(date, delimeter["unit"], delimeter["quantity"])
    if "@" in delimeter["sign"]:
        date = snapDate(date, delimeter["unit"])
    return date


def addDate(date, unit, value):
    incrementValue = {units[unit]: int(value)}
    return date + relativedelta(**incrementValue)


def subDate(date, unit, value):
    decrementValue = {units[unit]: int(value)}
    print(decrementValue)
    print("decdate")
    return date - relativedelta(**decrementValue)


def snapDate(date, unit):
    snapDict = getSnapDict(unit)
    date = date.replace(**snapDict)
    return date


def getSnapDict(unit):
    snapdown = ["year", "month", "day", "hour", "minute", "second", "microsecond"]
    snapValue = units[unit][:-1]
    snaps = snapdown[snapdown.index(snapValue) + 1 :]
    snapDict = {}
    for snap in snaps:
        if snap in ["year", "month", "day"]:
            snapDict[snap] = 1
        else:
            snapDict[snap] = 0
    return snapDict


def format(date):
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


def resetDelim():
    return {"sign": "", "quantity": "", "unit": ""}
