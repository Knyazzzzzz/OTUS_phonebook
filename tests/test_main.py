from unittest.mock import patch
from main import print_content, Contact, input_int, input_bool, main, PhoneBook


def test_print_content(capsys):
    contact = {2: Contact(name='Den', phone='5454', company='Yandex')}
    print_content(contact)
    captured = capsys.readouterr()
    assert captured.out == "Номер записи: 2, Имя: Den, Телефон: 5454, Компания: Yandex\n"


def test_input_int(capsys):
    with patch("builtins.input", side_effect=["Mark", "5"]):
        result = input_int('')

    captured = capsys.readouterr()
    assert captured.out == '\nВведите числовое значение\n'
    assert result == 5


def test_input_bool(capsys):
    with patch("builtins.input", side_effect=["33", "yes"]):
        result = input_bool()

    captured = capsys.readouterr()
    assert captured.out == "Введите ['yes', 'y', '1', 'да'] или ['no', 'n', '0', 'нет']\n"
    assert result == True


def test_main(input_file_path):
    with patch("builtins.input",
               side_effect=["77", "1", "2", "test1", "test2", "test3", "3", "Intel", "4", "22", "2", "Denis", "", "", "6", "5", "44", "3", "7", "yes"]):
        main(input_file_path)
    phonebook = PhoneBook(input_file_path)
    phonebook.read_file()
    all_contacts = phonebook.give_all_contacts()
    assert all_contacts == {
        1: Contact(name='', phone='1234', company='Intel'),
        2: Contact(name='Denis', phone='5454', company='Yandex'),
        4: Contact(name='Robert', phone='52134326', company=' yande'),
        6: Contact(name='Василиса', phone='', company='1В класс'),
        7: Contact(name='test1', phone='test2', company='test3'),
    }
