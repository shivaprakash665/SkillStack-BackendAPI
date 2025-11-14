from models.db import db
from datetime import datetime

class Certificate(db.Model):
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    learning_goal_id = db.Column(db.Integer, db.ForeignKey('learning_goals.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)
    file_name = db.Column(db.String(300), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    issuing_authority = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'learning_goal_id': self.learning_goal_id,
            'name': self.name,
            'file_url': self.file_url,
            'file_name': self.file_name,
            'file_type': self.file_type,
            'issue_date': self.issue_date.isoformat(),
            'issuing_authority': self.issuing_authority,
            'created_at': self.created_at.isoformat()
        }