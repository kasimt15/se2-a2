from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request, get_jwt
from functools import wraps
from App.models import User

def login(name, password):
    user = User.query.filter_by(name=name).first()
    if user and user.check_password(password):
        token = create_access_token(identity=user.id, additional_claims={"role": user.role})
        return token
    return None
    
    

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt

def add_auth_context(app):
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            current_user = User.query.get(user_id)
            is_authenticated = True
        except Exception as e:
            print(e)
            is_authenticated = False
            current_user = None
        return dict(is_authenticated=is_authenticated, current_user=current_user)
    
def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') != required_role:
                return jsonify(message="You are not authorized to access this resource"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
