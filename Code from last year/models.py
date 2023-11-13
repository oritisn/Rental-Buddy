import os.path
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import urandom
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import app, db, lm

Category_User = db.Table('category_user',
                         db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
                         db.Column("category_id", db.Integer, db.ForeignKey("category.id")))

Course_User = db.Table('course_user',
                       db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
                       db.Column("course_id", db.Integer, db.ForeignKey('course.id')))

Class_User = db.Table("class_user",
                      db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
                      db.Column("class_id", db.Integer, db.ForeignKey('class.id')))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Courses "{self.id}   {self.name}">'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    category = db.relationship("Category", secondary=Category_User, backref="User")
    courses = db.relationship('Course', secondary=Course_User, backref="User")

    def set_password(self, password):
        """Create hashed password."""
        print(password)
        hashed = generate_password_hash(
            password,
            method='sha256'
        )
        return hashed

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __init__(self, username, password, category, email):
        self.username = username
        self.password = self.set_password(password)
        # self.first_name = first_name
        # self.last_name = last_name
        self.email = email
        self.category.append(db.session.query(Category).filter(Category.name == category).first())

    def __repr__(self):
        return f'User: {self.username}' \
               f'first name: {self.first_name}' \
               f'lastname: {self.last_name}' \
               f'email: {self.email}' \
               f'dateadded: {self.date_added}'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Category "{self.name}">'


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)


def recreate_all_databases():
    """
    Drops then creates all databases as part of its db object. Therefore, all rows/columns are reset
    Use this instead of drop_all/create_all! This adds things that must be present

    NOTE: DB Browser extension connected to db locks the database. Make sure it's disconnected before running this command or any other command which reads/writes the db
    """
    db.drop_all()
    print("Dropped")
    db.create_all()
    print("Created")

    for course in ('IELTS', 'B1', 'Grammar'):
        ToAdd = Course(name=course)
        db.session.add(ToAdd)
        del ToAdd
    print(Course.query.all())
    print("Courses added")
    for category in ('Teacher', 'Student'):
        ToAdd = Category(name=category)
        db.session.add(ToAdd)
        del ToAdd
    print(Category.query.all())
    print("Categories added")
    db.session.commit()
    print("Committed")


if __name__ == '__main__':
    recreate_all_databases()
