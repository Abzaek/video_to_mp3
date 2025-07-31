import jwt, datetime, os
from flask import Flask, request

from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# confiquration
server.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
server.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'auth_user')
server.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'auth_password')
server.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'auth')
server.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))


@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return 'missing credentials', 401

    cur = mysql.connection.cursor()
    res = cur.execute('SELECT email, password FROM users WHERE email = %s', (auth.username,))

    if res > 0:
        user = cur.fetchone()
        if user and user[1] == auth.password and user[0] == auth.username:
            
            return createJWT(auth.username, os.getenv('JWT_SECRET', 'secret'), True), 200
        else:
            return 'invalid credentials', 401
    else:
        return 'user not found', 401
    
@server.route('/validate', methods=['POST'])
def validate():
    encoded_jwt = request.headers.get('Authorization')
    if not encoded_jwt:
        return 'missing token', 401
    try:
        token = encoded_jwt.split(' ')[1]
        decoded = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
    except:
        return 'invalid token', 401
    
    return decoded, 200

def createJWT(username, secret, auths):
    payload = {
        'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
        'iat': datetime.datetime.now(tz=datetime.timezone.utc),
        'username': username,
        'admin': auths
    }
    return jwt.encode(payload, secret, algorithm='HS256')

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)