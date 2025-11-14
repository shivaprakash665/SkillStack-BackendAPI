import jwt
from flask import request, jsonify
from models import user
from config import Config

def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            current_user = user.query.get(payload['sub'])
            
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
                
            return f(current_user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    
    decorator.__name__ = f.__name__
    return decorator