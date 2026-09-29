import os

from dotenv import load_dotenv
from flask import Flask, abort, request


def _load_configuration(app):
    """Carga la configuración local sin incluir secretos en el código."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(project_root, '.env'))

    secret_key = os.environ.get('FLASK_SECRET_KEY')
    database_user = os.environ.get('FLASK_DATABASE_USER')
    database_password = os.environ.get('FLASK_DATABASE_PASSWORD')
    database_name = os.environ.get('FLASK_DATABASE')

    missing = [
        name for name, value in {
            'FLASK_SECRET_KEY': secret_key,
            'FLASK_DATABASE_USER': database_user,
            'FLASK_DATABASE_PASSWORD': database_password,
            'FLASK_DATABASE': database_name,
        }.items() if not value
    ]

    if missing:
        raise RuntimeError(
            'Faltan variables de entorno requeridas: ' + ', '.join(missing)
        )

    try:
        database_port = int(os.environ.get('FLASK_DATABASE_PORT', '3306'))
    except ValueError as error:
        raise RuntimeError('FLASK_DATABASE_PORT debe ser un número válido.') from error

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST', '127.0.0.1'),
        DATABASE_PORT=database_port,
        DATABASE_USER=database_user,
        DATABASE_PASSWORD=database_password,
        DATABASE=database_name,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        _load_configuration(app)
    else:
        app.config.from_mapping(test_config)

    from . import db
    from .csrf import csrf_token, validate_csrf_token

    db.init_app(app)

    @app.context_processor
    def inject_csrf_token():
        return {'csrf_token': csrf_token}

    @app.before_request
    def protect_post_requests():
        if request.method == 'POST':
            validate_csrf_token()

    @app.errorhandler(400)
    def bad_request(error):
        return (
            'La solicitud no es válida o su sesión expiró. Volvé a cargar la página e intentá nuevamente.',
            400,
        )

    from . import auth
    from . import todo

    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    return app
        
