from flask import Blueprint, request
from controllers.learning_goal_controller import LearningGoalController
from controllers.session_controller import SessionController

learning_bp = Blueprint('learning', __name__)

# ---------------- Learning Goals ---------------- #

@learning_bp.route('/goals', methods=['POST'])
def create_learning_goal():
    user_id = request.json.get('user_id')
    return LearningGoalController.create_learning_goal(user_id)

@learning_bp.route('/goals', methods=['GET'])
def get_learning_goals():
    user_id = request.args.get('user_id')
    return LearningGoalController.get_learning_goals(user_id)

@learning_bp.route('/goals/<int:goal_id>', methods=['GET'])
def get_learning_goal(goal_id):
    user_id = request.args.get('user_id')
    return LearningGoalController.get_learning_goal(user_id, goal_id)

@learning_bp.route('/analytics', methods=['GET'])
def get_study_analytics():
    user_id = request.args.get('user_id')
    return LearningGoalController.get_study_analytics(user_id)


# ---------------- Sessions / Subtopics ---------------- #

@learning_bp.route('/goals/<int:goal_id>/sessions', methods=['POST'])
def create_session(goal_id):
    user_id = request.json.get('user_id')
    return SessionController.create_session(user_id, goal_id)

@learning_bp.route('/goals/<int:goal_id>/sessions', methods=['GET'])
def get_sessions(goal_id):
    user_id = request.args.get('user_id')
    return SessionController.get_sessions(user_id, goal_id)

@learning_bp.route('/sessions/<int:session_id>/status', methods=['PUT'])
def update_session_status(session_id):
    user_id = request.json.get('user_id')
    return SessionController.update_session_status(user_id, session_id)

@learning_bp.route('/sessions/<int:session_id>/order', methods=['PUT'])
def update_session_order(session_id):
    user_id = request.json.get('user_id')
    return SessionController.update_session_order(user_id, session_id)

@learning_bp.route('/goals/<int:goal_id>/analytics', methods=['GET'])
def get_session_analytics(goal_id):
    user_id = request.args.get('user_id')
    return SessionController.get_session_analytics(user_id, goal_id)
