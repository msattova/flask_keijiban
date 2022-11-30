import functools

from flask import (
    Blueprint, flash, g,
    redirect, render_template, request,
    session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from keijiban.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
  '''ユーザ登録'''
  if request.method == 'POST':
    print(request.form)
    username = request.form['username']
    nickname = request.form['nickname']
    password = request.form['password']
    censor_check = True if 'censor_check' in request.form else False
    db = get_db()
    error = None

    if not username:
      error = 'ユーザー名は必須です'
    elif not password:
      error = 'パスワードは必須です'
    elif not nickname:
      nickname = username

    if error is None:
      try:
        db.execute(
            "INSERT INTO user (username, nickname, password, censor_check, profile_text)"
            " VALUES (?, ?, ?, ?, NULL)",
            (username, nickname, generate_password_hash(password), censor_check),
        )
        db.commit()
      except db.IntegrityError:
        error = f"ユーザー名： {username} はすでに登録されています。他の名前をお試しください。"
      else:
        return redirect(url_for("auth.login"))
    flash(error)
  return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
  '''ログイン処理'''
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
      error = 'ユーザー名が正しくありません。'
    elif not check_password_hash(user['password'], password):
      error = 'パスワードが正しくありません。'

    if error is None:
      session.clear()
      session['user_id'] = user['id']
      return redirect(url_for('index'))

    flash(error)

  return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')
  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()


@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))


def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))

    return view(**kwargs)
  return wrapped_view
