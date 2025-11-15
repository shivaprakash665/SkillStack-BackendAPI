from flask import Blueprint, request, jsonify
from controllers.learning_goal_controller import LearningGoalController
from controllers.session_controller import SessionController

learning_bp = Blueprint('learning', __name__)

# Learning Goals routes
@learning_bp.route('/goals', methods=['POST'])
def create_learning_goal():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    return LearningGoalController.create_learning_goal(user_id)

@learning_bp.route('/goals', methods=['GET'])
def get_learning_goals():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    return LearningGoalController.get_learning_goals(int(user_id))

@learning_bp.route('/goals/<int:goal_id>', methods=['GET'])
def get_learning_goal(goal_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    return LearningGoalController.get_learning_goal(int(user_id), goal_id)

@learning_bp.route('/analytics', methods=['GET'])
def get_study_analytics():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    return LearningGoalController.get_study_analytics(int(user_id))

# Session/Subtopic routes
@learning_bp.route('/goals/<int:goal_id>/sessions', methods=['POST'])
def create_session(goal_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    return SessionController.create_session(user_id, goal_id)

@learning_bp.route('/goals/<int:goal_id>/sessions', methods=['GET'])
def get_sessions(goal_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    return SessionController.get_sessions(int(user_id), goal_id)

@learning_bp.route('/sessions/<int:session_id>/status', methods=['PUT'])
def update_session_status(session_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    return SessionController.update_session_status(int(user_id), session_id)

@learning_bp.route('/sessions/<int:session_id>/order', methods=['PUT'])
def update_session_order(session_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    return SessionController.update_session_order(int(user_id), session_id)

@learning_bp.route('/goals/<int:goal_id>/analytics', methods=['GET'])
def get_session_analytics(goal_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    return SessionController.get_session_analytics(int(user_id), goal_id)