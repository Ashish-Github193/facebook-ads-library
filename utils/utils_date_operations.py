import datetime


def get_min_date(month_difference, max_date):
    max_date_obj = datetime.datetime.strptime(max_date, "%Y-%m-%d")
    min_date_obj = max_date_obj - datetime.timedelta(days=month_difference * 30)
    return min_date_obj.strftime("%Y-%m-%d")


def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def check_if_start_is_bigger(start_date, end_date):
    return start_date > end_date
