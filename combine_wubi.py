#!/usr/bin/env python3

import re
from string import ascii_lowercase as alc

from util import read_file, get_code_points

output_dir = 'generated'
output_wubi_fn = 'caspal_wubi86.txt'
output_fuma_fn = 'caspal_wubi86_fuma.txt'

fuma = {}
for x in alc[:-1]:
  fuma[x] = set()
for x in alc[:-1]:
  for y in alc[:-1]:
    fuma[x + y] = set()

def substitute_specials(wubi86_map):
  wubi86_map['U+200CD'] = {'nnll'} # missing character '𠃍'

def main():
  wubi86_map = {}
  files = [
    'rime-wubi/wubi86.dict.yaml',
    'rime-wubi86-ext/wubi86.basiccmpl.dict.yaml',
    'rime-wubi86-ext/wubi86.extacmpl.dict.yaml',
    'rime-wubi86-ext/wubi86.extbcmpl.dict.yaml',
    'rime-wubi86-ext/wubi86.extc.dict.yaml',
    'rime-wubi86-ext/wubi86.extccmpl.dict.yaml',
    'rime-wubi86-ext/wubi86.extd.dict.yaml',
    'rime-wubi86-ext/wubi86.exte.dict.yaml',
    'rime-wubi86-ext/wubi86.extf.dict.yaml',
    'rime-wubi86-ext/wubi86.extg.dict.yaml',
    'rime-wubi86-ext/wubi86.exth.dict.yaml',
  ]
  code_points = get_code_points()
  for fn in files:
    lines = read_file(fn)
    lines = [re.sub(r'^\s*#.*|---|\.\.\.|^.*[-:z].*|^\S\S+\t.*', '', l) for l in lines]
    lines = list(filter(lambda x: len(x) > 0, lines))

    for line in lines:
      ch, code = [x.strip() for x in line.split('\t', 1)]
      uni = 'U+%04X' % ord(ch)
      if ord(ch) not in code_points['all']:
        print('Non-CJK character {}({}) found in {}'.format(ch, uni, fn))
      wubi86_map.setdefault(uni, set())
      code = re.sub(r'\t\d+', '', code)
      codes = code.split('\t')
      for c in codes:
        wubi86_map[uni].add(c)

  substitute_specials(wubi86_map)

  for c in sorted(code_points['uni']):
    k = 'U+%04X' % c
    if k not in wubi86_map:
      print('{} missing'.format(k))

  for uni in wubi86_map:
    if len(wubi86_map[uni]) < 1:
      continue
    for code in wubi86_map[uni]:
      char = chr(int(uni[2:], 16))
      code1 = code[0]
      code2 = code[:2] if len(code) > 1 else None
      fuma[code1].add(char)
      if code2:
        fuma[code2].add(char)

  keys = list(wubi86_map.keys())
  keys = [int(x[2:], 16) for x in keys]
  keys = sorted(keys)
  keys = ['U+%04X' % x for x in keys]

  with open('{}/{}'.format(output_dir, output_wubi_fn), 'w') as f:
    for key in keys:
      c = chr(int(key[2:], 16))
      for wubi in sorted(wubi86_map[key]):
        f.write('{}\t{}\n'.format(c, wubi))

  with open('{}/{}'.format(output_dir, output_fuma_fn), 'w') as f:
    for code in fuma:
      for char in sorted(fuma[code]):
        f.write('{}\t{}\n'.format(char, code))

if __name__ == '__main__':
  main()
