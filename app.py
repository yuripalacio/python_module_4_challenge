from dotenv import load_dotenv

load_dotenv()

import os
from flask import Flask
from src.shared.database import db
from src.shared.login_manager import login_manager
from src.routes.meal import bp as meal_bp
from src.routes.user import bp as user_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

app.register_blueprint(meal_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)
