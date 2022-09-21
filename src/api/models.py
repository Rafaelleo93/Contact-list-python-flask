import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


""" MODELOS """

# Tabla intermedia de relación MANY-TO-MANY
contact_group = db.Table('contact_group',
                         db.Column("contact_id", db.Integer, db.ForeignKey(
                             'contact.id'), primary_key=True),
                         db.Column('group_id', db.Integer, db.ForeignKey(
                             'group.id'), primary_key=True)
                         )


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(60), nullable=False)  # Obligatorio
    address = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    update_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    groups = db.relationship('Group', secondary=contact_group, lazy='subquery',
                             backref=db.backref('contacts', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "pokemon_name": self.full_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
            "groups": self.groups  # lista[1,2,3,4]
        }


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)  # obligatorio

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "contacts": self.contact
        }
