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


class PhoneBook:
    path: Path
    buffer: dict[int, dict]

    def __init__(self, path: Path):
        self.path = path
        self.buffer = {}

    def read_file(self) -> None:
        self.buffer = {}
        with self.path.open(mode="r", encoding='utf-8-sig') as csvfile:
            reader = DictReader(csvfile, delimiter=';')
            for row in reader:
                row_id = row.pop("ID")
                row_id_int = int(row_id)
                self.buffer[row_id_int] = row

    def save_file(self) -> None:
        with self.path.open(mode="w", encoding='utf-8-sig') as csvfile:
            fieldnames = ['ID', 'Name', 'Phone', 'Company']
            writer = DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()
            for row_id, row_content in self.buffer.items():
                # for row_id in buffer:
                #   row_content = buffer[row_id]
                data = {
                    'ID': row_id,
                    'Name': row_content['Name'],
                    'Phone': row_content['Phone'],
                    'Company': row_content['Company'],
                }
                writer.writerow(data)

    def create_contact(self, name: str, phone: str, company: str) -> None:
        last_id = max(self.buffer.keys())
        next_id = last_id + 1

        new_contact = {'Name': name, 'Phone': phone, 'Company': company}
        self.buffer[next_id] = new_contact

    def delete_contact(self, id_: int) -> None:
        try:
            del self.buffer[id_]
        except KeyError:
            raise ContactNotFoundError

    def update_contact(self, id_contact: int, name: str, phone: str, company: str) -> None:
        self.buffer[id_contact] = {
            'Name': name,
            'Phone': phone,
            'Company': company,
        }

    def find_contact(self, search_data: str) -> dict[int, dict]:
        search_results = {}
        for row_id, row_content in self.buffer.items():
            content_values = row_content.values()
            for value in content_values:
                if search_data.lower() in value.lower():
                    search_results[row_id] = row_content
                    break
        return search_results

    def give_all_contacts(self) -> dict[int, dict]:
        return self.buffer

    def get_contact_data(self, id_: int) -> dict:
        try:
            contact_data = self.buffer[id_]
            return contact_data
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
