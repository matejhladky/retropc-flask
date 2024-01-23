from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from ..models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        # Use only admin
        user = User.query.first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            return 'Invalid password'

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return 'Logged out!'
