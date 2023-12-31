from connect_db import session
from models import Group, Student, Teacher, Discipline, Grade
from sqlalchemy import func, desc


def select_1():
    """ Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    
    result = session.query(Student.student, func.round(func.avg(Grade.grade)).label('avg_grade')).select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    print(result)
   

def select_2(class_id=1):
    """Знайти студента із найвищим середнім балом з певного предмета."""

    result = session.query(Student.student, Discipline.discipline, func.avg(Grade.grade)) \
        .join(Discipline).join(Student). \
        filter(Discipline.id == class_id).group_by(Discipline.id, Student.id).order_by(desc(func.avg(Grade.grade))).first()

    answer = f'{result[0]} : {result[-2]}:{int(result[-1])}'
    print(answer)


def select_3(class_id=2):
    """Знайти середній бал у групах з певного предмета."""

    result = session.query(Discipline.discipline, Group.group_name, func.round(func.avg(Grade.grade), 2)) \
        .select_from(Discipline).join(Grade).join(Student).join(Group) \
        .filter(Discipline.id == class_id).group_by(Discipline.id, Group.id).all()

    print(result)
    for res in result:
        answer = f'Предмет: {res[0]}, Група: {res[1]} : Середній бал: {float(res[-1])}'
        print(answer)


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    result = session.query(func.round(func.avg(Grade.grade), 2)) \
        .select_from(Grade).all()

    for res in result:
        print(f'Cередній бал на потоці: {res[0]}')


def select_5(couch=3):
    """Знайти які курси читає певний викладач."""
 
    result = session.query(Teacher.teacher, Discipline.discipline) \
        .join(Discipline, Teacher.id == Discipline.teacher_id).filter(Teacher.id == couch).group_by(Teacher.id, Discipline.id).all()
    print(result)
     
    for res in result:
        answer = f'Викладач : {res[-2]} читає курси: {res[-1]} '
        print(answer)

def select_6(group=2):
    """Знайти список студентів у певній групі."""
   
    result = session.query(Student.student, Group.group_name) \
        .join(Group, Group.id == Student.group_id).filter(Group.id == group).group_by(Student.id, Group.id).all()
    print(result)
    student_list = []
    for res in result:
        student_fullname = f' {res[-2]}'
        student_list.append(student_fullname)
        answer = f'Студент {student_fullname}:  навчається в групі: {res[-1]} '
        print(answer)
   

def select_7(group=3, clas=3):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    
    result = session.query(Grade.grade, Student.student, Group.group_name, Discipline.discipline) \
        .join(Student, Student.id == Grade.student_id).join(Group, Group.id == Student.group_id).join(Discipline,
                                                                                                     Discipline.id == Grade.disciplines_id) \
        .filter(Group.id == group, Discipline.id == clas).all()
    print(result)
    for res in result:
        student_fullname = f' {res[-3]}'

        answer = f'Студент {student_fullname}:  навчається в групі: {res[-2]} і отримав оцінку {res[0]} з предмету: {res[-1]}. '
        print(answer)


def select_8(couch=2):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    
    result = session.query(Teacher.teacher, func.round(func.avg(Grade.grade), 2)).select_from(Grade) \
        .join(Discipline, Discipline.id == Grade.disciplines_id).join(Teacher, Teacher.id == Discipline.teacher_id) \
        .filter(Teacher.id == couch).group_by(Teacher.teacher).all()
    
    for res in result:
        answer = f'Середній бал {float(res[-1])}, який ставить викладач: {res[-2]} зі своїх предметів.'
        print(answer)


def select_9(student=5):
    """Знайти список курсів, які відвідує певний студент."""
    
    result = session.query(Student.student, Discipline.discipline).select_from(Grade) \
        .join(Discipline, Discipline.id == Grade.disciplines_id).join(Student, Student.id == Grade.student_id) \
        .filter(Student.id == student).group_by(Student.student, Discipline.discipline).all()

    class_list = []
    

    for res in result:
        class_list.append(res[-1])
        answer = f'Kурс: {res[-1]}, який відвідує студент: {res[-2]}.'
        print(answer)
       

def select_10(stud=9, teach=2):
    """Список курсів, які певному студенту читає певний викладач."""
   
    result = session.query(Student.student, Teacher.teacher, Discipline.discipline).select_from(Grade) \
        .join(Discipline, Discipline.id == Grade.disciplines_id).join(Student, Student.id == Grade.student_id).join(Teacher,
                                                                                                  Teacher.id == Discipline.teacher_id) \
        .filter(Student.id == stud, Teacher.id == teach).all()
    
    class_list = []
    student_fullname = []
    teacher_fullname = []
    for res in result:
        student_fullname.append(res[0])
        teacher_fullname.append(res[1])
        class_list.append(res[2])
       
    set_st_fn = set(student_fullname)
    set_t_fn = set(teacher_fullname)
    set_cl = set(class_list)
    str_st_fn = ', '.join(set_st_fn)
    str_t_fn = ', '.join(set_t_fn)
    str_cl = ', '.join(set_cl)
   
    print(f'Kурс: {str_cl}, який відвідує студент: {str_st_fn} у викладача: {str_t_fn}.')

        
queries_dict = {1: select_1, 2: select_2, 3: select_3, 4: select_4, 5: select_5, 6: select_6, 7: select_7, 8: select_8, 9: select_9, 10: select_10}

if __name__ == "__main__":
    while True:
        user_input = input('Choose SQL query: ')
        if user_input == 'exit':
            break
        else:
            try:
                queries_dict.get(int(user_input))()
            except ValueError as err:
                print(f"Incorrect input: {user_input}!!!, Please use integers from 1 to 10")



