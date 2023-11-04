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

police_schema = PoliceSchema()
polices_schema = PoliceSchema(many=True)
criminal_schema = CriminalSchema()
criminals_schema = CriminalSchema(many=True)
detection_schema = DetectionSchema()
detections_schema = DetectionSchema(many=True)

Criminal.listDetection = db.relationship('Detection', uselist=True)
Police.criminalsDetained = db.relationship('Criminal',uselist=True)
Detection.criminalDection = db.relationship('Criminal', backref='detection')


#login
@app.route('/login/<dni>/<password>', methods=['POST'])
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


#GET
@app.route('/polices', methods=['GET'])
def get_polices():
  polices = Police.query.all()
  result = polices_schema.dump(polices)
  return jsonify({"polices": result,"total": len(result)})

@app.route('/detections', methods=['GET'])
def get_detections():
  detections = Detection.query.all()
  result = detections_schema.dump(detections)
  return jsonify({"detections": result,"total": len(result)})

@app.route('/policesFilterDni/<dni>', methods=['GET'])
def get_polices_filter_dni(dni):
  polices = Police.query.filter(Police.dni.like(f'%{dni}%')).all()
  result = polices_schema.dump(polices)
  return jsonify({"polices": result,"total": len(result)})

@app.route('/criminalsFilterDni/<dni>', methods=['GET'])
def criminalsFilterDni(dni):
  criminal = Criminal.query.filter(Criminal.dni.like(f'%{dni}%')).all()
  result = criminals_schema.dump(criminal)
  listDetection = detections_schema.dump(criminal[0].listDetection)
  return jsonify({"criminals": result,"total": len(criminal[0].listDetection), "dossier": listDetection})

@app.route('/policeInformation/<dni>', methods=['GET'])
def policeInformation(dni):
  print(dni)
  police = Police.query.filter_by(dni=dni).first()
  data = police_schema.dump(police)
  criminals = criminals_schema.dump(police.criminalsDetained)
  return jsonify({"police": data,"criminalsArrests":criminals, "total": len(criminals)})

@app.route('/criminals', methods=['GET'])
def get_criminals():
  criminals = Criminal.query.all()
  result = criminals_schema.dump(criminals)
  return jsonify({"criminals": result,"total": len(result)})

@app.route('/dataSession/<token>', methods=['Post'])
def get_data(token):
  return jsonify({"data": JwtService.checkJWT(token) })

@app.route('/myArrests', methods=['GET'])
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

@app.route('/myPlatoon', methods=['GET'])
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

@app.route('/mySupervisor', methods=['GET'])
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

@app.route('/detectionCriminalList/<dni>', methods=['GET'])
def detectionCriminalList(dni):
    try:
      criminal = Criminal.query.filter_by(dni=dni).first()
      detections = Detection.query.filter_by(id_criminal=criminal.id).all()
      result = detections_schema.dump(detections)
      return jsonify({"detections": result, "total": len(result)})
    except Exception as e:
      return jsonify({"message": "Error"})

#POST
@app.route('/police', methods=['POST'])
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

@app.route('/criminal', methods=['POST'])
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


@app.route('/detection', methods=['POST'])
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


#DELETE
#PUT
@app.route('/police', methods=['PUT'])
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

if __name__ == '__main__':
    app.run(debug=True)
    