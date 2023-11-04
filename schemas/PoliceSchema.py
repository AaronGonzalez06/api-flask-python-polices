from flask_marshmallow import Marshmallow

ma = Marshmallow()

class PoliceSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'surname', 'email', 'phone', 'dni','age', 'province', 'location', 'private_office', 'supervisor']

    supervisor = ma.Nested('self', exclude=('supervisor',))