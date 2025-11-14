from flask import request, jsonify
from models.study_log import StudyLog
from models.learning_goal import LearningGoal
from models.session import Session
from models import db
from middleware.auth_middleware import token_required
from datetime import datetime, date, timedelta
from sqlalchemy import func

class StudyLogController:
    
    @staticmethod
    @token_required
    def log_study_time(current_user):
        try:
            data = request.get_json()
            
            required_fields = ['learning_goal_id', 'hours_studied', 'date']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Verify learning goal belongs to user
            goal = LearningGoal.query.filter_by(id=data['learning_goal_id'], user_id=current_user.id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            # Verify session belongs to learning goal if provided
            session = None
            if data.get('session_id'):
                session = Session.query.filter_by(id=data['session_id'], learning_goal_id=data['learning_goal_id']).first()
                if not session:
                    return jsonify({'error': 'Session not found for this learning goal'}), 400
            
            study_date = datetime.fromisoformat(data['date'].replace('Z', '+00:00')).date()
            
            study_log = StudyLog(
                user_id=current_user.id,
                learning_goal_id=data['learning_goal_id'],
                session_id=data.get('session_id'),
                date=study_date,
                hours_studied=data['hours_studied'],
                notes=data.get('notes')
            )
            
            db.session.add(study_log)
            db.session.commit()
            
            return jsonify({
                'message': 'Study time logged successfully',
                'study_log': study_log.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @token_required
    def get_study_analytics(current_user):
        try:
            # Daily study time for last 7 days
            end_date = date.today()
            start_date = end_date - timedelta(days=6)
            
            daily_study = db.session.query(
                StudyLog.date,
                func.sum(StudyLog.hours_studied).label('total_hours')
            ).filter(
                StudyLog.user_id == current_user.id,
                StudyLog.date >= start_date,
                StudyLog.date <= end_date
            ).group_by(StudyLog.date).all()
            
            # Weekly average
            weekly_avg = db.session.query(
                func.avg(StudyLog.hours_studied)
            ).filter(
                StudyLog.user_id == current_user.id,
                StudyLog.date >= start_date
            ).scalar() or 0
            
            # Category breakdown
            category_breakdown = db.session.query(
                LearningGoal.category,
                func.sum(StudyLog.hours_studied).label('total_hours')
            ).join(StudyLog, StudyLog.learning_goal_id == LearningGoal.id).filter(
                StudyLog.user_id == current_user.id
            ).group_by(LearningGoal.category).all()
            
            # Goal progress
            goals_progress = LearningGoal.query.filter_by(user_id=current_user.id).all()
            
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