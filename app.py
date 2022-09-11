from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

db = SQLAlchemy(engine_options=dict(executemany_mode="values"))