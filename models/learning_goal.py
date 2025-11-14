from models.db import db
from datetime import datetime

class LearningGoal(db.Model):
    __tablename__ = 'learning_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    resource_type = db.Column(db.String(50), nullable=False)
    platform = db.Column(db.String(100))
    link = db.Column(db.String(500))
    start_date = db.Column(db.DateTime, nullable=False)
    expected_end_date = db.Column(db.DateTime)
    actual_end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='not_started')
    difficulty_rating = db.Column(db.String(20))
    total_hours = db.Column(db.Float, default=0)
    certificate_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('Session', backref='learning_goal', lazy=True, cascade='all, delete-orphan')
    study_logs = db.relationship('StudyLog', backref='learning_goal', lazy=True, cascade='all, delete-orphan')
    certificates = db.relationship('Certificate', backref='learning_goal', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'resource_type': self.resource_type,
            'platform': self.platform,
            'link': self.link,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'expected_end_date': self.expected_end_date.isoformat() if self.expected_end_date else None,
            'actual_end_date': self.actual_end_date.isoformat() if self.actual_end_date else None,
            'status': self.status,
            'difficulty_rating': self.difficulty_rating,
            'total_hours': self.total_hours,
            'certificate_url': self.certificate_url,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'progress_percentage': self.calculate_progress(),
            'sessions_count': len(self.sessions),
            'completed_sessions_count': len([s for s in self.sessions if s.status == 'completed'])
        }
    
    def calculate_progress(self):
        if not self.sessions:
            return 0
        completed_sessions = len([s for s in self.sessions if s.status == 'completed'])
        return round((completed_sessions / len(self.sessions)) * 100, 2)