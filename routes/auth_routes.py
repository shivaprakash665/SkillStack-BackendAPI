from flask import Blueprint
from controllers.auth_controller import AuthController
from middleware.auth_middleware import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    return AuthController.register()

@auth_bp.route('/login', methods=['POST'])
def login():
    return AuthController.login()

@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    return AuthController.verify_token()

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return {
        'message': f'Hello {current_user.name}! This is a protected route.',
        'user': current_user.to_dict()
    }