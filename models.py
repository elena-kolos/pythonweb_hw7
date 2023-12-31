from datetime import datetime
import random

from sqlalchemy import Column, Integer, String, Boolean, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

# Таблиця студентів;
# Таблиця груп;
# Таблиця викладачів;
# Таблиця предметів із вказівкою викладача, який читає предмет;
# Таблиця, де кожен студент має оцінки з предметів із зазначенням коли оцінку отримано;


class Teacher(Base):
    """id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100) UNIQUE NOT NULL"""
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher = Column(String(50))
    # Зв'язок з таблицею disciplines
    disciplines = relationship("Discipline", back_populates="teacher")


class Group(Base):
    """id INTEGER PRIMARY KEY AUTOINCREMENT,
       group_name VARCHAR(100)  NOT NULL"""
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(50), unique=True)
    students = relationship('Student', back_populates='group_name')


class Student(Base):
    """id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100)  NOT NULL,
    group_id REFERENCES groups (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE"""
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student = Column(String(50))
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    group_name = relationship('Group', back_populates='students')
    
  

class Discipline(Base):
    """id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name VARCHAR(100) UNIQUE NOT NULL,
    teacher_id REFERENCES teachers (id)"""
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True, autoincrement=True)
    discipline = Column(String(50), unique=True)    
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))    
    teacher = relationship('Teacher', back_populates='disciplines')


class Grade(Base):
    """id INTEGER PRIMARY KEY AUTOINCREMENT,
    mark INTEGER,
    date_of DATE NOT NULL,
    class_id REFERENCES classes (id),
    student_id REFERENCES students (id)"""
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True, autoincrement=True)    
    grade = Column(Integer)    
    date = Column(Date)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    students = relationship('Student', backref='grades')
    disciplines_id = Column(Integer, ForeignKey('disciplines.id', ondelete='CASCADE'))
    disciplines = relationship('Discipline', backref='grades')




