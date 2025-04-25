from flask import Flask
from flask_cors import CORS
from models import db
import os
from controllers.auth_controller import auth_bp
from controllers.expense_controller import expense_bp

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(expense_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        return {
            'name': 'Expense Tracker API',
            'version': '1.0.0',
            'status': 'running'
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5555))
    app.run(host='0.0.0.0', port=port, debug=True)