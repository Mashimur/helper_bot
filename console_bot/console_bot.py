number_dictionary = {}

def format_phone_number(func):
    def decorator(phone_numb):
        new_phone_num = func(phone_numb)
        if len(new_phone_num) == 12:
            return f"+{new_phone_num}"
        elif not phone_numb.startswith("+38"):
            return f"+38{new_phone_num}"

    return decorator

@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    new_phone = [str(int(i)) for i in new_phone]
    new_phone = "".join(new_phone)
    return new_phone


def input_error(func):
    def decorator(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return "Enter a username"
        except ValueError:
            return "Phone number was entered incorrectly!"
        except IndexError:
            return "Enter name and phone please!"

    return decorator


@input_error
def hello():
    return "How can I help you?"


@input_error
def setting_number(lst):
    phone = str(lst[-1])
    name = " ".join(lst[:-1])
    phone = sanitize_phone_number(phone)
    if phone:
        number_dictionary[name.title()] = phone
        return f"Contact {name.title()} was created/edited"
    else:
        return ""


@input_error
def show_phone(lst):
    name = " ".join(lst)
    return number_dictionary[name.title()]


@input_error
def show_all_list():
    if len(number_dictionary) == 0:
        return "Phone dictionary is empty"
    text = ""
    for name, phone in number_dictionary.items():
        text += f"{name} {phone}\n"
    return text.strip()


@input_error
def good_bye():
    return "Good bye!"


def help():
    explanation = """Commands:
    1. Start work, enter the command: hello
    2. Add new contact, enter the command: add 'name' 'phone number'
    3. Change the contact, enter the command: change 'name' 'phone number'
    4. View the contact's phone number, enter the command: phone 'name'
    5. View all contacts, enter the command: show all
    6. Finish the job, enter one of the commands: good bye / close / exit
    """
    return explanation


command = {
    "help": help,
    ("add", "change"): setting_number,
    "phone": show_phone,
    "show all": show_all_list,
    "hello": hello,
    ("good bye", "close", "exit"): good_bye
}

@input_error
def main():
    while True:
        entered_command = input("Enter the command: ")
        if entered_command in (".",):
            break
        entered_command = entered_command.lower().split()
        for key in command:
            if entered_command[0] in key:
                print(command[key](entered_command[1:]))


if __name__ == "__main__":
    main()
