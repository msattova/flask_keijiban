from keijiban.static.censor_words import CENSOR_WORDS
from janome.tokenizer import Tokenizer
from typing import NamedTuple

t = Tokenizer(wakati=True)

CENSORS = tuple(d['censor'] for d in CENSOR_WORDS)
REPS = tuple(d['rep'] for d in CENSOR_WORDS)

class CensorWord(NamedTuple):
  word:  str
  index: int

def has_censor_words(string):
  '''
  不適切な単語があるかどうかを形態素解析による分かち書きの後に判断。
  複数語からなる不適切な単語は認識できない可能性が高い。
  string: str -> tuple[tuple[CensorWord, list[str]]] | None
  '''
  tokens = list(t.tokenize(string))
  ret = tuple([ CensorWord(word, i) for i, word in enumerate(tokens) if word in CENSORS])
  if not ret:
    return None
  return (ret, tokens)


def to_censored(string):
  '''
  不適切な単語があるか調べ、なければそのまま返す。
  あれば、分かち書きした文章の当該箇所を言い換え語に置き換えた文章を生成して返す。
  string: str -> str
  '''
  result = has_censor_words(string)
  if not result:
    return string
  cwords, ret = result
  for c in cwords:
    ret[c.index] = REPS[CENSORS.index(c.word)]
  return ''.join(ret)
