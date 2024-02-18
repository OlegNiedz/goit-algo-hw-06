import re
from collections import UserDict, UserList

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phones(UserList):
    
    def __phone_exist__(self,phone:str):
        return phone in self.data

    def __normalize_phone__(self, phone:str):
        ptrn=r"[\d\+]+"
        phone=''.join(re.findall(ptrn,phone))
        phone.strip()
        if len(phone)==12:
            phone = '+'+phone
        elif len(phone)==10:
            phone = '+38'+phone
        elif len(phone)==9:
            phone = '+380'+phone
        return phone
    
    def find_phone(self, phone:str):
        phone=self.__normalize_phone__(phone)
        if self.__phone_exist__(phone):
            return self.data[self.data.index(phone)]
        else:
            print(f"Phone {phone} don't founded")
    
    def set_phone(self,phone:str):
        self.data.append(self.__normalize_phone__(phone))
    
    def edit_phone(self, phone, new_phone=""):
        phone=self.__normalize_phone__(phone)
        if self.__phone_exist__(phone):
            new_phone=self.__normalize_phone__(new_phone)
            if new_phone and not self.__phone_exist__(new_phone):
                self.data[self.data.index(phone)]=new_phone
            else:
                self.data.remove(phone)

    def get_phones(self):
        return self.data
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = Phones()
         

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}"

class AddressBook(UserDict):
    def set_record(self,record:Record):
        self.data[record.name.value]=record
        
    def get_record(self,record_name):
        if record_name in self.data:
            return self.data.get(record_name)
        else:
            print(f"Record {record_name} don't found!")
            return None
    
    def delete_record(self,record_name):
       if record_name in self.data:
            self.data.__delitem__(record_name)

def main():
    # Створення нової адресної книги
    book = AddressBook()

        # Створення запису для John
    john_record = Record("John")
    john_record.phones.set_phone("1234567890")
    john_record.phones.set_phone("5555555555")

    # Додавання запису John до адресної книги
    book.set_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.phones.set_phone("9876543210")
    jane_record.phones.set_phone("3809876543211")
    book.set_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.get_record("John")
    john.phones.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.phones.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete_record("Jane")

    for name, record in book.data.items():
        print(record)

if __name__=='__main__':
    main()