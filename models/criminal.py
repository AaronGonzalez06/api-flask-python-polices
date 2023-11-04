from config.config import db

class Criminal(db.Model):
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
    police = db.relationship('Police', remote_side=[id], uselist=False, backref='policeCriminal')

    def __init__(self, name,surname,phone,dni,age,province,location,arrests,police):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.dni = dni
        self.age = age
        self.province = province
        self.location = location
        self.police = police
        self.arrests = arrests