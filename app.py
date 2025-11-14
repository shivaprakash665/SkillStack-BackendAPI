from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.learning_routes import learning_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app)

# Create upload directory
os.makedirs('uploads/certificates', exist_ok=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(learning_bp, url_prefix='/api/learning')

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)