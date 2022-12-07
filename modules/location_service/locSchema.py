from marshmallow import Schema, fields

class LocationSchema(Schema):
    person_id = fields.Integer(attribute="person_id")
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")
    creation_time = fields.String(attribute="creation_time")


