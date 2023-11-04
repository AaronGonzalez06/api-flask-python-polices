from flask_marshmallow import Marshmallow
from schemas.CriminalSchema import CriminalSchema
ma = Marshmallow()

class DetectionSchema(ma.Schema):
    class Meta:
        fields = [ 'name', 'description','criminalDection']

    criminalDection = ma.Nested('self', exclude=('criminalDection',))