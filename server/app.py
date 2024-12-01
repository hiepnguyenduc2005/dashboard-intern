from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_session import Session
import os
from dotenv import load_dotenv
from initial import initial_db, initial_tables
import api
from models import db
from config import ApplicationConfig


bcrypt = Bcrypt()
server_session = Session()

def create_app(config_class=ApplicationConfig):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(config_class)

    # Configure session
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    bcrypt.init_app(app)
    server_session.init_app(app)
    db.init_app(app)

    app.register_blueprint(api.bp)

    return app


if __name__ == '__main__':
    app = create_app()
        # autoload env variables
    load_dotenv()
    PASSWORD = os.getenv('PASSWORD')

    # configure MySQL
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = PASSWORD
    app.config['MYSQL_DB'] = 'dashboard'

    with app.app_context():
        initial_db()
        db.create_all()
        initial_tables(db, bcrypt)
    
    app.run(debug=True, host='0.0.0.0', port=5000)