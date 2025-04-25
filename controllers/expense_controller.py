from flask import Blueprint, request, jsonify
from models import db, Expense, CategoryEnum
from middlewares.auth_middleware import token_required
from datetime import datetime, timedelta
from sqlalchemy import and_

expense_bp = Blueprint('expense', __name__, url_prefix='/api/expenses')

@expense_bp.route('/', methods=['GET'])
@token_required
def get_expenses(current_user):
    filter_type = request.args.get('filter', 'all')
    today = datetime.utcnow()
    
    query = Expense.query.filter_by(user_id=current_user.id)
    
    if filter_type == 'week':
        past_week = today - timedelta(days=7)
        query = query.filter(Expense.date >= past_week)
    elif filter_type == 'month':
        past_month = today - timedelta(days=30)
        query = query.filter(Expense.date >= past_month)
    elif filter_type == 'three_months':
        past_three_months = today - timedelta(days=90)
        query = query.filter(Expense.date >= past_three_months)
    elif filter_type == 'custom':
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date and end_date:
            try:
                start_date = datetime.fromisoformat(start_date)
                end_date = datetime.fromisoformat(end_date)
                query = query.filter(and_(Expense.date >= start_date, Expense.date <= end_date))
            except ValueError:
                return jsonify({'message': 'Invalid date format! Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    expenses = query.order_by(Expense.date.desc()).all()
    
    return jsonify({
        'expenses': [expense.to_dict() for expense in expenses],
        'count': len(expenses)
    }), 200

@expense_bp.route('/<int:expense_id>', methods=['GET'])
@token_required
def get_expense(current_user, expense_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    
    if not expense:
        return jsonify({'message': 'Expense not found!'}), 404
    
    return jsonify(expense.to_dict()), 200

@expense_bp.route('/', methods=['POST'])
@token_required
def create_expense(current_user):
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('title') or not data.get('amount') or not data.get('category'):
        return jsonify({'message': 'Missing required fields!'}), 400
    

    try:
        category = CategoryEnum[data['category'].upper()]
    except KeyError:
        valid_categories = [cat.name for cat in CategoryEnum]
        return jsonify({
            'message': f'Invalid category! Valid categories are: {valid_categories}'
        }), 400
    

    try:
        expense_date = datetime.fromisoformat(data.get('date')) if data.get('date') else datetime.utcnow()
    except ValueError:
        return jsonify({'message': 'Invalid date format! Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    new_expense = Expense(
        title=data['title'],
        amount=float(data['amount']),
        category=category,
        date=expense_date,
        description=data.get('description', ''),
        user_id=current_user.id
    )
    
    db.session.add(new_expense)
    db.session.commit()
    
    return jsonify({
        'message': 'Expense created successfully!',
        'expense': new_expense.to_dict()
    }), 201

@expense_bp.route('/<int:expense_id>', methods=['PUT'])
@token_required
def update_expense(current_user, expense_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    
    if not expense:
        return jsonify({'message': 'Expense not found!'}), 404
    
    data = request.get_json()
    

    if data.get('title'):
        expense.title = data['title']
    
    if data.get('amount'):
        expense.amount = float(data['amount'])
    
    if data.get('category'):
        try:
            expense.category = CategoryEnum[data['category'].upper()]
        except KeyError:
            valid_categories = [cat.name for cat in CategoryEnum]
            return jsonify({
                'message': f'Invalid category! Valid categories are: {valid_categories}'
            }), 400
    
    if data.get('date'):
        try:
            expense.date = datetime.fromisoformat(data['date'])
        except ValueError:
            return jsonify({'message': 'Invalid date format! Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    if 'description' in data:
        expense.description = data['description']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Expense updated successfully!',
        'expense': expense.to_dict()
    }), 200

@expense_bp.route('/<int:expense_id>', methods=['DELETE'])
@token_required
def delete_expense(current_user, expense_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first()
    
    if not expense:
        return jsonify({'message': 'Expense not found!'}), 404
    
    db.session.delete(expense)
    db.session.commit()
    
    return jsonify({'message': 'Expense deleted successfully!'}), 200