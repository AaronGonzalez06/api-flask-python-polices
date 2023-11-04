from flask_marshmallow import Marshmallow

ma = Marshmallow()

class CriminalSchema(ma.Schema):
    class Meta:
        fields = [ 'name', 'surname','phone', 'dni','age', 'province','arrests','location','officer']

    officer = ma.Nested('self', exclude=('officer',))