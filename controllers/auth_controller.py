
from flask import request, jsonify
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import db
from models.user import User
from config import Config

class AuthController:
    @staticmethod
    def register():
        try:
            data = request.get_json()
            
            # Validation
            required_fields = ['name', 'email', 'password', 'confirmPassword']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            if data.get('password') != data.get('confirmPassword'):
                return jsonify({'error': 'Passwords do not match'}), 400
            
            if len(data['password']) < 6:
                return jsonify({'error': 'Password must be at least 6 characters'}), 400
            
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email already exists'}), 400
            
            # Create user
            hashed_password = generate_password_hash(data['password'])
            user = User(
                name=data['name'],
                email=data['email'],
                password=hashed_password,
                role=data.get('role', 'user')  # Default to 'user'
            )
            
            db.session.add(user)
            db.session.commit()
            
            token = AuthController.generate_token(user.id)
            
            return jsonify({
                'message': 'User created successfully',
                'token': token,
                'user': user.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def login():
        try:
            data = request.get_json()
            
            if not data.get('email') or not data.get('password'):
                return jsonify({'error': 'Email and password are required'}), 400
            
            user = User.query.filter_by(email=data['email']).first()
            
            if not user or not check_password_hash(user.password, data['password']):
                return jsonify({'error': 'Invalid email or password'}), 401
            
            token = AuthController.generate_token(user.id)
            
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': user.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def verify_token():
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': 'Token is missing'}), 401
            
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            user = User.query.get(payload['sub'])
            
            if not user:
                return jsonify({'error': 'Invalid token'}), 401
                
            return jsonify({
                'user': user.to_dict()
            }), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

    @staticmethod
    def generate_token(user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
