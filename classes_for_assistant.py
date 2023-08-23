from collections import UserDict
from datetime import datetime, date, timedelta
from dateparser import parse
import json


class Field:
    def __init__(self, some_value):
        self._value = None
        self.value = some_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return f'{self.value}'


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def phone_number(self, value):  # для перевірки в візьмемо український номер
        flag = True
        for i in value:
            if i.isdigit() or i in '+':
                continue
            else:
                flag = False
                return f'Wrong number'
        if flag:
            if value.startswith('+38') and len(value) == 13:
                self._value = value
            elif len(value) == 10:
                self._value = value
        else:
            return f'Wrong number'


class Birthday(Field):
    def valid_date(self, value: str):
        try:
            obj_datetime = parse(value)
            return obj_datetime
        except Exception:
            raise 'Wrong data type. Try "dd-mm-yy"'

    @Field.value.setter
    def value(self, value):
        self._value = value


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n=1):
        count = 0
        if n < 0:
            raise ValueError('Value must be positive')
        else:
            for key, value in self.data.items():
                result = f'{key}: {str(value)}'
                yield result
                result = ''
                count += 1
                if count == n:
                    break

    def dump(self):
        with open('AdressBook', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False)

    def load(self):
        with open('AdressBook', 'r', encoding='utf-8') as file:
            self.store = json.load(file)

    def search(self, search_str: str):
        result = []
        for record_id, record in self.records.items():
            if search_str in record:
                result.append(record_id)
        return result




class Record:
    def __init__(self, name: Name, phone: Phone, birthday=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
            self.phone = phone
        if birthday:
            b_date = birthday.valid_date(str(birthday))
            self.birthday = b_date

    def __str__(self):
        return f'{self.name}, {self.phone}, {self.birthday.date()}'

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def delete_phone(self, phone: Phone):
        if phone not in self.phones:
            raise KeyError(f'Wrong number or {phone} frone is not recorded')
        self.phones.remove(phone)

    def change_phone(self, phone: Phone):
        if phone in self.phones:
            indx = self.phones.index(phone)
            self.phones[indx] = phone
        else:
            raise ValueError(f'{phone} is not in record')

    def days_to_birthday(self):
        if self.birthday == None:
            raise "No birthday set for the contact."
        d_now = datetime.now()
        if d_now > self.birthday:
            bday = self.birthday.replace(year=d_now.year + 1)
        return (bday - d_now).days


if __name__ == "__main__":
    name_1 = Name('Bill')
    phone_1 = Phone('1234567890')
    b_day_1 = Birthday('1992-04-04')

    name_2 = Name('serg')
    phone_2 = Phone('1234567890')
    b_day_2 = Birthday('1995.3.2')

    name_3 = Name('Oleg')
    phone_3 = Phone('1234567890')
    b_day_3 = Birthday('2 02 1967')

    name_4 = Name('Max')
    phone_4 = Phone('1234567890')
    b_day_4 = Birthday('19*02*1999')

    rec_1 = Record(name_1, phone_1, b_day_1)
    rec_2 = Record(name_2, phone_2, b_day_2)
    rec_3 = Record(name_3, phone_3, b_day_3)
    rec_4 = Record(name_4, phone_4, b_day_4)
    ab = AddressBook()

    ab.add_record(rec_1)
    ab.add_record(rec_2)
    ab.add_record(rec_3)
    ab.add_record(rec_4)

    print('All Ok')

    for i in ab.iterator(4):
        print(i)

    print(rec_1.days_to_birthday())
    print(rec_2.days_to_birthday())
    print(rec_3.days_to_birthday())
    print(rec_4.days_to_birthday())
