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


class PhonebookError(Exception):
    pass

class ContactNotFoundError(PhonebookError):
    pass


def read_file(input_file_path: Path) -> dict[int, dict]:
    buffer = {}
    with input_file_path.open(mode="r", encoding='utf-8-sig') as csvfile:
        reader = DictReader(csvfile, delimiter=';')
        for row in reader:
            row_id = row.pop("ID")
            row_id_int = int(row_id)
            buffer[row_id_int] = row
    return buffer


def save_file(buffer: dict[int, dict], output_file_path: Path) -> None:
    with output_file_path.open(mode="w", encoding='utf-8-sig') as csvfile:
        fieldnames = ['ID', 'Name', 'Phone', 'Company']
        writer = DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for row_id, row_content in buffer.items():
            # for row_id in buffer:
            #   row_content = buffer[row_id]
            data = {
                'ID': row_id,
                'Name': row_content['Name'],
                'Phone': row_content['Phone'],
                'Company': row_content['Company'],
            }
            writer.writerow(data)


def create_contact(buffer: dict[int, dict], name: str, phone: str, company: str) -> None:
    last_id = max(buffer.keys())
    next_id = last_id + 1

    new_contact = {'Name': name, 'Phone': phone, 'Company': company}
    buffer[next_id] = new_contact


def delete_contact(buffer: dict[int, dict], id_: int) -> None:
    try:
        del buffer[id_]
    except KeyError:
        raise ContactNotFoundError


def update_contact(buffer: dict[int, dict], id_contact: int, name: str, phone: str, company: str) -> None:
    buffer[id_contact] = {
        'Name': name,
        'Phone': phone,
        'Company': company,
    }


def find_contact(buffer: dict[int, dict], search_data: str) -> dict[int, dict]:
    search_results = {}
    for row_id, row_content in buffer.items():
        content_values = row_content.values()
        for value in content_values:
            if search_data.lower() in value.lower():
                search_results[row_id] = row_content
                break
    return search_results

def give_all_contacts(buffer: dict[int, dict]) -> dict[int, dict]:
    return buffer

def get_contact_data(buffer: dict[int, dict], id_: int) -> dict:
    try:
        contact_data = buffer[id_]
        return contact_data
    except KeyError:
        raise ContactNotFoundError


if __name__ == '__main__':
    buffer = read_file(Path('data/input_data.csv'))
    result = find_contact(buffer,search_data='123')

    pprint(result)

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
