from applications.models import *
from applications.rawfun import raw
from flask_security import auth_token_required
from flask import make_response, jsonify, request as req
from flask_restful import Resource, marshal_with
from applications.marshal_fields import *

class Rating(Resource):
    def post(self):
        a=0
        b=0
        data = req.get_json()
        email = data.get('email')
        book_id = data.get('book_id')
        rating = data.get('rating')
        user = USER.query.filter_by(email=email).first()
        user_id=user.id
        book=BOOKS.query.filter_by(id=book_id).first()
        db.session.add(RATING(uid=user_id,bookid=book_id,rating=rating))
        db.session.commit()
        bookrating=RATING.query.filter_by(bookid=book_id).all()
        for i in bookrating:
            b+=1
            a+=i.rating
            print(a/b)
        book.rating=a/b
        db.session.commit()
        return make_response(jsonify('Rating Added Sucessfully'),200)