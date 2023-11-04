from config.config import db
from flask import Blueprint, jsonify,request
from models.police import Police
from schemas.PoliceSchema import PoliceSchema
import bcrypt
from services.JwtService import JwtService
from models.criminal import Criminal
from schemas.CriminalSchema import CriminalSchema
from models.detection import Detection
from schemas.DetectionSchema import DetectionSchema

criminal_blueprint = Blueprint('criminal', __name__)

police_schema = PoliceSchema()
polices_schema = PoliceSchema(many=True)
criminal_schema = CriminalSchema()
criminals_schema = CriminalSchema(many=True)
detection_schema = DetectionSchema()
detections_schema = DetectionSchema(many=True)

@criminal_blueprint.route('/criminalsFilterDni/<dni>', methods=['GET'])
def criminalsFilterDni(dni):
  criminal = Criminal.query.filter(Criminal.dni.like(f'%{dni}%')).all()
  result = criminals_schema.dump(criminal)
  listDetection = detections_schema.dump(criminal[0].listDetection)
  return jsonify({"criminals": result,"total": len(criminal[0].listDetection), "dossier": listDetection})


@criminal_blueprint.route('/criminals', methods=['GET'])
def get_criminals():
  criminals = Criminal.query.all()
  result = criminals_schema.dump(criminals)
  return jsonify({"criminals": result,"total": len(result)})


@criminal_blueprint.route('/detectionCriminalList/<dni>', methods=['GET'])
def detectionCriminalList(dni):
    try:
      criminal = Criminal.query.filter_by(dni=dni).first()
      detections = Detection.query.filter_by(id_criminal=criminal.id).all()
      result = detections_schema.dump(detections)
      return jsonify({"detections": result, "total": len(result)})
    except Exception as e:
      return jsonify({"message": "Error"})


@criminal_blueprint.route('/criminal', methods=['POST'])
def create_criminal():
  token = request.headers.get('Authorization')
  if token is None:
    return jsonify({"message": "You don't have access."})
  else:
    try:
      policeSession = JwtService.checkJWT(token)
      name = request.json['name']
      surname = request.json['surname']
      phone = request.json['phone']
      dni = request.json['dni']
      age = request.json['age']
      province = request.json['province']
      location = request.json['location']
      arrests = 1
      police = Police.query.filter_by(dni=policeSession['dni']).first()
      print(police)
      new_criminal= Criminal(name,surname,phone,dni,age,province,location,arrests,police)
      db.session.add(new_criminal)
      db.session.commit()
      return jsonify({"message": "Add criminal"})
    except Exception as e:
      return jsonify({"message": "Error"})