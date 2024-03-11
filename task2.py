'''Contacts bot'''

def main():
    '''Contacts bot'''
    contacts = {
        # "name": 2312434
    }
    print("Welcome to the assistant bot!")
    while True:
        user_input = input(" > Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        try:
            process_command(contacts, command, args)
        except ValueError as e:
            print(f"Error: {e}")

def process_command(contacts, command, args):
    '''Takes in a number command with its args and performs action with contats list'''
    if command == "hello":
        print("How can I help you?")
    elif command == "add":
        print(add_contact(args, contacts))
    elif command == "change":
        print(change_contact(args, contacts))
    elif command == "phone":
        print(show_phone(args, contacts))
    elif command == "all":
        print(show_all(args, contacts))
    else:
        print("Invalid command.")

def parse_input(user_input):
    '''Parses and normalizes input command'''
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def validate_args_count(args, expected):
    '''Checks args number'''
    if len(args) != expected:
        raise ValueError(
            f'Expected one arg for this command, given: {len(args)}, expected: {expected}'
        )

def must_contain_name(name, contacts):
    '''Checks if given name exists in contacts'''
    if not name in contacts:
        raise ValueError(f'Name not found in contacts: {name}')

def add_contact(args, contacts):
    '''Add row to contacts'''
    validate_args_count(args, 2)
    name, phone = args
    contacts[name] = phone
    return "Contact added."

def show_phone(args, contacts):
    '''Shows phone by given name'''
    validate_args_count(args, 1)
    name = args[0]
    must_contain_name(name, contacts)

    return f"{name}: {contacts[name]}"

def show_all(args, contacts):
    '''Shows all contacts'''
    validate_args_count(args, 0)

    return contacts

def change_contact(args, contacts):
    '''Changes phone by given name'''
    validate_args_count(args, 2)
    name, phone = args

    must_contain_name(name, contacts)
    contacts[name] = phone

    return "Contact updated."

if __name__ == "__main__":
    main()
