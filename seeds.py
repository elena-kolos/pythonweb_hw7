import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from connect_db import session
from models import Teacher, Group, Student, Discipline, Grade
from datetime import datetime

fake = Faker('uk-UA')


def insert_teachers():
    
    for _ in range(5):
        t = Teacher(
            teacher=fake.name(),                   
        )
        session.add(t)


def insert_groups():
   
    group_name1 = Group(group_name='A')
    group_name2 = Group(group_name='B')
    group_name3 = Group(group_name='C')

    session.add_all([group_name1, group_name2, group_name3])


def insert_students():
    
    for _ in range(40):
        s = Student(
            student=fake.name(),
            group_id=random.choice([1, 2, 3])
        )
        session.add(s)


def insert_disciplines():
    
    disc = ['Biology', 'Chemistry', 'Physiology', 'Math', 'Esport']

    for item in disc:
        d = Discipline(
            discipline = item,
            teacher_id=random.randint(1, 5)
        )
        session.add(d)

    
def insert_grades():
    
    for _ in range(200):
        gr = Grade(
            grade = random.randint(5, 12),
            date=fake.date_between(start_date='-1y', end_date='today'),
            student_id = random.randint(1, 40),
            disciplines_id = random.randint(1, 5)           
        )
        session.add(gr)


if __name__ == '__main__':
    try:
        insert_teachers()
        insert_groups()
        insert_students()
        insert_disciplines()
        insert_grades()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
