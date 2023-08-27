#!/usr/bin/env python3

import re

from util import untone, read_file, get_code_points

output_dir = 'generated'
output_fn = 'caspal_pinyin.txt'

def substitute_specials(pinyin_map):
  replace_map = {}
  lines = read_file('data/overwrite_pinyin.txt')
  for line in lines:
    ch, pinyin = [x.strip() for x in line.split('\t', 1)]
    pinyin = pinyin.split()[0]
    key = 'U+%04X' % ord(ch)
    replace_map.setdefault(key, set()).add(pinyin)
  for key in replace_map:
    pinyin_map[key] = replace_map[key]

def main():
  pinyin_map = {}
  lines = read_file('libs/pinyin-data/pinyin.txt')
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
