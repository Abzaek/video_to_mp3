import os, gridfs, pika, json, logging
from flask_pymongo import PyMongo
from flask import Flask, request, send_file
from auth import validate
from auth_svc import access
from storage import util 
from bson.objectid import ObjectId

server = Flask(__name__)

mongo_video = PyMongo({
    'app': server,
    'uri': "mongodb://host.minikube.internal:27017/videos"
})

mongo_mp3 = gridfs.GridFS(PyMongo({
    'app': server,
    'uri': "mongodb://host.minikube.internal:27017/mp3s"
}))

fs_video = gridfs.GridFS(mongo_video.db)
fs_mp3 = gridfs.GridFS(mongo_mp3.db)

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
        err = util.upload(f, fs_video, channel, access)

        if err:
            return err
    return "file uploaded successfully", 200
    
@server.route('/download', methods=['GET'])
def download():
    token, err = validate.token(request)

    if err:
        return err
    
    access = json.loads(token)

    if not access['admin']:
        return "not authorized", 403
    
    file_id = request.args.get('id')
    if not file_id:
        return "file id is required", 400
    
    try:        
        file = fs_mp3.get(ObjectId(file_id))
    except Exception as e:
        return "failed to retrieve file", 400


    if not file:
        return "file not found", 404
    
    return send_file(file, as_attachment=True, download_name=f"{file_id}.mp3")

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)