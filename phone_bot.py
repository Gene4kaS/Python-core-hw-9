phonebook = []

def handler_error(func):
    def print_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return e.args[0]
        except IndexError :
            return 'Please input: name and phone'
        except TypeError:
            return 'Wrong type of command.'
        except KeyError:
            return 'Wrong name'  
        except Exception as e:
            return e.args  
    return print_error

def read_phonebook():
    with open('phonebook.txt') as f:
        line = f.readlines()
    for phone_line in line:
        contact = (phone_line.replace('\n','')).split(' ')
        phonebook.append({'name': contact[0], 'phone': contact[1]})

def add_phonebook(name, phone):
    with open('phonebook.txt', 'a') as f:
        f.write(f'{name} {phone}\n')
        print(f'{name} with phone number {phone} added to phonebook.')
        read_phonebook()

def change_phonebook(name, phone):
    for phone_number in phonebook:
        if phone_number['name'].lower() == name.lower():
              phone_number['phone'] = phone
    with open('phonebook.txt', 'w') as f:
        for phone_number in phonebook:
            f.write(f"{phone_number['name']} {phone_number['phone']}\n")
        print(f"{name}'s phone number changed.")
        read_phonebook()

def remove_phonebook(name):
    for contact in phonebook:
        if contact['name'].lower() == name.lower():
            phonebook.remove(contact)
    with open('phonebook.txt', 'w') as f:
        for contact in phonebook:
            f.write(f"{contact['name']} {contact['phone']}\n")
        print(f"{name} deleted.")
        read_phonebook()

def check_args(count_args=None, name=None, phone=None, *args):
    if count_args == 1:
        if not name:
            raise ValueError('Enter user name')
    elif count_args == 2:
        if not (name and phone):
            raise ValueError('Write the name and phone, please')
    return True


@handler_error
def func_hello():
    return 'How can I help you?'

@handler_error
def func_exit():
    print('Good bye!')
    exit()

@handler_error
def func_add(name=None, phone=None, *args):
    check_args(2, name, phone, *args)
    add_phonebook(name, phone)
    return True

@handler_error
def func_change(name=None, phone=None, *args):
    check_args(2, name, phone, *args)
    change_phonebook(name, phone)
    return True

@handler_error
def func_remove(name=None, *args):
    check_args(1, name, *args)
    remove_phonebook(name)
    return True

@handler_error
def func_phone(name=None, *args):
    check_args(1, name, *args)
    for contacts in phonebook:
        if contacts['name'].lower() == name.lower():
            print(contacts['name'], ' has phone number: ', contacts['phone'])
    return True

@handler_error
def func_show_all():
    print('-'*43)
    print('|{:^20}|{:^20}|'.format('Name', 'Phone'))
    print('-'*43)
    for element in phonebook:
        print('|{:^20}|{:^20}|'.format(element['name'], element['phone']))
    print('-'*43)
    return True

def func_help():
    print('Commands:')
    print('hello')
    print('add <name> <phone>')
    print('change <name> <phone>')
    print('remove <name>')
    print('phone <name>')
    print('show all')
    print('good bye || close || exit')
    return True


@handler_error
def handler(cmd):
    command = cmd.split(' ')
    if command[0].lower() in handler_command:
        return handler_command[command[0].lower()](*command[1:])
    elif (' '.join(command[0:2]).lower()) in handler_command:
        return handler_command[' '.join(command[0:2]).lower()](*command[2:])
    else:
        raise IndexError


handler_command = {
    'hello': func_hello, 
    'add': func_add, 
    'change': func_change, 
    'remove': func_remove,
    'phone': func_phone,
    'show all': func_show_all,
    'exit': func_exit, 
    'close': func_exit, 
    'good buy': func_exit,
    'help': func_help
    }


def main():
    read_phonebook()
    while True:
        cmd = input('Enter command (help - show all commands): ')
        if not handler(cmd):
            break

if __name__ == '__main__':
    main()