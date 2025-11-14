from flask import Blueprint
from controllers.learning_goal_controller import LearningGoalController
from controllers.session_controller import SessionController
from controllers.study_log_controller import StudyLogController
from controllers.certificate_controller import CertificateController
from middleware.auth_middleware import token_required

learning_bp = Blueprint('learning', __name__)

# Learning Goals routes
@learning_bp.route('/goals', methods=['POST'])
@token_required
def create_learning_goal(current_user):
    return LearningGoalController.create_learning_goal(current_user)

@learning_bp.route('/goals', methods=['GET'])
@token_required
def get_learning_goals(current_user):
    return LearningGoalController.get_learning_goals(current_user)

@learning_bp.route('/goals/<int:goal_id>', methods=['GET'])
@token_required
def get_learning_goal(current_user, goal_id):
    return LearningGoalController.get_learning_goal(current_user, goal_id)

@learning_bp.route('/goals/<int:goal_id>', methods=['PUT'])
@token_required
def update_learning_goal(current_user, goal_id):
    return LearningGoalController.update_learning_goal(current_user, goal_id)

@learning_bp.route('/goals/<int:goal_id>', methods=['DELETE'])
@token_required
def delete_learning_goal(current_user, goal_id):
    return LearningGoalController.delete_learning_goal(current_user, goal_id)

# Sessions routes
@learning_bp.route('/goals/<int:goal_id>/sessions', methods=['POST'])
@token_required
def create_session(current_user, goal_id):
    return SessionController.create_session(current_user, goal_id)

@learning_bp.route('/goals/<int:goal_id>/sessions', methods=['GET'])
@token_required
def get_sessions(current_user, goal_id):
    return SessionController.get_sessions(current_user, goal_id)

@learning_bp.route('/sessions/<int:session_id>/status', methods=['PUT'])
@token_required
def update_session_status(current_user, session_id):
    return SessionController.update_session_status(current_user, session_id)

@learning_bp.route('/sessions/<int:session_id>/summarize', methods=['POST'])
@token_required
def summarize_notes(current_user, session_id):
    return SessionController.summarize_notes(current_user, session_id)

# Study Logs routes
@learning_bp.route('/study-logs', methods=['POST'])
@token_required
def log_study_time(current_user):
    return StudyLogController.log_study_time(current_user)

@learning_bp.route('/analytics', methods=['GET'])
@token_required
def get_study_analytics(current_user):
    return StudyLogController.get_study_analytics(current_user)

# Certificates routes
@learning_bp.route('/certificates', methods=['POST'])
@token_required
def upload_certificate(current_user):
    return CertificateController.upload_certificate(current_user)

@learning_bp.route('/certificates', methods=['GET'])
@token_required
def get_certificates(current_user):
    return CertificateController.get_certificates(current_user)