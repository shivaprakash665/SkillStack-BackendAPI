import jwt
from flask import request, jsonify
from models.user import User
from config import Config

def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode the token
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            current_user = User.query.get(payload['sub'])
            
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
                
            # Pass the current_user to the decorated function
            return f(current_user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
    
    # Preserve the original function name
    decorator.__name__ = f.__name__
    return decorator