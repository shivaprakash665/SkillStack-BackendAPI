import jwt
from flask import request, jsonify
from models.user import User
from config import Config

def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        print(f"🔐 Auth Middleware - Headers: {dict(request.headers)}")  # Debug all headers
        print(f"🔐 Auth Middleware - Auth Header: {auth_header}")  # Debug auth header
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            print(f"🔐 Auth Middleware - Token extracted: {token[:50]}...")  # Debug token (first 50 chars)
        else:
            print("🔐 Auth Middleware - No Bearer token found")
            return jsonify({'error': 'Token is missing'}), 401
        
        if not token:
            print("🔐 Auth Middleware - Token is empty")
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode the token
            print("🔐 Auth Middleware - Attempting to decode token...")
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            print(f"🔐 Auth Middleware - Token payload: {payload}")
            
            user = User.query.get(payload['sub'])
            
            if not user:
                print(f"🔐 Auth Middleware - User not found for ID: {payload['sub']}")
                return jsonify({'error': 'Invalid token'}), 401
            
            print(f"🔐 Auth Middleware - User authenticated: {user.email}")
            # Pass the current_user to the decorated function
            return f(current_user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            print("🔐 Auth Middleware - Token has expired")
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            print(f"🔐 Auth Middleware - Invalid token: {e}")
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            print(f"🔐 Auth Middleware - Token verification failed: {e}")
            return jsonify({'error': 'Token verification failed'}), 401
    
    # Preserve the original function name
    decorator.__name__ = f.__name__
    return decorator