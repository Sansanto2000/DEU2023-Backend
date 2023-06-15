from flask import Blueprint

auth_api = Blueprint('auth', __name__)

@auth_api.route('/login')
def login():
    return 'Página de inicio de sesión'

@auth_api.route('/register')
def register():
    return 'Página de registro'
