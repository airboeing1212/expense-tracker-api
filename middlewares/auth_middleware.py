import jwt
from functools import wraps
from flask import request, jsonify, current_app
from models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'token is mising'}) , 401
        

        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id = data['user_id']).first()
            if not current_user:
                return jsonify({'message' : 'user not found'}), 401
        
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'token expired'}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({'message' : 'invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


        

        

