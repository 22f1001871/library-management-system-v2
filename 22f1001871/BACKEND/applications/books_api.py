from flask_restful import Resource, marshal_with
from flask import make_response, jsonify, request as req
from flask_security import auth_token_required, roles_required, roles_accepted, current_user
from applications.models import *
from applications.marshal_fields import *
from datetime import datetime,timedelta
from sqlalchemy import asc,desc
from applications.rawfun import raw
from applications.cache import cache



#api to get all sections
class Allsections(Resource):
    @cache.cached(timeout=50)
    @marshal_with(section)  
    def get(self):
        sections = SECTIONS.query.all()
        return sections
    
    
    
#api to get all books
class AllBooks(Resource):
    @cache.cached(timeout=50)
    def get(self):
        Books = BOOKS.query.all()
        response = []
        for book in Books:
            section = SECTIONS.query.get(book.section_id)
            response.append({
                'book_id':book.id,
                'name':book.name,
                'content':book.content,
                'section':{
                    'section_id': section.id,
                    'name':section.name,
                    'description':section.description
                }
            })
        return make_response(jsonify(response),200)
    
    @cache.memoize(50)
    def get(self,id):
        book = BOOKS.query.get(id)
        section = SECTIONS.query.filter_by(id=book.section_id).first()
        if not book:
            return make_response(jsonify({'message':'Book does not exist'}),404)
        response={
            'id':book.id,
            'name':book.name,
            'author':book.author,
            'content':book.content,
            'price':book.price,
            'section_name':section.name
        }
        return make_response(jsonify(response),200)


#api to get  books of particular section
class BookApi(Resource):
    @cache.memoize(50)
    def get(self,id):
        book = BOOKS.query.filter_by(section_id=id).order_by(desc(BOOKS.rating)).all()
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
    

#api to get particualar book
class Book(Resource):

    def get(self,email):
        user=USER.query.filter_by(email=email).first()
        id=user.id
        book = BOOKS.query.get(id)
        section = SECTIONS.query.get(book.section_id)
        if not book:
            return make_response(jsonify({'message':'Book does not exist'}),404)
        response={
            'id':book.id,
            'name':book.name,
            'author':book.author,
            'content':book.content,
            'price':book.price,
            'section_name':section.name
        }
        return make_response(jsonify(response),200)

    #api with role based authentication to add book
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = req.get_json()

        name = data.get('name')
        section_name = data.get('section_name')
        content=data.get('content')
        author=data.get('author')
        price=data.get('price')

        if not name or not section_name:
            return make_response(jsonify({'message':'All fields are required'}),400)
        
        section = SECTIONS.query.filter_by(name=section_name).first()
        if not section:
            return make_response(jsonify({'message':'Section does not exist'}),404)
        
        try:
            book = BOOKS(section_id=section.id,name=name,content=content,author=author,price=price,rawname=raw(name),rawauth=raw(author))
            db.session.add(book)
            db.session.commit()
            response = {
                'message':'Book added successfully',
                'Book':{
                    'Book_id':book.id,
                    'name':book.name,
                    'price':book.price,
                    'author':book.author
                }
            }
            return make_response(jsonify(response),201)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        
    #api with role based access to update book
    @auth_token_required
    @roles_required('admin')
    def put(self,id):
        book = BOOKS.query.get(id)
        if not book:
            return make_response(jsonify({'message':'Book does not exist'}),404)
        
        data = req.get_json()

        name = data.get('name')
        section_name = data.get('section')
        content=data.get('content')
        author=data.get('author')
        selling_price=data.get('price')

        if not name or not section_name or not content or not author or not selling_price:
            return make_response(jsonify({'message':'Edit request is empty with any data'}),400)
        
        if name:
            book.name = name
            book.rawname = raw(name)
        if section_name:
            section = SECTIONS.query.filter_by(name=section_name).first()
            book.section_id = section.id
        if content:
            book.content = content
        if author:
            book.author = author
            book.rawauth = raw(author)
        
        try:
            db.session.commit()
            return make_response(jsonify({'message':'Book updated successfully'}),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        

    #api with role based access to delete particular book
    @auth_token_required
    @roles_required('admin')
    def delete(self,id):
        book = BOOKS.query.get(id)
        if not book:
            return make_response(jsonify({'message':'Book does not exist'}),404)
        
        try:
            db.session.delete(book)
            db.session.commit()
            return make_response(jsonify({'message':'Book deleted successfully'}),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)





#api to ger particular section
class Section(Resource):
    @cache.memoize(5)
    @marshal_with(section)
    def get(self,id):
        section = SECTIONS.query.get(id)
        if not section:
            return make_response(jsonify({'message':'Section does not exist'}),404)
        else:
            return section

     #api with role based access to add a section
    @auth_token_required
    @roles_accepted('admin')
    def post(self):
        data = req.get_json()


        name = data.get('name')
        description = data.get('description')

        # Data Validation
        if not name:
            return make_response(jsonify({'message':'Category Name is required'}),400)
        
        if SECTIONS.query.filter_by(name=name).first():
            return make_response(jsonify({'message':'Section already exists'}),400)

        if current_user.has_role('admin'):
            try:
                section = SECTIONS(name=name,description=description,rawsection=raw(name))
                db.session.add(section)
                db.session.commit()
                response = {
                    'message':'Section added successfully',
                    'category':{
                        'section_id':section.id,
                        'name':section.name,
                        'description':section.description
                    }
                }
                return make_response(jsonify(response),201)

            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)
            
    #role based access to update category        
    @auth_token_required
    @roles_accepted('admin')
    def put(self,id):
        data = req.get_json()

        section = SECTIONS.query.get(id)

        if not section:
            return make_response(jsonify({'message':'section does not exist'}),404)

        name = data.get('name')
        description = data.get('description')

        # Data Validation
        if not name and not description:  
            return make_response(jsonify({'message':'Edit request is empty with any data'}),400)
        
        if current_user.has_role('admin'):
            try:
                if name:
                    section.name = name
                    section.rawsection = raw(name)
                if description:
                    section.description = description
                db.session.commit()
                response = {
                    'message':'Category updated successfully',
                    'category':{
                        'section_id':section.id,
                        'name':section.name,
                        'description':section.description
                    }
                }
                return make_response(jsonify(response),201)

            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)
            
     #role based access to delete section      
    @auth_token_required
    @roles_accepted('admin')
    def delete(self, id):
        section = SECTIONS.query.get(id)

        if not section:
            return make_response(jsonify({'message':'Section does not exist'}),404)
        
        if current_user.has_role('admin'):
            try:
                books = BOOKS.query.filter_by(section_id=id).all()
                for book in books:
                    db.session.delete(book)
                    db.session.commit()
                db.session.delete(section)
                db.session.commit()
                return make_response(jsonify({'message':'Section deleted successfully'}),200)
            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)
        
#role based access to see all requests
class ViewRequests(Resource):
    @auth_token_required
    @roles_accepted('user')
    def post(self):
        recieved_data = req.get_json()
        email = recieved_data.get('email')
        book_id = recieved_data.get('book_id')
        Days = recieved_data.get('no_of_days')
        try:
            user = USER.query.filter_by(email=email).first()
            user_id=user.id
            bo = MYBOOKS.query.filter_by(uid=user_id).all()
            re = REQUESTS.query.filter_by(user_id=user_id).all()
            if(len(bo)+len(re))<=5:
                book=BOOKS.query.filter_by(id=book_id).first()
                book.user_id=user_id
                db.session.commit()
                history=HISTORY(user_id=user_id,book_id=book_id,date_requested=datetime.now())
                db.session.add(history)
                db.session.commit()
                request=REQUESTS(h_id=history.id,user_id=user_id,book_id=book_id,no_of_days=Days,day_requested=datetime.now())
                db.session.add(request)
                db.session.commit()
                response = {
                    'message':'Request added successfully',
                    'Requset':{
                        'reqest_id':request.id,
                        }
                    }
                return make_response(jsonify(response),200)
            else:
                return make_response(jsonify({'message':'You have more amount of books'}),400)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
    
     
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        try:
            requests = REQUESTS.query.all()
            response = []
            for request in requests:
                response.append({
                    'request_id':request.id,
                    'username':request.user_id
                })
            return make_response(jsonify(response),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)

#role based access to veiw particular request        
class Viewbooksapproved(Resource):   
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        try:
            books=MYBOOKS.query.all()
            if not books:
                return make_response(jsonify({'message':'No Approved Reqests'}),404)
            response=[]         
            for book in books:
                req = BOOKS.query.filter_by(id=book.bookid).first()
                response.append({
                'name':req.name,
                'request_id':book.mbid,
                'book_id':req.id,
                'date_requested':req.issued_date,
                'date_returning':req.return_date
                })
            return make_response(jsonify(response),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)

class ViewRequest(Resource):   
    @auth_token_required
    @roles_accepted('user')
    def get(self,email):
        try:
            user = USER.query.filter_by(email=email).first()
            user = user.id
            request = REQUESTS.query.filter_by(user_id=user).all()
            if not request:
                return make_response(jsonify({'message':'Request does not exist'}),404)
            response=[]
            for req in request:
                book = BOOKS.query.filter_by(id=req.book_id).first()
                response.append({
                'name':book.name,
                'date_requested':req.day_requested,
                'days_requested':req.no_of_days
                })
            return make_response(jsonify(response),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)

#role based authentication to approve request
class ApproveRequest(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self,request_id):
        request = REQUESTS.query.get(request_id)
        history = HISTORY.query.filter_by(id=request.h_id).first()
        
        if not request:
            return make_response(jsonify({'message':'Request does not exist'}),404)
        
        
        try:
            book=BOOKS.query.get(request.book_id)
            book.issued_date=datetime.now()
            book.return_date=book.issued_date+timedelta(request.no_of_days)
            bname=book.name
            db.session.add(MYBOOKS(uid=request.user_id,bookid=request.book_id,bname=bname))
            db.session.commit()
            history.access=True
            history.description="access granted"
            history.date_accessed=datetime.now()
            db.session.commit()               
            db.session.delete(request)
            db.session.commit() 
            return make_response(jsonify({'message':'Request Approved successfully'}),200)

        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
            
#role based access to reject a request
class RejectRequest(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self,request_id):
        request = REQUESTS.query.get(request_id)
        history = HISTORY.query.filter_by(id=request.h_id).first()

        if not request:
            return make_response(jsonify({'message':'Request does not exist'}),404)

       
        try:
            book=BOOKS.query.filter_by(id=request.book_id).first()
            book.user_id=0
            history.access=False
            history.description="access denied"
            history.date_accessed=datetime.now()
            history.date_returned=datetime.now()
            db.session.delete(request)
            db.session.commit()
            response = {
                        'message':'Request Rejected',
            }
            return make_response(jsonify(response),200)
        
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
    
#api to get accessed books
class MyBook(Resource):
    def get(self,email):
        user = USER.query.filter_by(email=email).first()
        mybook = MYBOOKS.query.filter_by(uid=user.id).all()
        if not mybook:
            return make_response(jsonify({'message':'Book does not exist'}),404)
        else:
            response=[]
            for book in mybook:
                returndate=BOOKS.query.filter_by(id=book.bookid).first()
                response.append({'name':book.bname,
                                 'bid':book.bookid,
                                 'return_date':returndate.return_date,
                                 'content':returndate.content})
            return make_response(jsonify(response),200)
  
    @auth_token_required
    @roles_accepted('user','admin')
    def delete(self,id):
       book=BOOKS.query.filter_by(id=id).first()
       user=USER.query.filter_by(id=book.user_id).first()
       mybook=MYBOOKS.query.filter_by(bookid=id).first()
       db.session.delete(mybook)
       db.session.commit()
       book.user_id=0
       db.session.commit()
       history=HISTORY.query.filter_by(user_id=user.id).all()
       if not history:
            return make_response(jsonify({'message':'Book does not exist'}),404)
       for his in history:
           if his.access==True:
            his.access=False
            db.session.commit()
            his.description='Book Returned'
            db.session.commit()
            his.date_returned=datetime.now()
            db.session.commit()
            return make_response(jsonify({'message':'Book returned successfully'}),200)
           else:
            continue

class History(Resource):
    @cache.cached(timeout=50)
    @auth_token_required
    def get(self):
        try:
            history = HISTORY.query.all()
            if not history:
                return make_response(jsonify({'message':'History does not exist'}),404)
            response=[]
            for req in history:
                if req.access==False:
                    response.append({
                        'history_id':req.id,
                        'user_id':req.user_id,
                        'book_id':req.book_id,
                        'description':req.description,
                        'date_requested':req.date_requested,
                        'days_requested':req.date_accessed,
                        'date_returned':req.date_returned
                        })
            return make_response(jsonify(response),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)