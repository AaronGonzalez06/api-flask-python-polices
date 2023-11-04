from config.config import db
from sqlalchemy import Text

class Detection(db.Model):
    __tablename__ = 'detections'
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(255))
    description = db.Column(db.Text)
    id_criminal = db.Column(db.Integer, db.ForeignKey('criminals.id'))
    criminalDection = db.relationship('Criminal', backref='detection')

    def __init__(self, name,description,criminalDection):
        self.name = name
        self.description = description
        self.criminalDection = criminalDection


class Criminal(db.Model):
    __tablename__ = 'criminals'
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(255))
    surname= db.Column(db.String(255))
    phone= db.Column(db.Integer, unique=True)
    dni= db.Column(db.String(255))
    age= db.Column(db.String(255))
    province= db.Column(db.String(255))
    location= db.Column(db.String(255))
    arrests= db.Column(db.Integer)
    id_police = db.Column(db.Integer, db.ForeignKey('police.id'))
    officer = db.relationship('Police', backref='criminals')
    listDetection = db.relationship('Detection', uselist=True)

    def __init__(self, name,surname,phone,dni,age,province,location,arrests,officer):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.dni = dni
        self.age = age
        self.province = province
        self.location = location
        self.officer = officer
        self.arrests = arrests



class Police(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(255))
    surname= db.Column(db.String(255))
    email= db.Column(db.String(255), unique=True)
    phone= db.Column(db.Integer, unique=True)
    dni= db.Column(db.String(255))
    password= db.Column(db.String(255))
    age= db.Column(db.String(255))
    province= db.Column(db.String(255))
    location= db.Column(db.String(255))
    private_office= db.Column(db.String(255))
    id_supervisor = db.Column(db.Integer, db.ForeignKey('police.id'))
    supervisor = db.relationship('Police', remote_side=[id], uselist=False, backref='subordinate')
    criminalsDetained = db.relationship('Criminal',uselist=True)

    def __init__(self, name,surname,email,phone,dni,password,age,province,location,private_office, supervisor=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.dni = dni
        self.password = password
        self.age = age
        self.province = province
        self.location = location
        self.private_office = private_office
        if supervisor:
            self.supervisor = supervisor