from config.config import db
from sqlalchemy import Text

class Detection(db.Model):
    __tablename__ = 'detections'
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(255))
    description = db.Column(db.Text)
    id_criminal = db.Column(db.Integer, db.ForeignKey('criminals.id'))
    criminalDection = None

    def __init__(self, name,description,criminalDection):
        self.name = name
        self.description = description
        self.criminalDection = criminalDection