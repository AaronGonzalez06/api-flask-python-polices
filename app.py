from config.config import app,db
from flask import request, jsonify
from models.police import Police
from schemas.PoliceSchema import PoliceSchema
import bcrypt
from services.JwtService import JwtService
from models.criminal import Criminal
from schemas.CriminalSchema import CriminalSchema
from models.detection import Detection
from schemas.DetectionSchema import DetectionSchema
from routes.policeRoutes import police_blueprint
from routes.criminalRoute import criminal_blueprint
from routes.detectionRoute import detection_blueprint

Criminal.listDetection = db.relationship('Detection', uselist=True)
Police.criminalsDetained = db.relationship('Criminal',uselist=True)
Detection.criminalDection = db.relationship('Criminal', backref='detection')

app.register_blueprint(police_blueprint, url_prefix='/api')
app.register_blueprint(criminal_blueprint, url_prefix='/api')
app.register_blueprint(detection_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
    