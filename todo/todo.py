from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__)
MAX_DESCRIPTION_LENGTH = 500


def _validate_description(description):
    if not description:
        return 'La descripción es obligatoria.'
    if len(description) > MAX_DESCRIPTION_LENGTH:
        return f'La descripción no puede superar los {MAX_DESCRIPTION_LENGTH} caracteres.'
    return None

@bp.route('/')
@login_required
def index():
    db, c = get_db()
    c.execute(
        'select t.id, t.description, u.username, t.completed, t.created_at from todo t JOIN user u on t.created_by = u.id where t.created_by = %s order by created_at desc',
        (g.user['id'],)
    )
    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)

    
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        error = _validate_description(description)

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'insert into todo (description, completed, created_by) values (%s, %s, %s)',
                (description, False, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))
    return render_template('todo/create.html', description=request.form.get('description', ''))

def get_todo(id):
    if id < 1:
        abort(404)

    db, c = get_db()
    c.execute(
        'select t.id, t.description, t.completed, t.created_by, t.created_at, u.username from todo t join user u on t.created_by = u.id where t.id = %s and t.created_by = %s',
        (id, g.user['id'])
    )

    todo = c.fetchone()

    if todo is None:
        abort(404)

    return todo

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        completed = True if request.form.get('completed') == 'on' else False
        error = _validate_description(description)

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'update todo set description = %s, completed = %s where id = %s and created_by = %s',
                (description, completed, id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))
    return render_template('todo/update.html', todo=todo)
        
    


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    get_todo(id)
    db, c = get_db()
    c.execute('delete from todo where id = %s and created_by = %s', (id, g.user['id']))
    db.commit()
    flash('Tarea eliminada correctamente.')
    return redirect(url_for('todo.index'))
