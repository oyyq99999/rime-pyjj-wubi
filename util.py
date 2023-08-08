
import re
__all__ = ['read_file', 'untone']

def read_file(fn):
  with open(fn) as f:
    lines = f.readlines()
  lines = [re.sub(r'#.*?(\n|$)', '', line).strip() for line in lines]
  lines = list(filter(lambda x: len(x) > 0, lines))
  return lines

def untone(pinyin):
  mappings = {
    'ā': 'a',
    'á': 'a',
    'ǎ': 'a',
    'à': 'a',
    'ē': 'e',
    'é': 'e',
    'ě': 'e',
    'è': 'e',
    'ī': 'i',
    'í': 'i',
    'ǐ': 'i',
    'ì': 'i',
    'ō': 'o',
    'ó': 'o',
    'ǒ': 'o',
    'ò': 'o',
    'ū': 'u',
    'ú': 'u',
    'ǔ': 'u',
    'ù': 'u',
    'ǖ': 'v',
    'ǘ': 'v',
    'ǚ': 'v',
    'ǜ': 'v',
    'ü': 'v',
    'm̄': 'm',
    'ḿ': 'm',
    'm̀': 'm',
    'ń': 'n',
    'ň': 'n',
    'ǹ': 'n',
    'ê̄': 'ei',
    'ế': 'ei',
    'ê̌': 'ei',
    'ề': 'ei',
  }
  for f, t in mappings.items():
    pinyin = pinyin.replace(f, t)
  return pinyin
