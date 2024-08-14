import matplotlib.pyplot as plt
import matplotlib
from flask_restful import Resource
from flask_security import auth_token_required, roles_required, roles_accepted, current_user
from sqlalchemy import asc,desc
from flask import make_response, jsonify, request as req
from applications.models import *
matplotlib.use("Agg")

class stat(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        books=db.session.query(BOOKS.name,BOOKS.rating).order_by(desc(BOOKS.rating)).limit(10).all()
        bookname,rating=[],[]
        for book in books:
            bookname.append(book.name)
            rating.append(book.rating)
        #plt.switch_backend('Agg')
        plt.clf()
        #plt.figure()
        plt.bar(bookname,rating,color='skyblue')
        plt.title('TOP 10 RATED BOOKS')
        plt.savefig('../FRONTEND/src/assets/stat.png')
        return make_response(jsonify({'message':'updated statistics page'},200))
