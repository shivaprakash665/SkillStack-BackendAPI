from flask import request, jsonify
from models.certificate import Certificate
from models.learning_goal import LearningGoal
from models import db
from middleware.auth_middleware import token_required
from datetime import datetime
import os
from werkzeug.utils import secure_filename

class CertificateController:
    
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
    UPLOAD_FOLDER = 'uploads/certificates'
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in CertificateController.ALLOWED_EXTENSIONS
    
    @staticmethod
    @token_required
    def upload_certificate(current_user):
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not CertificateController.allowed_file(file.filename):
                return jsonify({'error': 'File type not allowed. Use PDF, JPG, or PNG'}), 400
            
            learning_goal_id = request.form.get('learning_goal_id')
            if not learning_goal_id:
                return jsonify({'error': 'Learning goal ID is required'}), 400
            
            # Verify learning goal belongs to user
            goal = LearningGoal.query.filter_by(id=learning_goal_id, user_id=current_user.id).first()
            if not goal:
                return jsonify({'error': 'Learning goal not found'}), 404
            
            # Create upload directory if not exists
            os.makedirs(CertificateController.UPLOAD_FOLDER, exist_ok=True)
            
            # Save file
            filename = secure_filename(file.filename)
            unique_filename = f"{current_user.id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
            file_path = os.path.join(CertificateController.UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            
            certificate = Certificate(
                user_id=current_user.id,
                learning_goal_id=learning_goal_id,
                name=request.form.get('name', filename),
                file_url=f"/{file_path}",
                file_name=filename,
                file_type=filename.rsplit('.', 1)[1].lower(),
                issue_date=datetime.utcnow(),
                issuing_authority=request.form.get('issuing_authority')
            )
            
            db.session.add(certificate)
            db.session.commit()
            
            return jsonify({
                'message': 'Certificate uploaded successfully',
                'certificate': certificate.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @token_required
    def get_certificates(current_user):
        try:
            certificates = Certificate.query.filter_by(user_id=current_user.id).all()
            return jsonify({
                'certificates': [cert.to_dict() for cert in certificates]
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500