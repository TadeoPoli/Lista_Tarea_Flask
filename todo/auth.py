import functools
import re

from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

from werkzeug.security import check_password_hash, generate_password_hash

from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

USERNAME_PATTERN = re.compile(r'^[A-Za-z0-9_.-]{3,50}$')
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
DUMMY_PASSWORD_HASH = generate_password_hash('invalid-password-for-timing-check')


def _validate_registration(username, password):
    if not username:
        return 'El nombre de usuario es obligatorio.'
    if not USERNAME_PATTERN.fullmatch(username):
        return (
            'El nombre de usuario debe tener entre 3 y 50 caracteres y solo puede '
            'contener letras, números, puntos, guiones y guiones bajos.'
        )
    if not password:
        return 'La contraseña es obligatoria.'
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        return 'La contraseña debe tener entre 8 y 128 caracteres.'
    return None

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        db, c = get_db()
        error = _validate_registration(username, password)

        c.execute(
            'select id from user where username = %s', (username,)
        )
        if error is None and c.fetchone() is not None:
            error = 'El nombre de usuario ya se encuentra registrado.'

        if error is None:
            c.execute(
                'insert into user (username, password) values (%s, %s)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', username=request.form.get('username', ''))

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        db, c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s', (username,) 
        )
        user = c.fetchone()

        if user is None:
            check_password_hash(DUMMY_PASSWORD_HASH, password)
            error = 'Usuario y/o contraseña invalida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña invalida'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))

        flash(error)

    return render_template('auth/login.html', username=request.form.get('username', ''))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()    
   
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))




        
