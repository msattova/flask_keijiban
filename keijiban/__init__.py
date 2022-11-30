from dotenv import load_dotenv
from flask import Flask, send_from_directory
from pathlib import Path
import os
from waitress import serve

load_dotenv(override=True)

def create_app(test_config=None):
  '''ここからプログラムが始まる'''
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
      SECRET_KEY=('dev' if 'FLASK_SECRET_KEY' not in os.environ
                  else os.environ['FLASK_SECRET_KEY']),
      DATABASE=Path(app.instance_path)/'flask.sqlite',
  )
  if test_config is None:
    app.config.from_pyfile('config.py', silent=True)
  else:
    app.config.from_mapping(test_config)
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  @app.route('/favicon.ico')
  def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico',)

  from . import db
  db.init_app(app)

  from . import auth
  app.register_blueprint(auth.bp)

  from . import posts
  app.register_blueprint(posts.bp)
  app.add_url_rule('/', endpoint='index')

  from . import profile
  app.register_blueprint(profile.bp)

  from .util import filters
  app.register_blueprint(filters.bp)

  return app
