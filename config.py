from flask import Flask
from flask_migrate import Migrate
from resources import create_restful_api
from app import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://yatin:yatin@db:5432/sportsbook"
db.init_app(app)
create_restful_api(app)
migrate = Migrate(app, db)




