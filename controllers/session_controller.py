from flask import request, jsonify
from models.learning_goal import LearningGoal
from models.session import Session
from models import db
from middleware.auth_middleware import token_required
from datetime import datetime
import os

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
            
            session = Session(
                learning_goal_id=goal_id,
                title=data['title'],
                description=data.get('description'),
                estimated_hours=data.get('estimated_hours', 0),
                order_index=data.get('order_index', 0)
            )
            
            db.session.add(session)
            db.session.commit()
            
            return jsonify({
                'message': 'Session created successfully',
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
                session.status = data['status']
                if data['status'] == 'completed':
                    session.end_date = datetime.utcnow()
                elif data['status'] == 'in_progress':
                    session.start_date = datetime.utcnow()
            
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
    def summarize_notes(current_user, session_id):
        try:
            session = Session.query.join(LearningGoal).filter(
                Session.id == session_id,
                LearningGoal.user_id == current_user.id
            ).first()
            
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            if not session.notes:
                return jsonify({'error': 'No notes to summarize'}), 400
            
            # For now, return mock summary
            mock_summary = f"Summary of notes for '{session.title}': Key points from your learning session."
            session.ai_summary = mock_summary
            db.session.commit()
            
            return jsonify({
                'message': 'Notes summarized successfully',
                'summary': mock_summary
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500