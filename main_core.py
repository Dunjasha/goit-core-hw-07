    from collections import UserDict
    from datetime import datetime, timedelta

    class Field:
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return str(self.value)

    class Name(Field):
        pass

    class Phone(Field):
        def __init__(self, value):
            if len(value) == 10 and value.isdigit():
                super().__init__(value)
            else:
                raise ValueError("Phone number must be 10 digits long.")

    class Birthday(Field):
        def __init__(self, value):
            try:
                datetime.strptime(value, "%d.%m.%Y")
                super().__init__(value)
            except ValueError:
                raise ValueError("Invalid date format. Use DD.MM.YYYY")

        def to_datetime(self):
            return datetime.strptime(self.value, "%d.%m.%Y")

    class Record:
        def __init__(self, name):
            self.name = Name(name)
            self.phones = []
            self.birthday = None

        def add_phone(self, phone):
            if self.find_phone(phone):
                raise ValueError(f"Phone number '{phone}' already exists.")
            self.phones.append(Phone(phone))

        def add_birthday(self, birthday):
            self.birthday = Birthday(birthday)

        def edit_phone(self, old_phone, new_phone):
            self.remove_phone(old_phone)
            self.add_phone(new_phone)

        def find_phone(self, phone_number):
            for phone in self.phones:
                if phone.value == phone_number:
                    return phone
            return None

        def remove_phone(self, phone_number):
            phone = self.find_phone(phone_number)
            if phone:
                self.phones.remove(phone)
            else:
                raise ValueError(f"Phone number '{phone_number}' not found.")

        def __str__(self):
            phones = '; '.join(p.value for p in self.phones)
            birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
            return f"Contact name: {self.name.value}, phones: {phones}{birthday_str}"

    class AddressBook(UserDict):
        def add_record(self, record):
            self.data[record.name.value] = record

        def find(self, name):
            return self.data.get(name)

        def delete(self, name):
            if name in self.data:
                del self.data[name]

        def get_upcoming_birthdays(self):
            today = datetime.today().date()
            upcoming = []

            for record in self.data.values():
                if not record.birthday:
                    continue

                bday = record.birthday.to_datetime().date()
                bday_this_year = bday.replace(year=today.year)

                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)

                days_diff = (bday_this_year - today).days

                if 0 <= days_diff <= 7:
                    congratulate_date = bday_this_year
                    if congratulate_date.weekday() >= 5:  
                        days_to_monday = 7 - congratulate_date.weekday()
                        congratulate_date += timedelta(days=days_to_monday)
                    upcoming.append({
                        "name": record.name.value,
                        "birthday": congratulate_date.strftime("%d.%m.%Y")
                    })

            return upcoming
        def __str__(self):
            result = []
            for record in self.data.values():
                phones = "; ".join(phone.value for phone in record.phones)
                birthday = f", birthday: {record.birthday.value}" if record.birthday else ""
                result.append(f"Contact name: {record.name.value}, phones: {phones}{birthday}")
            return "\n".join(result) if result else "Address book is empty."
    def input_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, IndexError, KeyError) as e:
                return f"Error: {e}"
        return wrapper

    # Функції для обробки команд
    @input_error
    def add_contact(args, book):
        name, phone = args[0], args[1]
        record = book.find(name)
        if not record:
            record = Record(name)
            book.add_record(record)
            message = "Contact added."
        else:
            message = "Contact updated."
        record.add_phone(phone)
        return message

    @input_error
    def change_contact(args, book):
        name, old_phone, new_phone = args
        record = book.find(name)
        if not record:
            raise KeyError("Contact not found.")
        record.edit_phone(old_phone, new_phone)
        return "Phone updated."

    @input_error
    def show_phone(args, book):
        name = args[0]
        record = book.find(name)
        if not record:
            raise KeyError("Contact not found.")
        return '; '.join(phone.value for phone in record.phones)

    @input_error
    def show_all(book):
        return str(book) if book.data else "Address book is empty."

    @input_error
    def add_birthday(args, book):
        name, bday = args
        record = book.find(name)
        if not record:
            raise KeyError("Contact not found.")
        record.add_birthday(bday)
        return "Birthday added."

    @input_error
    def show_birthday(args, book):
        name = args[0]
        record = book.find(name)
        if not record or not record.birthday:
            raise KeyError("Birthday not found.")
        return record.birthday.value

    @input_error
    def birthdays(args, book):
        upcoming = book.get_upcoming_birthdays()
        if not upcoming:
            return "No upcoming birthdays this week."
        return "\n".join([f"{item['name']} - {item['birthday']}" for item in upcoming])

    def parse_input(user_input):
        parts = user_input.strip().split()
        command = parts[0].lower()
        return command, parts[1:]

    def main():
        book = AddressBook()
        print("Welcome to the assistant bot!")

        while True:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if command in ("close", "exit"):
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")

            elif command == "add":
                print(add_contact(args, book))

            elif command == "change":
                print(change_contact(args, book))

            elif command == "phone":
                print(show_phone(args, book))

            elif command == "all":
                print(show_all(book))

            elif command == "add-birthday":
                print(add_birthday(args, book))

            elif command == "show-birthday":
                print(show_birthday(args, book))

            elif command == "birthdays":
                print(birthdays(args, book))

            else:
                print("Invalid command.")

    if __name__ == "__main__":
        main()
