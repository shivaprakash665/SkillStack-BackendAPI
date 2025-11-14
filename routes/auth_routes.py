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

@auth_bp.route('/verify', methods=['GET', 'POST'])  # Allow both GET and POST
@token_required
def verify_token(current_user):
    return jsonify({
        'message': 'Token is valid',
        'user': current_user.to_dict()
    }), 200