'''Gets birsdays for nearest week'''

from datetime import date
from datetime import datetime
from collections import UserDict

class BirthdayShift(UserDict):
    '''BirthdayShift keeps info of celebration shift'''
    def __init__(self, shift_to, shift_from):
        self.shift_to = shift_to
        self.shift_from=shift_from
        super().__init__(self)

    def is_shift_day(self, dayofweek):
        '''check if given day is to be shifted'''
        if self.shift_to is not None or self.shift_to is not None:
            return False
        
        return dayofweek in self.shift_from

default_birthday_shift = BirthdayShift('Monday', ['Saturday', 'Sunday'])

# data format: {'Monday': ['Bill Gates'], 'Thursday': ['Jan Koum']}
def format_birthdays(data):
    '''Formats agregated data for print'''
    lines=[]
    for day, names in data.items():
        names=", ".join(names)
        lines.append(f"{day}: {names}")

    return "\n".join(lines)

def get_birthday_weekday(birthday:date, shift:BirthdayShift, max_delta=7):
    '''Gets birthday weekday'''
    delta_days = (birthday - date.today()).days

    if delta_days < 0 or delta_days >= max_delta:
        return None

    dayofweek=birthday.strftime('%A')

    if shift.is_shift_day(dayofweek):
        return shift.shift_to

    return dayofweek
