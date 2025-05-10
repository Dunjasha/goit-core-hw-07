from collections import UserDict
from datetime import datetime

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
            self.birthday = datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD-MM-YYYY")
        
    def __str__(self):
       return self.birthday.strftime("%d-%m-%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if self.find_phone(phone):
            raise ValueError(f"Phone number '{phone}' already exists.")
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(new_phone):
            raise ValueError(f"Phone number '{new_phone}' already exists.")
        self.add_phone(new_phone)
        self.remove_phone(old_phone)
        



    
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if not phone:
            raise ValueError(f"Phone number '{phone_number}' not found.")
        self.phones.remove(phone)
    
    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday_str}"
    

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)
        
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Record with name '{name}' not found.")
        
    def get_upcoming_birthdays(self):
        pass

    def __str__(self):
        result = ""
        for record in self.data.values():
            result += str(record) + "\n"
        return result.strip()

        
r = Record("Даніїл")
r.add_phone("0991234567")
r.add_birthday("10-05-2000")

print(r)

r.add_phone("9002461900")

print(r)
