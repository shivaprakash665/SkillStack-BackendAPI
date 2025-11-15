from flask import request, jsonify
from models.learning_goal import LearningGoal
from models.session import Session
from models import db
from middleware.auth_middleware import token_required
from datetime import datetime, timedelta

class SessionController:
    
    @staticmethod
    @token_required
    def create_session(current_user, goal_id):
        try:
            # Verify learning goal belongs to user
            goal = LearningGoal.query.filter_by(id=goal_id, user_id=current_user.id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            data = request.get_json()
            
            if not data.get('title'):
                return jsonify({'error': 'Title is required'}), 400
            
            # Get the highest order index for this goal
            max_order = db.session.query(db.func.max(Session.order_index)).filter_by(learning_goal_id=goal_id).scalar() or 0
            
            session = Session(
                learning_goal_id=goal_id,
                title=data['title'],
                description=data.get('description'),
                estimated_hours=data.get('estimated_hours', 0),
                order_index=max_order + 1,
                time_added=datetime.utcnow()
            )
            
            db.session.add(session)
            db.session.commit()
            
            return jsonify({
                'message': 'Subtopic created successfully',
                'session': session.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @token_required
    def get_sessions(current_user, goal_id):
        try:
            # Verify learning goal belongs to user
            goal = LearningGoal.query.filter_by(id=goal_id, user_id=current_user.id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            sessions = Session.query.filter_by(learning_goal_id=goal_id).order_by(Session.order_index).all()
            return jsonify({
                'sessions': [session.to_dict() for session in sessions]
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @token_required
    def update_session_status(current_user, session_id):
        try:
            session = Session.query.join(LearningGoal).filter(
                Session.id == session_id,
                LearningGoal.user_id == current_user.id
            ).first()
            
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            data = request.get_json()
            
            if 'status' in data:
                new_status = data['status']
                old_status = session.status
                
                # Update timestamps based on status changes
                if new_status == 'in_progress' and old_status != 'in_progress':
                    session.time_started = datetime.utcnow()
                elif new_status == 'completed' and old_status != 'completed':
                    session.time_completed = datetime.utcnow()
                    # Calculate total time spent if started time exists
                    if session.time_started:
                        time_diff = session.time_completed - session.time_started
                        session.total_time_spent = round(time_diff.total_seconds() / 3600, 2)  # Convert to hours
                
                session.status = new_status
            
            if 'actual_hours' in data:
                session.actual_hours = data['actual_hours']
            
            if 'notes' in data:
                session.notes = data['notes']
            
            session.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'message': 'Session updated successfully',
                'session': session.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @token_required
    def update_session_order(current_user, session_id):
        try:
            session = Session.query.join(LearningGoal).filter(
                Session.id == session_id,
                LearningGoal.user_id == current_user.id
            ).first()
            
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            data = request.get_json()
            
            if 'order_index' in data:
                session.order_index = data['order_index']
            
            session.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'message': 'Session order updated successfully',
                'session': session.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @token_required
    def get_session_analytics(current_user, goal_id):
        try:
            # Verify learning goal belongs to user
            goal = LearningGoal.query.filter_by(id=goal_id, user_id=current_user.id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            sessions = Session.query.filter_by(learning_goal_id=goal_id).all()
            
            total_sessions = len(sessions)
            completed_sessions = len([s for s in sessions if s.status == 'completed'])
            in_progress_sessions = len([s for s in sessions if s.status == 'in_progress'])
            not_started_sessions = len([s for s in sessions if s.status == 'not_started'])
            
            # Calculate time statistics
            total_time_spent = sum(s.total_time_spent for s in sessions if s.total_time_spent)
            avg_time_per_session = total_time_spent / completed_sessions if completed_sessions > 0 else 0
            
            return jsonify({
                'total_sessions': total_sessions,
                'completed_sessions': completed_sessions,
                'in_progress_sessions': in_progress_sessions,
                'not_started_sessions': not_started_sessions,
                'completion_percentage': round((completed_sessions / total_sessions) * 100, 2) if total_sessions > 0 else 0,
                'total_time_spent': round(total_time_spent, 2),
                'average_time_per_session': round(avg_time_per_session, 2)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500