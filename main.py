# User interface
from pathlib import Path
from pprint import pprint

from phonebook_functions import PhoneBook, ContactNotFoundError

# 1 - показать все контакты
# 2 - создать контакт
# 3 - найти контакт
# 4 - изменить контакт
# 5 - удалить контакт
# 6 - сохранить изменения
# 7 - выход


COMMANDS = {
    1: 'Показать все контакты',
    2: 'Создать контакт',
    3: 'Найти контакт',
    4: 'Изменить контакт',
    5: 'Удалить контакт',
    6: 'Сохранить изменения',
    7: 'Выход',
}

TELEPHONE_BOOK_FILE_PATH = Path('data/input_data2.csv')

phonebook = PhoneBook(TELEPHONE_BOOK_FILE_PATH)
phonebook.read_file()

any_changes_made = False


def print_content(contacts: dict[int, dict]) -> None:
    for id_, data in contacts.items():
        name = data['Name']
        phone = data['Phone']
        company = data['Company']
        print(f'Номер записи: {id_}, Имя: {name}, Телефон: {phone}, Компания: {company}')


def input_int(text: str) -> int:
    print(text)
    while True:
        user_input = input()
        if not user_input.isdigit():
            print('Введите числовое значение')
            continue
        user_input = int(user_input)
        return user_input


def input_bool() -> bool:
    yes_answers = ['yes', 'y', '1', 'да']
    no_answers = ['no', 'n', '0', 'нет']
    while True:
        exit_decision = input('').lower()
        if exit_decision in yes_answers:
            return True
        elif exit_decision in no_answers:
            return False

        print(f'Введите {yes_answers} или {no_answers}')


while True:
    print('Выберите действие:')
    for number, description in COMMANDS.items():
        print(f'{number}: {description}')

    choice_int = input_int('Введите номер:')

    # choice = input('Введите номер:')
    # if not choice.isdigit():
    #     print(f'{choice} - недопустимое значение. Введите цифровое значение.')
    #     continue
    # choice_int = int(choice)

    # Проверка на int
    # try:
    #     choice_int = int(choice)
    # except ValueError:
    #     print(f'{choice} - недопустимое значение. Введите цифровое значение.')
    #     continue

    if choice_int not in COMMANDS.keys():
        print("Неправильно выбрано опция, выберите число из предложенного списка")
        print(f'Неправильный выбор:{choice_int}')
        continue

    if choice_int == 1:
        all_contacts = phonebook.give_all_contacts()
        print_content(all_contacts)

    elif choice_int == 2:
        input_name = input('Введите имя:')
        input_phone = input('Введите телефон:')
        input_company = input('Введите название компании:')
        phonebook.create_contact(name=input_name, phone=input_phone, company=input_company)
        any_changes_made = True

    elif choice_int == 3:
        input_data = input('Введите поисковый запрос:')
        search_results = phonebook.find_contact(search_data=input_data)
        print_content(search_results)


    elif choice_int == 4:
        print('Введите ID контакта, который вы хотите измнеить:')
        while True:
            contact_id = input_int('')
            try:
                contact_data = phonebook.get_contact_data(id_=contact_id)
                break
            except ContactNotFoundError:
                print('Контакт не найден. Введите номер существующего контакта')

        changed_name = input('Введите новое имя (нажмите Enter если не хотите вносить изменений в данное поле):')
        changed_phone = input('Введите новый телефон (нажмите Enter если не хотите вносить изменений в данное поле):')
        changed_company = input(
            'Введите новое название компании (нажмите Enter если не хотите вносить изменений в данное поле):')

        if changed_name != '':
            name_to_save = changed_name
        else:
            name_to_save = contact_data['Name']

        if changed_phone != '':
            phone_to_save = changed_phone
        else:
            phone_to_save = contact_data['Phone']

        if changed_company != '':
            company_to_save = changed_company
        else:
            company_to_save = contact_data['Company']
        # company_to_save = changed_company if changed_company != '' else contact_data['Company']

        phonebook.update_contact(id_contact=contact_id, name=name_to_save, phone=phone_to_save, company=company_to_save)
        if changed_name != '' or changed_phone != '' or changed_company != '':
            any_changes_made = True

    elif choice_int == 5:
        print('Введите ID контакта, который вы хотите удалить:')
        while True:
            contact_id = input_int('')
            try:
                phonebook.delete_contact(id_=contact_id)
                break
            except ContactNotFoundError:
                print('Контакт не найден. Введите номер существующего контакта')
        any_changes_made = True

    elif choice_int == 6:
        phonebook.save_file()
        any_changes_made = False

    elif choice_int == 7:
        if not any_changes_made:
            break
        else:
            print('Ваши изменения не были сохранены. Сохранить их? (да/нет)')
            exit_decision = input_bool()
            if exit_decision is True:
                phonebook.save_file()
                break
            else:
                break
