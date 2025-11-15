from models.db import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    learning_goal_id = db.Column(db.Integer, db.ForeignKey('learning_goals.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed
    estimated_hours = db.Column(db.Float, default=0)
    actual_hours = db.Column(db.Float, default=0)
    order_index = db.Column(db.Integer, default=0)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    ai_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Add time tracking fields
    time_added = db.Column(db.DateTime, default=datetime.utcnow)  # When subtopic was added
    time_started = db.Column(db.DateTime)  # When moved to in_progress
    time_completed = db.Column(db.DateTime)  # When moved to completed
    total_time_spent = db.Column(db.Float, default=0)  # In hours
    
    def to_dict(self):
        return {
            'id': self.id,
            'learning_goal_id': self.learning_goal_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'order_index': self.order_index,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'notes': self.notes,
            'ai_summary': self.ai_summary,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'time_added': self.time_added.isoformat() if self.time_added else None,
            'time_started': self.time_started.isoformat() if self.time_started else None,
            'time_completed': self.time_completed.isoformat() if self.time_completed else None,
            'total_time_spent': self.total_time_spent
        }