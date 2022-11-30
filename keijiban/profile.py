from flask import (Blueprint, Markup, flash, g, redirect,
                   render_template, request, url_for)

from html import escape

from keijiban.auth import login_required
from keijiban.db import get_db
from keijiban.markdown import conv_markdown
from keijiban.censor import to_censored

bp = Blueprint('profile', __name__)

@bp.route('/<string:username>')
def profile(username):
  db = get_db()
  print('user', username)
  profile = db.execute(
      'SELECT id, username, nickname, created_at, censor_check, profile_text'
      ' FROM user WHERE username = ?',
      (username,)
    ).fetchone()
  print(profile)
  profile = dict(profile) if profile else None
  print('profile', profile)

  if not profile:
    render_template('profile/userpage.html', userdata=profile, posts=[])

  posts = db.execute(
    'SELECT p.id, body, p.created_at, author_id, username, nickname'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' WHERE u.id = ?'
    ' ORDER BY p.created_at DESC',
    (profile['id'],)
    ).fetchall()
  posts = [dict(p) for p in posts if p]

  if g.user is None or g.user['censor_check']:
    for i in range(len(posts)):
      posts[i]['body'] = conv_markdown(to_censored(posts[i]['body']))
  else:
    for i in range(len(posts)):
      posts[i]['body'] = conv_markdown(posts[i]['body'])

  if profile['profile_text']:
    profile['profile_text'] = conv_markdown(profile['profile_text'])
  print(profile)
  return render_template('profile/userpage.html', userdata=profile, posts=posts)


@bp.route('/<string:username>/update', methods=('GET', 'POST'))
@login_required
def update(username):
  '''
  プロフィール文章、ニックネーム、表示設定の変更
  '''
  db = get_db()
  profile = db.execute(
      'SELECT profile_text, censor_check, nickname FROM user WHERE id = ?', (g.user['id'],)
  ).fetchone()

  if not profile:
    return redirect(url_for('profile.profile', username=username))

  profile = dict(profile)
  profile['profile_text'] = "" if not profile['profile_text'] else profile['profile_text']

  if request.method == 'POST':
    profile['profile_text'] = request.form['profile']
    profile['censor_check'] = True if 'censor_check' in request.form else False
    profile['nickname']     = request.form['nickname']
    error = None

    if error is not None:
      flash(error)
    else:
      db.execute(
          'UPDATE user'
          ' SET (profile_text, censor_check, nickname) = (?, ?, ?)'
          ' WHERE id = ?',
          (escape(profile['profile_text']),
           profile['censor_check'],
           profile['nickname'],
           g.user['id']))
      db.commit()
      return redirect(url_for('profile.profile', username=username))
  return render_template('profile/update.html', profile=profile)
