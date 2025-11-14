from flask import request, jsonify
from models.learning_goal import LearningGoal
from models.session import Session
from models import db
from middleware.auth_middleware import token_required
from datetime import datetime

class LearningGoalController:
    
    @staticmethod
    @token_required
    def create_learning_goal(current_user):
        try:
            data = request.get_json()
            
            # Validation
            required_fields = ['title', 'resource_type', 'start_date']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Parse dates
            start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
            expected_end_date = None
            if data.get('expected_end_date'):
                expected_end_date = datetime.fromisoformat(data['expected_end_date'].replace('Z', '+00:00'))
            
            learning_goal = LearningGoal(
                user_id=current_user.id,
                title=data['title'],
                description=data.get('description'),
                resource_type=data['resource_type'],
                platform=data.get('platform'),
                link=data.get('link'),
                start_date=start_date,
                expected_end_date=expected_end_date,
                difficulty_rating=data.get('difficulty_rating'),
                total_hours=data.get('total_hours', 0),
                category=data.get('category')
            )
            
            db.session.add(learning_goal)
            db.session.commit()
            
            return jsonify({
                'message': 'Learning goal created successfully',
                'learning_goal': learning_goal.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @token_required
    def get_learning_goals(current_user):
        try:
            goals = LearningGoal.query.filter_by(user_id=current_user.id).all()
            return jsonify({
                'learning_goals': [goal.to_dict() for goal in goals]
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @token_required
    def get_learning_goal(current_user, goal_id):
        try:
            goal = LearningGoal.query.filter_by(id=goal_id, user_id=current_user.id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            return jsonify({
                'learning_goal': goal.to_dict()
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @token_required
    def update_learning_goal(current_user, goal_id):
        try:
            goal = LearningGoal.query.filter_by(id=goal_id, user_id=current_user.id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            data = request.get_json()
            
            # Update fields
            if 'title' in data:
                goal.title = data['title']
            if 'description' in data:
                goal.description = data['description']
            if 'status' in data:
                goal.status = data['status']
                if data['status'] == 'completed':
                    goal.actual_end_date = datetime.utcnow()
            if 'difficulty_rating' in data:
                goal.difficulty_rating = data['difficulty_rating']
            if 'total_hours' in data:
                goal.total_hours = data['total_hours']
            if 'category' in data:
                goal.category = data['category']
            
            goal.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'message': 'Learning goal updated successfully',
                'learning_goal': goal.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @token_required
    def delete_learning_goal(current_user, goal_id):
        try:
            goal = LearningGoal.query.filter_by(id=goal_id, user_id=current_user.id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            db.session.delete(goal)
            db.session.commit()
            
            return jsonify({
                'message': 'Learning goal deleted successfully'
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500