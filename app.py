from flask import Flask
from flask_cors import CORS
from config import Config
from models.db import db
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)