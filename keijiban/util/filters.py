
from flask import (
    Blueprint, Markup
)

bp = Blueprint('filter', __name__)

@bp.app_template_filter('to_br')
def to_br(string):
  '''
  改行を<br>タグに変換し、文字列中のHTMLタグをJinjaテンプレートでHTMLタグとして解釈するようにする
  string: str -> Markup
  '''
  return Markup(string.replace('\r', '<br>'))
