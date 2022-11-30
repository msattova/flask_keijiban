import re

'''
対応している記法

* em *
** strong **
` code `

'''

pattern = {
  'em': re.compile(r'\*([^*]+?)\*'),
  'strong': re.compile(r'\*{2}([^*]+?)\*{2}'),
  'code': re.compile(r'`([^`]+?)`'),
  }

def conv_markdown(string):
  '''
  文字列に含まれる対応済みのMarkdownマークアップをHTMLに変換
  string: str -> str
  '''
  ret_str = string
  if pattern['strong'].search(ret_str) is not None:
    ret_str = pattern['strong'].sub(r'<strong>\1</strong>', ret_str)
  if pattern['em'].search(ret_str) is not None:
    ret_str = pattern['em'].sub(r'<em>\1</em>', ret_str)
  if pattern['code'].search(ret_str) is not None:
    ret_str = pattern['code'].sub(r'<code>\1</code>', ret_str)
  return ret_str
