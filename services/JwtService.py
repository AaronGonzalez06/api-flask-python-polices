import jwt

class JwtService():
    def createJWT(name,surname,email,phone,dni,age,province,location,private_office,id_supervisor):
        payload = {
            "name": name,
            "surname": surname,
            "email": email,
            "phone": phone,
            "dni": dni,
            "age": age,
            "province": province,
            "location": location,
            "private_office": private_office,
            "id_supervisor": id_supervisor,
        }
        return jwt.encode(payload,"aaronGonzalezAlvarez",algorithm='HS256')
    
    def checkJWT(token):
        try:
            return jwt.decode(token, "aaronGonzalezAlvarez", algorithms=['HS256'])
        except jwt.DecodeError:
            return "invalid token"