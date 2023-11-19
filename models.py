from datetime import datetime

from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


# Category_User = db.Table('category_user',
#                          db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
#                          db.Column("category_id", db.Integer, db.ForeignKey("category.id")))
#
# Course_User = db.Table('course_user',
#                        db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
#                        db.Column("course_id", db.Integer, db.ForeignKey('course.id')))
#
# Class_User = db.Table("class_user",
#                       db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
#                       db.Column("class_id", db.Integer, db.ForeignKey('class.id')))
#
#
# class Course(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#
#     def __repr__(self):
#         return f'<Courses "{self.id}   {self.name}">'
#
#
#
#
#
# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#
#     def __repr__(self):
#         return f'<Category "{self.name}">'
#
#
# class Class(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)

Property_Tenant = db.Table("property_tenant",
                           db.Column("property_id", db.Integer, db.ForeignKey('property.id')),
                           db.Column("tenant_id", db.Integer, db.ForeignKey('tenant.tenant_id'))
                           )

Property_Landlord = db.Table("property_landlord",
                             db.Column("property_id", db.Integer, db.ForeignKey('property.id')),
                             db.Column("landlord_id", db.Integer, db.ForeignKey('landlord.landlord_id'))
                             )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    security_number = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def set_password(self, password):
        """Create hashed password."""
        print(password)
        hashed = generate_password_hash(
            password
        )
        return hashed

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __init__(self, username, password, email, security_number):
        self.username = username
        self.password = self.set_password(password)
        self.email = email
        self.security_number = security_number

    def __repr__(self):
        return f'User: {self.username}' \
               f'email: {self.email}' \
               f'date added: {self.date_added}' \
               f'security number: {self.security_number}'


class Tenant(db.Model):
    tenant_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    def __init__(self,user_id):
        self.user_id=user_id
class Landlord(db.Model):
    landlord_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    def __init__(self,user_id):
        self.user_id=user_id


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    # add columns for other details here


def recreate_all_databases():
    """
    Drops then creates all databases as part of its db object. Therefore, all rows/columns are reset
    Use this instead of drop_all/create_all! This adds things that must be present

    NOTE: DB Browser extension connected to db locks the database. Make sure it's disconnected before running this
    command, or any other command which reads/writes the db
    """
    db.drop_all()
    print("Dropped")
    db.create_all()
    print("Created")
    db.session.commit()
    print("Committed")


if __name__ == '__main__':
    recreate_all_databases()
