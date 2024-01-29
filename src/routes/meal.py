from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from marshmallow import Schema, fields, ValidationError
from src.models.meal import db, Meal

bp = Blueprint('meals', __name__)

class CreateMealSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    date = fields.DateTime(required=True)
    diet = fields.Bool(load_default=False)

class UpdateMealSchema(Schema):
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    date = fields.DateTime(required=False)
    diet = fields.Bool(required=False)

@bp.route('/meals', methods=['POST'])
@login_required
def create_meal():
    data = request.json

    try:
        data = CreateMealSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    name = data["name"]
    description = data["description"]
    date = data["date"]
    diet = data["diet"]

    meal = Meal(name=name, description=description, date=date, diet=diet, user_id=current_user.id)

    db.session.add(meal)
    db.session.commit()

    return jsonify(meal.to_dict())

@bp.route('/meals', methods=['GET'])
@login_required
def get_meals():
    meals = Meal.query.filter_by(user_id=current_user.id).all()

    dict_meals = []
    dict_meals = [meal.to_dict() for meal in meals]

    return jsonify(dict_meals)

@bp.route('/meals/<int:meal_id>', methods=['GET'])
@login_required
def get_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id).to_dict()

    if current_user.role != 'admin' and meal['user_id'] != current_user.id:
        return jsonify({"message": "Unauthorized user"}), 403

    return jsonify(meal)

@bp.route('/meals/<int:meal_id>', methods=['PUT'])
@login_required
def update_meal(meal_id):
    data = request.json
    
    try:
        data = UpdateMealSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    meal = Meal.query.get_or_404(meal_id)

    meal_dict = meal.to_dict()
    if meal_dict['user_id'] != current_user.id:
        return jsonify({"message": "Unauthorized user"}), 403

    changes_made = False
    for field, value in data.items():
        if hasattr(meal, field) and getattr(meal, field) != value:
            setattr(meal, field, value)
            changes_made = True

    if changes_made:
        db.session.add(meal)
        db.session.commit()

    return jsonify(meal.to_dict())

@bp.route('/meals/<int:meal_id>', methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)

    meal_dict = meal.to_dict()
    if meal_dict['user_id'] != current_user.id:
        return jsonify({"message": "Unauthorized user"}), 403

    db.session.delete(meal)
    db.session.commit()

    return '', 204

@bp.route('/meals/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_meals(user_id):
    if current_user.role != 'admin':
        return jsonify({"message": "Unauthorized user"}), 403

    meals = Meal.query.filter_by(user_id=user_id).all()
    dict_meals = []

    dict_meals = [meal.to_dict() for meal in meals]

    return jsonify(dict_meals)
