import os, gridfs, pika, json, logging
from flask_pymongo import PyMongo
from flask import Flask, request
from auth import validate
from auth_svs import access
from storage import util 

server = Flask(__name__)
server.config['MONGO_URI'] = "mongodb://host.minikube.internal:27017/videos"
mongo = PyMongo(server)
