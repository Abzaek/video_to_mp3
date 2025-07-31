import os, gridfs, pika, json, logging
from flask_pymongo import PyMongo
from flask import Flask, request
from auth import validate
from auth_svc import access
from storage import util 

server = Flask(__name__)
server.config['MONGO_URI'] = "mongodb://host.minikube.internal:27017/videos"
mongo = PyMongo(server)
grid_fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
channel = connection.channel()
@server.route('/login', methods=['POST'])
def login():
    token, err = access.login(request)

    if err:
        return err
    
    return token

@server.route('/upload', methods=['POST'])
def upload():
    token, err = validate.token(request)

    if err:
        return err
    
    access = json.loads(token)

    if not access['admin']:
        return "not authorized", 403
    
    if len(request.files) != 1:
        return "exactly 1 file required", 400
    
    for _, f in request.files.items():
        err = util.upload(f, grid_fs, channel, access)

        if err:
            return err
    
@server.route('/download', methods=['GET'])
def download():
    pass

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)