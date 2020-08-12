"""
Задание 2

Решение должно быть в виде SQL-запросов (без Python)!

В базе данных содержатся 3 сущности — users, courses и saves:

users [ id, name ]
courses [ id, name ]
saves [ id, user_id, course_id, lesson_no, exercise_no, data ]

Таблица users содержит информацию о пользователях.
Таблица courses содержит информацию об обучающих курсах.
Таблица saves содержит информацию о результатах прохождения различных упражнений пользователями в определенных курсах.
Каждое упражнение характеризуется 3 атрибутами: course_id, lesson_no, exercise_no.
В каждом уроке каждого курса может быть несколько упражнений.
Пользователи могут выполнять каждое упражнение в каждом курсе более одного раза.
В таблице хранится информация обо всех попытках пользователя.

Используя sqlite3 создайте базу данных и соответствующие сущности (напишите SQL для создания таблиц).
Напишите SQL-запрос, результатом которого будет выборка из двух полей: "Имя пользователя" и "Количество пройденных курсов".
Курс считается пройденным, если суммарно по курсу выполнено 100 различных упражнений.
Факт наличия записи в таблице saves — это показатель, что соответствующее упражнение было выполнено пользователем.
"""


import os
from sqlite3 import connect


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))

    with connect(os.path.join(base_dir, 'db.sqlite3')) as conn:
        cursor = conn.cursor()

        # CREATE TABLES
        cursor.executescript("""   
            CREATE TABLE users (
                id integer unsigned not null,
                name varchar(20) not null,
                CONSTRAINT pk PRIMARY KEY (id)
            );
            
            CREATE TABLE courses (
                id integer unsigned not null,
                name varchar(30) not null,
                CONSTRAINT pk PRIMARY KEY (id)
            );
            
            CREATE TABLE saves (
                id integer unsigned not null,
                user_id int unsigned not null, 
                course_id int unsigned not null, 
                lesson_no int unsigned not null, 
                exercise_no int unsigned not null, 
                data text not null,
                CONSTRAINT pk PRIMARY KEY (id),
                CONSTRAINT course_fk FOREIGN KEY (user_id, course_id)
                REFERENCES courses(user_id, course_id) ON DELETE CASCADE 
            );
        """)

        # SELECT DATA
        cursor.execute("""
            SELECT name, count(name) as courses
            FROM (
                    SELECT name
                    FROM saves as s
                    inner join users AS u ON u.id == s.user_id
                    GROUP BY user_id, s.course_id, s.lesson_no
                    HAVING count(distinct s.exercise_no) >= 100
                 )
            GROUP BY name
        """)

        for row in cursor.fetchall():
            print(row)
