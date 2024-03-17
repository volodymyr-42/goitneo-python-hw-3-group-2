'''AdressBook entities'''
from collections import UserDict
import re
import birthday 
from datetime import date
from datetime import datetime
import calendar

class Field:
    '''Field entity'''
    def __init__(self, value):
        '''Field constructor'''
        self.value = value

    def __str__(self):
        # return ""
        return f"{self.value}"

class Name(Field):
    '''Name entity'''

class Birthday(Field):
    '''Birthday entity'''

    def to_date(self):
        '''Convert value to datetime object'''
        if self.value is None:
            return None
        return datetime.strptime(self.value, '%d.%m.%Y').date()

    def is_empty(self):
        '''Check is valid birthday'''
        return not self.value is None and self.value != ""

    def validate(self):
        '''Validate birthday'''
        if not isinstance(self.value, str):
            t = type(self.value)
            raise ValueError(f'Invalid field type: {t}, expected string')        

        pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        if re.match(pattern, self.value) is None:
            raise ValueError('Invalid date format, expected: DD.MM.YYYY')

        res=self.value.split(".")
        if int(res[0]) > 31:
            raise ValueError('Day can not be greater than 31')
        if int(res[0]) == 0:
            raise ValueError('Day can not be 0')
        if int(res[1]) > 12:
            raise ValueError('Month can not be greater than 31')
        if int(res[1]) == 0:
            raise ValueError('Month can not be 0')
        if int(res[2]) == 0:
            raise ValueError('Year can not be 0')

class Phone(Field):
    '''Phone entity'''

    def validate(self):
        '''Validate phone'''
        if not isinstance(self.value, str):
            t = type(self.value)
            raise ValueError(f'Invalid field type: {t}, expected string of digits')
        if  not self.value.isdigit():
            raise ValueError(f'Invalid value: {self.value}, expected digits only')
        l = len(self.value)
        minlen = 10
        if len(self.value) < minlen:
            t = type(self.value)
            raise ValueError(f'Invalid len: {l}, expected: {minlen}')

class Record:
    '''Record keeps name and phones'''
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None
        self.phones = {}

    def add_phone(self, phone: str):
        '''Add phone to list'''
        p = Phone(phone)
        p.validate()
        self.phones[phone] = p

    def add_birthday(self, value: str):
        '''Add phone to list'''
        b=Birthday(value)
        b.validate()
        self.birthday = b

    def has_birthday(self):
        '''Check if phone in record'''
        return not self.birthday is None

    def remove_phone(self, phone: str):
        '''Remove phone from list'''
        self.phones.pop(phone, None)

    def edit_phone(self, old, newval: str):
        '''Edit phone'''
        if not self.phone_exists(old):
            raise ValueError(f'Can not edit, phone not found: {old}')
        p = Phone(newval)
        p.validate()

        self.phones[old] = p

    def clear_phones(self):
        '''Remove phones'''
        self.phones = {}

    def find_phone(self, v: str):
        '''Find phone'''
        return self.phones.get(v)

    def phone_exists(self, v: str):
        '''Check if phone in record'''
        return v in self.phones

    def __str__(self):
        phones = [str(p) for k, p in self.phones.items()]
        return f"Contact name: {self.name}, phones: {'; '.join(phones)}"

class AddressBook(UserDict):
    '''AddressBook keeps records'''
    def __init__(self):
        self.data = {}
        self.weekend=['Saturday', 'Sunday']
        super().__init__(self)

    def add_record(self, rec: Record):
        '''Add record to address book'''
        self.data[str(rec.name).lower()] = rec

    def find(self, name: str, required=False) -> Record:
        '''Find record by name'''
        r = self.data.get(name.lower())

        if required and r is None:
            raise ValueError(f"Contact '{name}' not found")

        return r

    def delete(self, name: str):
        '''Delete record by name'''
        self.data.pop(name.lower(), None)

    def get_birthdays_per_week(self):
        '''Gets birsdays for nearest week'''
        birthday_shift=birthday.default_birthday_shift
        res = {}
        # exclude shift days from result
        for d in list(calendar.day_name):
            if d not in birthday_shift.shift_from:
                res[d]=[]

        curr_year=date.today().year

        for k, r in self.data.items():
            if not r.has_birthday():
                continue

            # in case if today is last days of year should also check next year
            years_to_check = [curr_year, curr_year+1]
            for year_to_check in years_to_check:
                db = r.birthday.to_date()
                birthday_to_check = db.replace(year=year_to_check)
                dayofweek=birthday.get_birthday_weekday(
                    birthday_to_check, shift=birthday.default_birthday_shift,
                )
                if dayofweek is None:
                    continue
                res[dayofweek].append(f"{r.name} ({r.birthday})")

        return birthday.format_birthdays(res)

    def __str__(self):
        data = [str(d) for k, d in self.data.items()]
        return "\n".join(data)
