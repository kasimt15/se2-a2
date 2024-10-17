from flask import Blueprint, make_response, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies
from App.controllers.user import get_all_users
from App.controllers.auth import role_required

from App.controllers import login, create_user

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.name}")
    

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['name'], data['password'])
    response = redirect(request.referrer)
    if not token:
        flash('Bad name or password given'), 401
    else:
        flash('Login Successful')
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

'''
API Routes
'''

@auth_views.route('/api/register', methods= ['POST'])
def user_register_api():
    data= request.json
    if not data or 'name' not in data or 'password' not in data or 'role' not in data:
        return jsonify(message="Invalid input"), 400
    try:
        new_user = create_user(data['name'], data['password'], data["email"], data['phone'], data['role'])
    except Exception as e:
        return jsonify(message="An error occurred while creating the user"), 500
    return jsonify({"message": f"id: {new_user.id}, name: {new_user.name} was created"}), 201
    

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    if not data or 'name' not in data or 'password' not in data:
        return jsonify(message="Invalid input"), 400
    
    token = login(data['name'], data['password'])

    if not token:
        return jsonify(message='Invalid name or password'), 401
    return jsonify(access_token=token)

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"name: {current_user.name}, id : {current_user.id}, role: {current_user.role}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response
