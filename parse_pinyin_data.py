#!/usr/bin/env python3

import re

output_dir = 'generated'
output_fn = 'caspal_pinyin.txt'

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

def process(pinyins):
  result = set()
  for x in pinyins:
    xx = untone(x)
    if re.search(r'^[^aeiouv]+$|[^a-z]', xx):
      print(xx)
    result.add(xx)
  return list(result)

def substitute_specials(pinyin_map):
  pinyin_map['U+3576'] = ['fu'] # 㕶
  pinyin_map['U+5452'] = ['fu', 'wu'] # 呒
  pinyin_map['U+5514'] = ['wu', 'en'] # 唔
  pinyin_map['U+5463'] = ['mou'] # 呣
  pinyin_map['U+54B9'] = ['e', 'an'] # 咹
  pinyin_map['U+54CF'] = ['gen', 'hen'] # 哏
  pinyin_map['U+54FC'] = ['heng'] # 哼
  pinyin_map['U+54FD'] = ['geng', 'ying'] # 哽
  pinyin_map['U+5535'] = ['an'] # 唵
  pinyin_map['U+55EF'] = ['en'] # 嗯
  pinyin_map['U+5638'] = ['fu', 'wu'] # 嘸
  pinyin_map['U+5677'] = ['hen', 'xin'] # 噷
  pinyin_map['U+20BBE'] = ['en'] # 𠮾
  pinyin_map['U+228F5'] = ['chu'] # 𢣵
  pinyin_map['U+2574C'] = ['chu'] # 𥝌

def main():
  pinyin_map = {}
  with open('pinyin-data/pinyin.txt') as f:
    lines = f.readlines()
  lines = [line.strip() for line in lines]
  lines = list(filter(lambda x: len(x) > 0 and x[0] != '#', lines))
  for line in lines:
    code, pinyins = [x.strip() for x in line.split(':', 1)]
    pinyin_map[code] = [x.strip() for x in pinyins[:pinyins.index('#')].strip().split(',')]

  substitute_specials(pinyin_map)

  keys = list(pinyin_map.keys())
  keys = [int(x[2:], 16) for x in keys]
  keys = sorted(keys)
  keys = ['U+%04X' % x for x in keys]

  with open('{}/{}'.format(output_dir, output_fn), 'w') as f:
    for key in keys:
      c = bytes.fromhex(('%8s' % key[2:]).replace(' ', '0')).decode('utf-32be')
      pinyin_list = process(pinyin_map[key])
      for pinyin in pinyin_list:
        f.write('{}\t{}\n'.format(c, pinyin))

if __name__ == '__main__':
  main()
