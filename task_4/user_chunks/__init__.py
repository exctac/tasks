"""
Задание 4

Имеется csv-файл вида (данные не упорядочены):

email,name
test1@mail.ru,username1
test2@gmail.com,username2
test3@gmail.com,username3
test4@rambler.ru,username4
test5@ya.ru,username5
...
testN@yahoo.com,usernameN

Используя данные из csv-файла необходимо создать список чанков,
в которых будут содержаться группы кортежей вида (email, username) с условием,
что в каждом чанке почтовые домены не должны повторяться
(в каждом чанке должно аккумулироваться максимальное число email'ов с уникальными доменами).

Формат выходных данных:

(
    (
   	    ( ...@mail.ru, username1 ),
   	    ( ...@gmail.com, username2 ),
   	    ( ...@rambler.ru, username4 ),
   	    ( ...@ya.ru, username5 ),
   	    ...,
   	    ( ...@yahoo.com, usernameN ),
    ),
    (
   	    ( ...@gmail.com, username3 ),
   	    ( ...@rambler.ru, ... ),
   	    ( ...@ya.ru, ... ),
   	    ...,
    ),

    ...

    (
   	    ( ...@mail.ru, ... ),
   	    ( ...@ya.ru, ... ),
    ),
)
"""


import csv
from collections import Counter


__all__ = (
    'build_unique_user_chunks',
)


def build_unique_user_chunks(file):
    content = csv.reader(file, delimiter=',')
    next(content)

    users = Counter([tuple(name) for name in content])
    unique_chunk_all = []

    while True:
        unique_chunk = []
        for user, count in users.items():
            if count and user not in unique_chunk:
                unique_chunk.append(user)
                users[user] -= 1

        if not unique_chunk:
            break

        unique_chunk_all.append(tuple(unique_chunk))

    return tuple(unique_chunk_all)
