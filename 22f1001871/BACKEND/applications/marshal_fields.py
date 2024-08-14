from flask_restful import fields


section = {
    "id":fields.Integer,
    "name":fields.String,
    "date":fields.DateTime,
    "description":fields.String,
    "rawsection":fields.String
}

