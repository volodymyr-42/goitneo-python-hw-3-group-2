'''Gets birsdays for nearest week'''

from datetime import date
from datetime import datetime
import calendar

weekend=['Saturday', 'Sunday']

#users: [{"name": "Bill Gates", "birthday": datetime(1955, 10, 28)}]
#returns: {'Monday': ['Bill Gates'], 'Thursday': ['Jan Koum']}
def get_birthdays_per_week(user_list):
    '''Gets birsdays for nearest week'''
    date_format='%Y-%m-%d'

    res = {}
    for d in list(calendar.day_name):
        if d not in weekend:
            res[d]=[]

    curr_year=date.today().year
    for user in user_list:
        name = user["name"]
        birthday= datetime.strptime(user["birthday"], date_format).date()

        # in case if today is last days of year should also check next year
        years_to_check = [curr_year, curr_year+1]
        for year_to_check in years_to_check:
            birthday_to_check = birthday.replace(year=year_to_check)
            dayofweek=get_birthday_per_week(birthday_to_check)
            if dayofweek is None:
                continue
            res[dayofweek].append(name)

    print(format_birthdays(res))
    # return res

# data format: {'Monday': ['Bill Gates'], 'Thursday': ['Jan Koum']}
def format_birthdays(data):
    '''Formats agregated data for print'''
    lines=[]
    for day, names in data.items():
        names=", ".join(names)
        lines.append(f"{day}: {names}")

    return "\n".join(lines)

def get_birthday_per_week(birthday):
    '''Gets weekday within 7 days, shift to Monday if weekend'''
    after_weekend= 'Monday'
    delta_days = (birthday - date.today()).days

    if delta_days < 0:
        return None

    dayofweek=birthday.strftime('%A')

    if delta_days < 5:
        return dayofweek
    if delta_days < 7  and dayofweek in weekend:
        return after_weekend

    return None

if __name__ == "__main__":
    users=[
        {"name": "Bill Gates1", "birthday": "1955-10-28"},
        {"name": "Bill Gates2", "birthday": "1955-01-10"},
        {"name": "Bill Gates3", "birthday": "1955-03-10"},
        {"name": "Bill Gates4", "birthday": "1955-03-11"},
        {"name": "Bill Gates5", "birthday": "1955-03-16"},
        {"name": "Bill Gates6", "birthday": "1955-03-14"},
    ]

    get_birthdays_per_week(users)
