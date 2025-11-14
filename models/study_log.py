from .db import db
from datetime import datetime, date

class StudyLog(db.Model):
    __tablename__ = 'study_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    learning_goal_id = db.Column(db.Integer, db.ForeignKey('learning_goals.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    date = db.Column(db.Date, nullable=False, default=date.today)
    hours_studied = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'learning_goal_id': self.learning_goal_id,
            'session_id': self.session_id,
            'date': self.date.isoformat(),
            'hours_studied': self.hours_studied,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }