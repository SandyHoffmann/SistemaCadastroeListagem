# importacoes para demais arquivos, importante!
#aqui se encontra as importações, a aplicação, e o banco de dados!
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
import os, io
import json
from PIL import Image
import base64
import secrets
import math

app = Flask(__name__) 
CORS(app)
path = os.path.dirname(os.path.abspath(__file__)) 
arquivobd = os.path.join(path, 'evento.db') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+arquivobd 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
