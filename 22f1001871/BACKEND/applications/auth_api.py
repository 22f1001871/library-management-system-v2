import time,os
from applications.user_datastore import user_datastore
from flask_restful import Resource
from flask import make_response, jsonify, send_file, request
from flask_security import utils, auth_token_required
from applications.models import *
from applications.cache import cache
from datetime import datetime
from applications import task
from applications.cache import cache


class Login(Resource):
    def post(self):
        recieved_data = request.get_json()

        email = recieved_data.get('email')
        password = recieved_data.get('password')

        if not email or not password:
            return make_response(jsonify({'message':'Email and Password are required'}),400)
        
        user = user_datastore.find_user(email=email)
        if not user:
            return make_response(jsonify({'message':'Invalid Credentials - User doesn\'t exists '}),401)
        
        if not utils.verify_password(password, user.password):
            return make_response(jsonify({'message':'Invalid Credentials - Invalid Password'}),401)
        
        user.last_login_at = user.current_login_at
        db.session.commit()
        user.current_login_at=datetime.now()
        db.session.commit()
        user.login_count+=1
        db.session.commit()

        utils.login_user(user)
        auth_token = user.get_auth_token()

        response = {
            'message':'Login Successful',
            'user':{
                'username':user.username,
                'email':user.email,
                'roles': [role.name for role in user.roles],
                'auth_token':auth_token
            }
        } 
        return make_response(jsonify(response),200) 
    
    @cache.cached(timeout=50)
    def get(self):
        user = USER.query.filter(USER.id != 1).all()
        response = []
        for book in user:
            response.append({
                'user_id':book.id,
                'name':book.username,
                'email':book.email,
                'last_login_at':book.last_login_at,
                'login_count':book.login_count
                })
        return make_response(jsonify(response),200)

class Register(Resource):
    def post(self):
        recieved_data = request.get_json()

        email = recieved_data.get('email')
        password = recieved_data.get('password')
        username = recieved_data.get('username')
        role   = recieved_data.get('role')
        

        if not email or not password or not username:
            return make_response(jsonify({'message':'Email, Username and Password are required'}),400)
        
        user = user_datastore.find_user(email=email)
        if user:
            return make_response(jsonify({'message':'User with provided email id already exists'}),400)
        
        user = user_datastore.find_user(username=username)
        if user:
            return make_response(jsonify({'message':'User with provided username already exists'}),400)
        
        # Input validations at Backend

        if '@' not in email or '.' not in email:
            return make_response(jsonify({'message':'Invalid Email'}),400)
        
        if len(password) < 8:
            return make_response(jsonify({'message':'Password must be atleast 8 characters long'}),400)
        
        if len(username) < 3 or not username.isalnum():
            return make_response(jsonify({'message':'Username must be atleast 3 characters long and alphanumeric characters'}),400)

        if role not in ['user']:
            return make_response(jsonify({'message':'Invalid Role'}),400)
        
        try:
            role = user_datastore.find_role(role)
            user = user_datastore.create_user(email=email, username=username, password=utils.hash_password(password),roles=[role])
            user_datastore.commit()
            # auth_token = user.get_auth_token()

            response = {
                'message':'User Registered Successfully',
                'user':{
                    'username':user.username,
                    'roles': [role.name for role in user.roles],
                }
            }

            data = {
            'username':username,
            'email_address': email}
            
            assigned_task = task.send_welcome_msg.delay(data)

            return make_response(jsonify(response),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),500)
    
    @auth_token_required
    def put(self,email):
        recieved_data = request.get_json()
         
        new_password = recieved_data.get('new_password')
        confirm_password = recieved_data.get('confirm_password')

    
        if  not new_password:
            return make_response(jsonify({'message':'New Password is required'}),400)
         
        if  not confirm_password:
            return make_response(jsonify({'message':'Coform Password is required'}),400)

        if len(new_password) < 8:
            return make_response(jsonify({'message':'Password must be atleast 8 characters long'}),400)
        
        user = user_datastore.find_user(email=email)
        
        if new_password == confirm_password:
            user.password=utils.hash_password(new_password)
            db.session.commit()
            return make_response(jsonify({'message':'Password Changed Successfully'},200))
        else:
            return make_response(jsonify({'message':'Your conform password is not same as new password'},400))



class Logout(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        return make_response(jsonify({'message':'Logout Successful'}),200)

class exportCSV(Resource):
    @auth_token_required
    def get(self,email):
        user = USER.query.filter_by(email=email).first()
        job = task.export_csv.delay(user_id = user.id)
        return make_response(jsonify({'message':'CSV File Created Successfuly Click Download'}),200)

class downloadfile(Resource):
    @auth_token_required
    def get(self,emailid):
        user = USER.query.filter_by(email=emailid).first()
        return send_file(f'report_{user.id}.csv',as_attachment=True, download_name=f'report_{user.id}.csv')