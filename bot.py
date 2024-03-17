'''Contacts bot'''

def main():
    '''Contacts bot'''
    contacts = {
        "name": 2312434
    }
    print("Welcome to the assistant bot!")
    print_help(None, None)

    while True:
        try:
            user_input = input(" > Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit", "q"]:
                print("Good bye!")
                break

            process_command(contacts, command, args)
        except ValueError as e:
            print_help(None, None)
            print(f"Error: {e}")

def show_all(args, contacts):
    '''Shows all contacts'''

    return contacts

def change_contact(args, contacts):
    '''Changes phone by given name'''
    name, phone = args

    must_contain_name(name, contacts)
    contacts[name] = phone

    return "Contact updated."

def add_contact(args, contacts):
    '''Add row to contacts'''
    name, phone = args
    contacts[name] = phone
    return "Contact added."

def show_phone(args, contacts):
    '''Shows phone by given name'''
    name = args[0]
    must_contain_name(name, contacts)

    return f"{name}: {contacts[name]}"

def greet(args, contacts):
    print_help(args, contacts)
    print("How can I help you?")

commandsMap={}

def print_help(args, contacts):
    '''Print help'''
    print()
    for i, c in commandsMap.items():
        print(f"|{c.command:^10}| {c.description:52}|")
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
def process_command(contacts, command, args):
    '''Takes in a number command with its args and performs action with contats list'''

    if command not in commandsMap:
        raise ValueError("Invalid command.")

    c = commandsMap[command]
    if len(args) != c.expected_args:
        raise ValueError(
            f'Expected one arg for this command, given: {len(args)}, expected: {c.expected_args}'
        )
    res = c.handler(args, contacts)
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
