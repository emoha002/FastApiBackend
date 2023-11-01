import datetime


def last_datetime_of_current_year():
    current_year = datetime.datetime.now().year
    return datetime.datetime(current_year, 12, 31, 23, 59, 59)


def get_previous_sunday():
    today = datetime.date.today()

    idx = today.weekday()
    if idx == 6:
        return today
    last_sun = today - datetime.timedelta(days=idx + 1)
    return last_sun
