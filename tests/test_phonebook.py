from pathlib import Path
import pytest
from phonebook import PhoneBook, Contact, ContactNotFoundError


def test_read_file(phonebook: PhoneBook):
    assert len(phonebook.buffer) > 0
    assert phonebook.buffer[2] == Contact(name='Den', phone='5454', company='Yandex')


def test_save_file(input_file_path: Path, phonebook: PhoneBook):
    # :D
    # phonebook.buffer[2] = Contact(name='Knyaz', phone='5454', company='Yandex')
    phonebook.buffer[2].name = 'Knyaz'
    phonebook.save_file()

    file_content = input_file_path.read_text(encoding="utf8")
    lines = file_content.split("\n")

    assert lines[4] == '2;Knyaz;5454;Yandex'


@pytest.mark.parametrize(
    ("name", "phone", "company"),
    [
        ("test1", "test2", "test3"),
        ("", "12345", ""),
        ("","",""),
    ]
)
def test_create_contact(name, phone, company, phonebook: PhoneBook):
    phonebook.create_contact(name=name, phone=phone, company=company)
    assert phonebook.buffer[7] == Contact(name=name, phone=phone, company=company)


def test_delete_contact(phonebook: PhoneBook):
    phonebook.delete_contact(id_=6)
    assert 6 not in phonebook.buffer.keys()


def test_update_contact(phonebook: PhoneBook):
    phonebook.update_contact(id_contact=2, name='test1', phone='test2', company='test3')
    assert phonebook.buffer[2] == Contact(name='test1', phone='test2', company='test3')


def test_find_contact(phonebook: PhoneBook):
    search_results = phonebook.find_contact(search_data='Yand')
    assert search_results == {
        2: Contact(name='Den', phone='5454', company='Yandex'),
        4: Contact(name='Robert', phone='52134326', company=' yande'),
    }


def test_give_all_contacts(phonebook: PhoneBook):
    all_contacts = phonebook.give_all_contacts()
    assert all_contacts == {
        1: Contact(name='', phone='1234', company='Intel'),
        2: Contact(name='Den', phone='5454', company='Yandex'),
        3: Contact(name='Илья', phone='', company='Мосводоканал'),
        4: Contact(name='Robert', phone='52134326', company=' yande'),
        6: Contact(name='Василиса', phone='', company='1В класс'),
    }

def test_get_contact_success(phonebook: PhoneBook):
    contact = phonebook.get_contact(2)
    assert contact == Contact(name='Den', phone='5454', company='Yandex')

def test_get_contact_failure(phonebook: PhoneBook):
    with pytest.raises(ContactNotFoundError):
        phonebook.get_contact(999)
