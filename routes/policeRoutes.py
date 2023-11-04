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

police_blueprint = Blueprint('police', __name__)

police_schema = PoliceSchema()
polices_schema = PoliceSchema(many=True)
criminal_schema = CriminalSchema()
criminals_schema = CriminalSchema(many=True)
detection_schema = DetectionSchema()
detections_schema = DetectionSchema(many=True)

#GET

@police_blueprint.route('/polices', methods=['GET'])
def get_polices():
  polices = Police.query.all()
  result = polices_schema.dump(polices)
  return jsonify({"polices": result,"total": len(result)})

@police_blueprint.route('/login/<dni>/<password>', methods=['POST'])
def login(dni,password):
  #police = Police.query.get(dni)
  try:
    police = Police.query.filter_by(dni=dni).first()
    if bcrypt.checkpw(password.encode('utf-8'), police.password.encode('utf-8')):
      return jsonify({"JWT": JwtService.createJWT(police.name,police.surname,police.email,police.phone,police.dni,police.age,police.province,police.location,police.private_office,police.id_supervisor)})
    else:
      return jsonify({"message": "Incorrect Login."})
  except Exception as e:
    return jsonify({"message": "Incorrect Login."})

@police_blueprint.route('/policesFilterDni/<dni>', methods=['GET'])
def get_polices_filter_dni(dni):
  polices = Police.query.filter(Police.dni.like(f'%{dni}%')).all()
  result = polices_schema.dump(polices)
  return jsonify({"polices": result,"total": len(result)})

@police_blueprint.route('/policeInformation/<dni>', methods=['GET'])
def policeInformation(dni):
  print(dni)
  police = Police.query.filter_by(dni=dni).first()
  data = police_schema.dump(police)
  criminals = criminals_schema.dump(police.criminalsDetained)
  return jsonify({"police": data,"criminalsArrests":criminals, "total": len(criminals)})

@police_blueprint.route('/dataSession/<token>', methods=['Post'])
def get_data(token):
  return jsonify({"data": JwtService.checkJWT(token) })

@police_blueprint.route('/myArrests', methods=['GET'])
def myArrests():
  token = request.headers.get('Authorization')
  if token is None:
    return jsonify({"message": "You don't have access."})
  else:
    policeSession = JwtService.checkJWT(token)
    police = Police.query.filter_by(dni=policeSession['dni']).first()
    criminals = Criminal.query.filter_by(id_police=police.id).all()
    result = criminals_schema.dump(criminals)
    print("resultado: " , criminals)
    return jsonify({"total": len(criminals),"criminals": result})

@police_blueprint.route('/myPlatoon', methods=['GET'])
def myPlatoon():
  token = request.headers.get('Authorization')
  if token is None:
    return jsonify({"message": "You don't have access."})
  else:
    policeSession = JwtService.checkJWT(token)
    police = Police.query.filter_by(dni=policeSession['dni']).first()
    polices = Police.query.filter_by(id_supervisor=police.id).all()
    result = polices_schema.dump(polices)
    return jsonify({"total": len(polices),"polices": result})

@police_blueprint.route('/mySupervisor', methods=['GET'])
def mySupervisor():
  token = request.headers.get('Authorization')
  if token is None:
    return jsonify({"message": "You don't have access."})
  else:
    policeSession = JwtService.checkJWT(token)
    police = Police.query.filter_by(dni=policeSession['dni']).first()
    supervisor = police.supervisor
    result = police_schema.dump(supervisor)
    return jsonify({"supervisor": result})

#POST
@police_blueprint.route('/police', methods=['POST'])
def create_police():
  name = request.json['name']
  surname = request.json['surname']
  email = request.json['email']
  phone = request.json['phone']
  dni = request.json['dni']
  #cifrar password
  pw = request.json['password'].encode('utf-8')
  salt = bcrypt.gensalt()
  Encrypted = bcrypt.hashpw(pw,salt)
  password = Encrypted
  age = request.json['age']
  province = request.json['province']
  location = request.json['location']
  private_office = request.json['private_office']
  id_supervisor = request.json['id_supervisor']
  supervisor = Police.query.get(id_supervisor)
  new_police= Police(name,surname,email,phone,dni,password,age,province,location,private_office,supervisor= supervisor)
  db.session.add(new_police)
  db.session.commit()
  return jsonify({"message": "Add police","JWT": JwtService.createJWT(name,surname,email,phone,dni,age,province,location,private_office,id_supervisor)})


#PUT
@police_blueprint.route('/police', methods=['PUT'])
def update_police():
  token = request.headers.get('Authorization')
  if token is None:
    return jsonify({"message": "You don't have access."})
  else:
    policeSession = JwtService.checkJWT(token)
    police = Police.query.filter_by(dni=policeSession['dni']).first()
    print(police)
    email = request.json['email']
    phone = request.json['phone']
    province = request.json['province']
    location = request.json['location']
    police.email = email
    police.phone = phone
    police.province = province
    police.location = location
    db.session.commit()
    return jsonify({"message": "Update police."})