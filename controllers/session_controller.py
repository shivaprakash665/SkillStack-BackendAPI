from flask import request, jsonify
from models.learning_goal import LearningGoal
from models.session import Session
from models import db
from datetime import datetime

class SessionController:
    
    @staticmethod
    def create_session(user_id, goal_id):
        try:
            goal = LearningGoal.query.filter_by(id=goal_id, user_id=user_id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            data = request.get_json()
            if not data.get('title'):
                return jsonify({'error': 'Title is required'}), 400
            
            max_order = db.session.query(db.func.max(Session.order_index)).filter_by(
                learning_goal_id=goal_id
            ).scalar() or 0
            
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
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_sessions(user_id, goal_id):
        try:
            goal = LearningGoal.query.filter_by(id=goal_id, user_id=user_id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            sessions = Session.query.filter_by(
                learning_goal_id=goal_id
            ).order_by(Session.order_index).all()
            
            return jsonify({
                'sessions': [s.to_dict() for s in sessions]
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update_session_status(user_id, session_id):
        try:
            session = Session.query.join(LearningGoal).filter(
                Session.id == session_id,
                LearningGoal.user_id == user_id
            ).first()
            
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            data = request.get_json()
            old_status = session.status
            
            if "status" in data:
                new_status = data["status"]
                
                if new_status == "in_progress" and old_status != "in_progress":
                    session.time_started = datetime.utcnow()
                
                if new_status == "completed" and old_status != "completed":
                    session.time_completed = datetime.utcnow()
                    if session.time_started:
                        diff = session.time_completed - session.time_started
                        session.total_time_spent = round(diff.total_seconds() / 3600, 2)
                
                session.status = new_status
            
            if "actual_hours" in data:
                session.actual_hours = data["actual_hours"]
            
            if "notes" in data:
                session.notes = data["notes"]

            session.updated_at = datetime.utcnow()
            
            # Update the parent learning goal status
            session.learning_goal.update_status_based_on_sessions()
            
            db.session.commit()

            return jsonify({
                "message": "Session updated successfully",
                "session": session.to_dict()
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update_session_order(user_id, session_id):
        try:
            session = Session.query.join(LearningGoal).filter(
                Session.id == session_id,
                LearningGoal.user_id == user_id
            ).first()
            
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            data = request.get_json()
            if "order_index" in data:
                session.order_index = data["order_index"]
            
            session.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                "message": "Session order updated successfully",
                "session": session.to_dict()
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_session_analytics(user_id, goal_id):
        try:
            goal = LearningGoal.query.filter_by(id=goal_id, user_id=user_id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            sessions = Session.query.filter_by(learning_goal_id=goal_id).all()

            total = len(sessions)
            completed = len([s for s in sessions if s.status == 'completed'])
            in_progress = len([s for s in sessions if s.status == 'in_progress'])
            not_started = len([s for s in sessions if s.status == 'not_started'])
            total_time = sum(s.total_time_spent for s in sessions if s.total_time_spent)

            return jsonify({
                "total_sessions": total,
                "completed_sessions": completed,
                "in_progress_sessions": in_progress,
                "not_started_sessions": not_started,
                "completion_percentage": round((completed / total) * 100, 2) if total > 0 else 0,
                "total_time_spent": round(total_time, 2),
                "average_time_per_session": round(total_time / completed, 2) if completed > 0 else 0
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    @staticmethod
    def delete_session(user_id, session_id):
        try:
            session = Session.query.join(LearningGoal).filter(
                Session.id == session_id,
                LearningGoal.user_id == user_id
            ).first()
            
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            db.session.delete(session)
            db.session.commit()
            
            return jsonify({'message': 'Session deleted successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str("deleted")}), 500

    @staticmethod
    def update_session_notes(user_id, session_id):
        try:
            session = Session.query.join(LearningGoal).filter(
                Session.id == session_id,
                LearningGoal.user_id == user_id
            ).first()
            
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            data = request.get_json()
            
            if "notes" in data:
                session.notes = data["notes"]
            
            if "ai_summary" in data:
                session.ai_summary = data["ai_summary"]
            
            session.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                "message": "Session notes updated successfully",
                "session": session.to_dict()
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500