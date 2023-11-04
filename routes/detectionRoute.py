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

detection_blueprint = Blueprint('detection', __name__)

police_schema = PoliceSchema()
polices_schema = PoliceSchema(many=True)
criminal_schema = CriminalSchema()
criminals_schema = CriminalSchema(many=True)
detection_schema = DetectionSchema()
detections_schema = DetectionSchema(many=True)



@detection_blueprint.route('/detections', methods=['GET'])
def get_detections():
  detections = Detection.query.all()
  result = detections_schema.dump(detections)
  return jsonify({"detections": result,"total": len(result)})

@detection_blueprint.route('/detection', methods=['POST'])
def create_detection():
  token = request.headers.get('Authorization')
  if token is None:
    return jsonify({"message": "You don't have access."})
  else:
    try:
      name = request.json['name']
      description = request.json['description']
      dniCriminal = request.json['dni']
      criminal = Criminal.query.filter_by(dni=dniCriminal).first()
      new_detection= Detection(name,description,criminal)
      db.session.add(new_detection)
      db.session.commit()
      return jsonify({"message": "Add detection"})
    except Exception as e:
      return jsonify({"message": "Error"})