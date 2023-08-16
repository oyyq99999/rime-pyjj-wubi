#!/usr/bin/env python3

import re

from util import untone, read_file, get_code_points

output_dir = 'generated'
output_fn = 'caspal_pinyin.txt'

def substitute_specials(pinyin_map):
  pinyin_map['U+3576'] ={'fu'} # 㕶
  pinyin_map['U+5452'] ={'fu', 'wu'} # 呒
  pinyin_map['U+5514'] ={'wu', 'en'} # 唔
  pinyin_map['U+5463'] ={'mou'} # 呣
  pinyin_map['U+54B9'] ={'e', 'an'} # 咹
  pinyin_map['U+54CF'] ={'gen', 'hen'} # 哏
  pinyin_map['U+54FC'] ={'heng'} # 哼
  pinyin_map['U+54FD'] ={'geng', 'ying'} # 哽
  pinyin_map['U+5535'] ={'an'} # 唵
  pinyin_map['U+55EF'] ={'en'} # 嗯
  pinyin_map['U+5638'] ={'fu', 'wu'} # 嘸
  pinyin_map['U+5677'] ={'hen', 'xin'} # 噷
  pinyin_map['U+20BBE'] ={'en'} # 𠮾
  pinyin_map['U+228F5'] ={'chu'} # 𢣵
  pinyin_map['U+2574C'] ={'chu'} # 𥝌
  pinyin_map['U+2E9F5'] ={'wei'} # 𮧵

def main():
  pinyin_map = {}
  lines = read_file('pinyin-data/pinyin.txt')
  code_points = get_code_points()
  for line in lines:
    code, pinyins = [x.strip() for x in line.split(':', 1)]
    cp = int(code[2:], 16)
    if cp not in code_points['all'] and cp not in code_points['pua']:
      print('Non-CJK Ideograph {}({}) found'.format(chr(cp), code))
    pinyin_map.setdefault(code, set())
    for pinyin in pinyins.split(','):
      pinyin_map[code].add(untone(pinyin.strip()))

  substitute_specials(pinyin_map)
  for x in pinyin_map:
    for xx in pinyin_map[x]:
      if re.search(r'^[^aeiouv]+$|[^a-z]', xx):
        print(xx)

  keys = list(pinyin_map.keys())
  keys = [int(x[2:], 16) for x in keys]
  keys = sorted(keys)
  keys = ['U+%04X' % x for x in keys]

  with open('{}/{}'.format(output_dir, output_fn), 'w') as f:
    for key in keys:
      c = chr(int(key[2:], 16))
      for pinyin in sorted(pinyin_map[key]):
        f.write('{}\t{}\n'.format(c, pinyin))

if __name__ == '__main__':
  main()
