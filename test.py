import re
from collections import UserDict, UserList

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    
    def __init__(self,value):
        self.value=self.__normalize_phone__(value)
    
    def __normalize_phone__(self, phone:str):
        ptrn=r"[\d\+]+"
        phone=''.join(re.findall(ptrn,phone))
        phone.strip()
        if len(phone) in (11,12):
            phone = '+'+phone
        elif len(phone)==10:
            phone = '+38'+phone
        elif len(phone)==9:
            phone = '+380'+phone
        return phone
    


class Phones(UserList):
    
    def phone_exist(self,phone):
        return phone in self.data

    def set_phone(self,phone):
        self.data.append(phone)
    
    def edit_phone(self, phone, new_phone):
        if self.phone_exist(phone) and not self.phone_exist(new_phone):
            self.data[self.data.index(phone)]=new_phone

    def get_phones(self):
        return self.data
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = Phones()    

    def __str__(self):
        return f"Contact name: {self.name.value:20}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def set_record(self,record:Record):
        self.data[record.name.value]=record

    def get_record(self,record_name):
        if record_name in self.data:
            return self.data.get(record_name)

def main():
    # Створення нової адресної книги
    book = AddressBook()

        # Створення запису для John
    john_record = Record("John")
    john_record.phones.set_phone(Phone("09734567890"))
    john_record.phones.set_phone(Phone("1234567890"))

    # Додавання запису John до адресної книги
    book.set_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.phones.set_phone(Phone("9876543210"))
    jane_record.phones.set_phone(Phone("3809876543211"))
    book.set_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.get_record("John")
    john.phones.edit_phone(Phone("1234567890"), Phone("1112223333"))

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # # Пошук конкретного телефону у записі John
    # found_phone = john.find_phone("5555555555")
    # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # # Видалення запису Jane
    # book.delete("Jane")

if __name__ == "__main__":
    main()