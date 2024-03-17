'''AdressBook entities'''
from collections import UserDict

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

class Phone(Field):
    '''Phone entity'''
    def validate(self: str):
        '''Add phone to list'''
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
        self.phones = {}

    def add_phone(self, phone: str):
        '''Add phone to list'''
        self.phones[phone] = Phone(phone)

    def remove_phone(self, phone: str):
        '''Remove phone from list'''
        self.phones.pop(phone, None)

    def edit_phone(self, old, newval: str):
        '''Edit phone'''
        if not self.phone_exists(old):
            raise ValueError(f'Can not edit, phone not found: {old}')

        self.phones[old] = Phone(newval)

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
        super().__init__(self)

    def add_record(self, rec: Record):
        '''Add record to address book'''
        self.data[str(rec.name)] = rec

    def find(self, name: str):
        '''Find record by name'''
        return self.data.get(name)

    def delete(self, name: str):
        '''Delete record by name'''
        self.data.pop(name, None)

    def __str__(self):
        data = [str(d) for k, d in self.data.items()]
        return "\n".join(data)
