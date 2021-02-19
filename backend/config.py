# importacoes para demais arquivos
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
import os, io
import json
from PIL import Image
import base64
import secrets

app = Flask(__name__) 
CORS(app)
path = os.path.dirname(os.path.abspath(__file__)) 
arquivobd = os.path.join(path, 'evento.db') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+arquivobd 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)