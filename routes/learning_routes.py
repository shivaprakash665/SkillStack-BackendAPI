from flask import Blueprint, request, jsonify
from controllers.learning_goal_controller import LearningGoalController

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