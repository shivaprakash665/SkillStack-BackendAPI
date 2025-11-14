from flask import request, jsonify
from models.learning_goal import LearningGoal
from models.session import Session
from models.study_log import StudyLog
from models import db
from datetime import datetime, date, timedelta
from sqlalchemy import func

class LearningGoalController:
    
    @staticmethod
    def create_learning_goal(user_id):
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
                user_id=user_id,
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
    def get_learning_goals(user_id):
        try:
            goals = LearningGoal.query.filter_by(user_id=user_id).all()
            return jsonify({
                'learning_goals': [goal.to_dict() for goal in goals]
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def get_learning_goal(user_id, goal_id):
        try:
            goal = LearningGoal.query.filter_by(id=goal_id, user_id=user_id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            return jsonify({
                'learning_goal': goal.to_dict()
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def get_study_analytics(user_id):
        try:
            # Daily study time for last 7 days
            end_date = date.today()
            start_date = end_date - timedelta(days=6)
            
            daily_study = db.session.query(
                StudyLog.date,
                func.sum(StudyLog.hours_studied).label('total_hours')
            ).filter(
                StudyLog.user_id == user_id,
                StudyLog.date >= start_date,
                StudyLog.date <= end_date
            ).group_by(StudyLog.date).all()
            
            # Weekly average
            weekly_avg = db.session.query(
                func.avg(StudyLog.hours_studied)
            ).filter(
                StudyLog.user_id == user_id,
                StudyLog.date >= start_date
            ).scalar() or 0
            
            # Category breakdown
            category_breakdown = db.session.query(
                LearningGoal.category,
                func.sum(StudyLog.hours_studied).label('total_hours')
            ).join(StudyLog, StudyLog.learning_goal_id == LearningGoal.id).filter(
                StudyLog.user_id == user_id
            ).group_by(LearningGoal.category).all()
            
            # Goal progress
            goals_progress = LearningGoal.query.filter_by(user_id=user_id).all()
            
            return jsonify({
                'daily_study': [
                    {'date': log.date.isoformat(), 'hours': float(log.total_hours or 0)}
                    for log in daily_study
                ],
                'weekly_average': round(float(weekly_avg), 2),
                'category_breakdown': [
                    {'category': cat.category or 'Uncategorized', 'hours': float(cat.total_hours or 0)}
                    for cat in category_breakdown
                ],
                'goals_progress': [
                    {
                        'title': goal.title,
                        'progress': goal.calculate_progress(),
                        'status': goal.status
                    }
                    for goal in goals_progress
                ]
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500