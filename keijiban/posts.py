from keijiban.censor import to_censored

from flask import ( Blueprint, flash, g, redirect, render_template, request, url_for, Markup )
from werkzeug.exceptions import abort

from html import escape

from keijiban.auth import login_required
from keijiban.db import get_db
from keijiban.markdown import conv_markdown

bp = Blueprint('posts', __name__)

@bp.route('/')
def index():
  db = get_db()
  posts = db.execute(
    'SELECT p.id, body, p.created_at, author_id, username, nickname'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' ORDER BY p.created_at DESC'
  ).fetchall()
  n_posts = [dict(posts[i]) for i in range(len(posts))]
  #print(n_posts)
  if g.user is None or g.user['censor_check'] :
    for i in range(len(n_posts)):
      n_posts[i]['body'] = conv_markdown(to_censored(posts[i]['body']))
  else:
    for i in range(len(n_posts)):
      n_posts[i]['body'] = conv_markdown(posts[i]['body'])

  return render_template('posts/index.html', posts=n_posts)

@bp.route('/', methods=('GET', 'POST'))
@login_required
def create():
  if request.method == 'POST':
    body = request.form['body']
    error = None

    if not body:
      error = '呟きは空にできません。'

    if error is not None:
      flash(error)
    else:
      #print(escape(body))
      db = get_db()
      db.execute(
        'INSERT INTO post (body, author_id)'
        ' VALUES (?, ?)',
        (escape(body), g.user['id'])
      )
      db.commit()
      return redirect(url_for('posts.index'))
  return render_template('posts/index.html')

def get_post(id, check_author=True):
  posts = get_db().execute(
    'SELECT p.id, body, p.created_at, author_id, username, nickname'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' WHERE p.id = ?',
    (id,)
  ).fetchone()

  if posts is None:
    abort(404, f"id {id} の呟きは存在しません。")

  if check_author and posts['author_id'] != g.user['id']:
    abort(403)

  return posts

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
  post = get_post(id)

  if request.method == 'POST':
    body = request.form['body']
    error = None

    if not body:
      error = '呟きは空にできません。'

    if error is not None:
      flash(error)
    else:
      #print(escape(body))
      db = get_db()
      db.execute(
        'UPDATE post SET body = ?'
        ' WHERE id = ?',
        (escape(body), id)
      )
      db.commit()
      return redirect(url_for('posts.index'))
  return render_template('posts/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
  get_post(id)
  db = get_db()
  db.execute('DELETE FROM post WHERE id = ?', (id,))
  db.commit()
  return redirect(url_for('posts.index'))
