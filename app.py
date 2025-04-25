from flask import Flask
from flask_cors import CORS
from models import db
import os
from controllers.auth_controller import auth_bp
from controllers.expense_controller import expense_bp

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    

    db.init_app(app)
    CORS(app)
    

    app.register_blueprint(auth_bp)
    app.register_blueprint(expense_bp)
    

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
    port = int(os.environ.get('PORT', 5555)) # It will use 5555 as default. You can change it.
    app.run(host='0.0.0.0', port=port, debug=True)