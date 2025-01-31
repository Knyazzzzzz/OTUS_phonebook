# открыть файл
# сохранить файл
# показать все контакты
# создать контакт
# найти контакт
# изменить контакт
# удалить контакт
# выход

from pathlib import Path
from csv import DictReader
from pprint import pprint
from csv import DictWriter
from time import process_time_ns


class PhonebookError(Exception):
    pass


class ContactNotFoundError(PhonebookError):
    pass

class Contact:
    name: str
    phone: str
    company: str

    def __init__(self, name: str, phone: str, company: str):
        self.name = name
        self.phone = phone
        self.company = company



class PhoneBook:
    path: Path
    buffer: dict[int, Contact]
    any_changes_made: bool

    def __init__(self, path: Path):
        self.path = path
        self.buffer = {}
        self.any_changes_made = False

    def read_file(self) -> None:
        self.buffer = {}
        with self.path.open(mode="r", encoding='utf-8-sig') as csvfile:
            reader = DictReader(csvfile, delimiter=';')
            for row in reader:
                row_id = row.pop("ID")
                row_id_int = int(row_id)
                contact = Contact(name=row['Name'], phone=row['Phone'], company=row['Company'])
                self.buffer[row_id_int] = contact


    def save_file(self) -> None:
        with self.path.open(mode="w", encoding='utf-8-sig') as csvfile:
            fieldnames = ['ID', 'Name', 'Phone', 'Company']
            writer = DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()
            for row_id, contact in self.buffer.items():
                # for row_id in buffer:
                #   row_content = buffer[row_id]
                data = {
                    'ID': row_id,
                    'Name': contact.name,
                    'Phone': contact.phone,
                    'Company': contact.company,
                }
                writer.writerow(data)
        self.any_changes_made = False

    def create_contact(self, name: str, phone: str, company: str) -> None:
        last_id = max(self.buffer.keys())
        next_id = last_id + 1
        new_contact = Contact(name=name, phone=phone, company=company)
        self.buffer[next_id] = new_contact
        self.any_changes_made = True

    def delete_contact(self, id_: int) -> None:
        try:
            del self.buffer[id_]
            self.any_changes_made = True
        except KeyError:
            raise ContactNotFoundError

    def update_contact(self, id_contact: int, name: str, phone: str, company: str) -> None:
        self.buffer[id_contact] = Contact(name=name, phone=phone, company=company)
        self.any_changes_made = True

    def find_contact(self, search_data: str) -> dict[int, Contact]:
        search_results = {}
        for row_id, contact in self.buffer.items():
            content_values = [contact.name, contact.phone, contact.company]
            for value in content_values:
                if search_data.lower() in value.lower():
                    search_results[row_id] = contact
                    break
        return search_results

    def give_all_contacts(self) -> dict[int, Contact]:
        return self.buffer

    def get_contact(self, id_: int) -> Contact:
        try:
            contact = self.buffer[id_]
            return contact
        except KeyError:
            raise ContactNotFoundError


if __name__ == '__main__':

    phonebook_one = PhoneBook(path=Path('data/input_data.csv'))

    # buffer = read_file(Path('data/input_data.csv'))
    phonebook_one.read_file()
    phonebook_one.create_contact(name='Peter', phone='13212', company='MIEE')
    result = phonebook_one.find_contact('Peter')

    phonebook_two = PhoneBook(path=Path('data/input_data2.csv'))
    phonebook_two.read_file()
    results2 = phonebook_two.give_all_contacts()

    print(result)
    print(results2)
















    # buffer = {
    #     1: {'Name': 'Pupkin', 'Phone': '', 'Company': ''},
    #
    # }
    #
    # create_contact(buffer, name='Rooney', phone='4564564560', company='Manchester United')
    # save_file(buffer, Path('data/input_data_test.csv'))
    # create_contact(buffer, name='Rooney', phone='4564564560', company='Manchester United')
    # save_file(buffer, Path('data/input_data_test.csv'))
    # telephone_book_path = Path('data/input_data_test.csv')
    # result = read_file(telephone_book_path)
    # pprint(result)
