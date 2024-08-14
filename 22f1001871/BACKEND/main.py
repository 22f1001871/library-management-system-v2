
from flask import Flask

from applications.user_datastore import user_datastore
from applications.database import db
from applications.config import Config
from flask_restful import Api
from flask_security import Security,hash_password
from applications.auth_api import *
from applications.books_api import *
from applications.search_api import *
from applications.rating_api import *
from applications.statistics import *
from applications.cache import cache
from applications import workers


from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    api = Api(app,prefix='/api/v2')

   

    #Cache App Initialization
    cache.init_app(app)
    

    app.security = Security(app, user_datastore)

    celery = workers.celery
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        broker_connection_retry_on_startup=True,
        timezone='Asia/Kolkata',
        enable_utc=False
    )
    celery.Task = workers.ContextTask
    

    with app.app_context():
        db.create_all()

        admin = app.security.datastore.find_or_create_role(name='admin',description='Administrator')
        user = app.security.datastore.find_or_create_role(name='user',description = 'Customers')
        if not app.security.datastore.find_user(email="admin@gmail.com"):
            app.security.datastore.create_user(email="admin@gmail.com", username='admin', password=hash_password("password"),roles = [admin])
        db.session.commit()
    app.app_context().push()
    return app, api, celery
    


app, api, celery = create_app()


CORS(app)


api.add_resource(Login,'/login')
api.add_resource(Register,'/register','/editProfile/<string:email>')
api.add_resource(Logout,'/logout')

api.add_resource(BookApi,'/section/<int:id>/books')
api.add_resource(Book,'/book','/book/<string:email>','/books/<int:id>')
api.add_resource(Allsections,'/get_all_sections')
api.add_resource(ApproveRequest,'/approve_request/<int:request_id>')
api.add_resource(RejectRequest,'/reject_request/<int:request_id>')
api.add_resource(ViewRequests,'/view_requests')
api.add_resource(ViewRequest,'/view_request/<string:email>','/view_request/<int:id>')
api.add_resource(MyBook,'/mybooks/<string:email>','/return/<int:id>')
api.add_resource(Section,'/section','/section/<int:id>')
api.add_resource(AllBooks,'/get_all_books','/book/<int:id>')
api.add_resource(Viewbooksapproved,'/approvedbooks')
api.add_resource(History,'/history')

api.add_resource(search_section,'/search_section/<string:srch_word>')
api.add_resource(search_book,'/search_book/<string:srch_word>/<int:sid>')

api.add_resource(stat,'/statistics')

api.add_resource(Rating,'/rate')
api.add_resource(exportCSV,'/exportcsv/<string:email>')
api.add_resource(downloadfile,'/get_file/<string:emailid>')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)
