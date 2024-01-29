import bcrypt
from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from flask_login import login_user, current_user, logout_user, login_required
from src.shared.login_manager import login_manager
from src.models.user import db, User

bp = Blueprint('users', __name__)

class LoginUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class CreateUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Str(default='user')

class UpdateUserSchema(Schema):
    password = fields.Str(required=False)
    role = fields.Str(required=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@bp.route('/login', methods=['POST'])
def login():
    data = request.json

    try:
        data = LoginUserSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    username = data["username"]
    password = data["password"]
    
    user_exists = User.query.filter_by(username=username).first()

    if not user_exists or not bcrypt.checkpw(str.encode(password), user_exists.password):
        return jsonify({"message": "Invalid credentials"}), 400

    login_user(user_exists)

    return jsonify(user_exists.to_dict())

@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return '', 204

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    
    try:
        data = CreateUserSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    username = data["username"]
    
    user_exists = User.query.filter_by(username=username).first()
    
    if user_exists:
        return jsonify({"message": "Invalid data"}), 400
    
    password = data["password"]
    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

    user = User(username=username, password=hashed_password, role='user')
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict())

@bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    
    return jsonify(user.to_dict())

@bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    data = request.json

    if current_user.role != 'admin' and current_user.id != user_id:
        return jsonify({"message": "Unauthorized user"}), 403

    try:
        data = UpdateUserSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    if current_user.role != 'admin' and data.get('role'):
        return jsonify({"message": "Unauthorized user"}), 400

    user = User.query.get_or_404(user_id)
    
    changes_made = False
    for field, value in data.items():
        if hasattr(user, field) and getattr(user, field) != value:
            setattr(user, field, value if field != 'password' else bcrypt.hashpw(str.encode(value), bcrypt.gensalt()))
            changes_made = True

    if changes_made:
        db.session.add(user)
        db.session.commit()

    return jsonify(user.to_dict())

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"message": f"User [{user_id}] not fount"}), 404
    
    if user.username == 'admin':
        return jsonify({"message": "Invalid data"}), 400

    if current_user.role != 'admin' or current_user.username != user.username:
        return jsonify({"message": "Unauthorized user"}), 403

    db.session.delete(user)
    db.session.commit()

    if user_id == current_user.id:
        logout_user()
    
    return '', 204