from config.config import db

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
    criminalsDetained = None

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