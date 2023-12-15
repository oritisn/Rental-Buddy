from datetime import datetime

from flask_sqlalchemy.session import Session
from sqlalchemy import ForeignKey, delete
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

# Property_Tenant = db.Table("property_tenant",
#                            db.Column("property_id", db.Integer, db.ForeignKey('property.id')),
#                            db.Column("tenant_id", db.Integer, db.ForeignKey('tenant.tenant_id'))
#                            )
# 
# Property_Landlord = db.Table("property_landlord",
#                              db.Column("property_id", db.Integer, db.ForeignKey('property.id')),
#                              db.Column("landlord_id", db.Integer, db.ForeignKey('landlord.landlord_id'))
#                              )
Lease_Tenant = db.Table("lease_tenant",
                        db.Column("lease_id", db.Integer, db.ForeignKey('lease.lease_id')),
                        db.Column("tenant_id", db.Integer, db.ForeignKey('tenant.tenant_id'))
                        )

Lease_Landlord = db.Table("lease_landlord",
                          db.Column("lease_id", db.Integer, db.ForeignKey('lease.lease_id')),
                          db.Column("landlord_id", db.Integer, db.ForeignKey('landlord.landlord_id'))
                          )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
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

    def __init__(self, username, password, email):
        self.username = username
        self.password = self.set_password(password)
        self.email = email

    def __repr__(self):
        return f'User: {self.username}' \
               f'email: {self.email}' \
               f'date added: {self.date_added}'
class Tenant(db.Model):
    tenant_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id


class Landlord(db.Model):
    landlord_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id


class Lease(db.Model):
    lease_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False, unique=True)
    landlord = db.relationship("Landlord", secondary=Lease_Landlord, backref="Lease")

    def __init__(self, file_name, landlord):
        self.file_name = file_name
        self.landlord.append(landlord)

    def __repr__(self):
        return f"{self.lease_id} {self.file_name} {self.landlord}"


# class Property(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     address = db.Column(db.String, nullable=False)
#     # add columns for other details here


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
    db.create_all()

