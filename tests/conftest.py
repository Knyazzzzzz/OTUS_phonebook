from tempfile import gettempdir
from pathlib import Path
from textwrap import dedent

import pytest
from os import urandom
from phonebook import PhoneBook


@pytest.fixture
def input_file_path():
    temp_dir = Path(gettempdir())
    file_name = urandom(24).hex()
    path = temp_dir / file_name
    path.write_text(dedent("""
        ID;Name;Phone;Company
        1;;1234;Intel
        2;Den;5454;Yandex
        3;Илья;;Мосводоканал
        4;Robert;52134326; yande
        6;Василиса;;1В класс
    """.strip()), encoding="UTF-8")

    yield path

    path.unlink()


@pytest.fixture
def phonebook(input_file_path):
    phonebook = PhoneBook(input_file_path)
    phonebook.read_file()
    yield phonebook