'''Contacts bot'''

from address_book import AddressBook, Record

def main():
    '''Contacts bot'''
    book = AddressBook()

    r = Record("John")
    r.add_phone("1234567890")
    r.add_phone("5555555555")
    r.add_birthday("19.03.1999")

    book.add_record(r)

    print("Welcome to the assistant bot!")
    print_help(None, None)

    while True:
        try:
            user_input = input(" > Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit", "q"]:
                print("Good bye!")
                break

            process_command(book, command, args)
        except ValueError as e:
            print_help(None, None)
            print(f"Error: {e}")

def show_all(args, book:AddressBook):
    '''Shows all contacts'''

    return str(book)

def change_contact(args, book:AddressBook):
    '''Changes phone by given name'''
    name, phone = args

    r = book.find(name, True)
    r.clear_phones()
    r.add_phone(phone)

    return "Contact updated."

def add_contact(args, book:AddressBook):
    '''Add row to contacts'''
    name, phone = args

    r = Record(name)
    r.add_phone(phone)
    book.add_record(r)

    return "Contact added."

def show_phone(args, book:AddressBook):
    '''Shows phone by given name'''
    name = args[0]
    r = book.find(name, True)
    phones=", ".join(r.phones)

    return f"{name}: {phones}"

def add_birthday(args, book:AddressBook):
    '''Add birthday to contact'''
    name, birthday = args

    r = book.find(name, True)
    r.add_birthday(birthday)

    return "Birthday added."

def show_birthday(args, book:AddressBook):
    '''Shows birthday by given name'''
    name = args[0]
    r = book.find(name, True)

    return f"{name}: {r.birthday}"

def birthdays(args, book:AddressBook):
    '''Gets birsdays for nearest week'''
    print(book.get_birthdays_per_week())

# add-birthday [ім'я] [дата народження]
#show-birthday [ім'я]
# birthdays
def greet(args, book:AddressBook):
    '''Shows greetings'''
    print_help(args, book)
    print("How can I help you?")

commandsMap={}

def print_help(args, book:AddressBook):
    '''Print help'''
    print()
    for i, c in commandsMap.items():
        print(f"|{c.command:^15}| {c.description:65}|")
    print()

class Command:
    def __init__(self, command, expected_args, handler, description):
        self.command = command
        self.expected_args = expected_args
        self.handler = handler
        self.description = description


commands = [
    Command("hello", 0, greet, "greetings"),
    Command("help", 0, print_help, "type 'help' list of commands"),
    Command("add", 2, add_contact, "type 'add [name] [phone]' to add one contact"),
    Command("change", 2, change_contact, "type 'change [name] [phone]' to change one contact"),
    Command("phone", 1, show_phone, "type 'phone [name]' to print contant phone"),
    Command("add-birthday", 2, add_birthday,
            "type 'add-birthday [name] [birthday]' to add contant birthday"),
    Command("show-birthday", 1, show_birthday,
            "type 'show-birthday [name]' to show contant birthday"),
    Command("birthdays", 0, birthdays, "type 'birthdays' to show next week birthdays"),
    Command("all", 0, show_all, "type 'all' to print to print all contacts"),
]
for c in commands:
    commandsMap[c.command] = c

def input_error(func):
    '''This decodator handles errors'''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            print(f"Error: {e}")
            print_help(None, None)

    return inner

@input_error
def process_command(book, command, args):
    '''Takes in a number command with its args and performs action with contats list'''

    if command not in commandsMap:
        raise ValueError("Invalid command.")

    c = commandsMap[command]
    if len(args) != c.expected_args:
        raise ValueError(
            f'Expected one arg for this command, given: {len(args)}, expected: {c.expected_args}'
        )
    res = c.handler(args, book)
    if res is not None:
        print(res)

def parse_input(user_input):
    '''Parses and normalizes input command'''
    if user_input == "":
        raise ValueError("Command can not be empty.")
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def must_contain_name(name, contacts):
    '''Checks if given name exists in contacts'''
    if not name in contacts:
        raise ValueError(f'Name not found in contacts: {name}')

if __name__ == "__main__":
    main()
