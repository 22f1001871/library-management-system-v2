from applications.models import *
from applications.rawfun import raw
from flask_security import auth_token_required
from flask import make_response, jsonify, request as req
from flask_restful import Resource, marshal_with
from applications.marshal_fields import *
from sqlalchemy import or_

class search_section(Resource):
    @marshal_with(section)
    def get(self,srch_word):
        srch_word="%"+raw(srch_word)+"%"
        section=SECTIONS.query.filter(SECTIONS.rawsection.like(srch_word)).all()
        if not section:
            return make_response(jsonify({'message':'Section does not exist'}),404)
        else:
            return section
        
class search_book(Resource):
    def get(self,srch_word,sid):
        srch_word="%"+raw(srch_word)+"%"
        book=BOOKS.query.filter((BOOKS.rawname.like(srch_word)| BOOKS.rawauth.like(srch_word)),BOOKS.section_id==sid).all()
        if not book:
            return make_response(jsonify({'message':'Book does not exist'}),404)
    
        response = []
        for books in book:
            response.append({
                'book_id':books.id,
                'name':books.name,
                'book_description':books.author,
                'price':books.price,
                'user_id':books.user_id,
                'return_date':books.return_date
            })
        return make_response(jsonify(response),200)