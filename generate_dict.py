#!/usr/bin/env python3

from datetime import datetime

from util import read_file

now = datetime.now()
version = now.strftime('%Y.%m.%d')

output_dir = 'generated'
output_fn_format = '{}.dict.yaml'
pinyin_id = 'caspal_pinyin_unicode15'
fuma_id = 'caspal_wubi_fuma'
wubi_id = 'caspal_wubi86'

output_fn_pinyin = output_fn_format.format(pinyin_id)
output_fn_fuma = output_fn_format.format(fuma_id)
output_fn_wubi = output_fn_format.format(wubi_id)

header_template = '''# author: Caspal

---
name: {id}
version: "{v}"
sort: by_weight
use_preset_vocabulary: {p}
...

'''

header_pinyin = header_template.format(id=pinyin_id, v=version, p='true')
header_fuma = header_template.format(id=fuma_id, v=version, p='false')

header_wubi = '''# author: Caspal

---
name: {id}
version: "{v}"
sort: by_weight
columns:
  - text
  - code
  - weight
  - stem
encoder:
  exclude_patterns:
    - '^z.*$'
  rules:
    - length_equal: 2
      formula: "AaAbBaBb"
    - length_equal: 3
      formula: "AaBaCaCb"
    - length_in_range: [4, 10]
      formula: "AaBaCaZa"
...

'''.format(id=wubi_id, v=version)

def wubi():
  wubi86_map = {}
  lines = read_file('{}/{}'.format(output_dir, 'caspal_wubi86.txt'))
  for line in lines:
    ch, wubi = line.split('\t')
    wubi86_map.setdefault(ch, set()).add(wubi)

  keys = sorted(wubi86_map.keys())
  with open('{}/{}'.format(output_dir, output_fn_wubi), 'w') as f:
    f.write(header_wubi)
    for key in keys:
      for wubi in sorted(wubi86_map[key]):
        f.write('{}\t{}\n'.format(key, wubi))
    with open("{}/{}".format(output_dir, 'caspal_phrase_pinyin.txt')) as fph:
      lines = fph.readlines()
    f.write('\n')
    f.write('# 以下为词组\n')
    for line in lines:
      f.write('{}\n'.format(line.split('\t')[0]))

def pinyin():
  pinyin_map = {}

  lines = read_file('{}/{}'.format(output_dir, 'caspal_pinyin.txt'))
  for line in lines:
    ch, pinyin = line.split('\t')
    pinyin_map.setdefault(ch, set()).add(pinyin)

  keys = sorted(pinyin_map.keys())
  with open('{}/{}'.format(output_dir, output_fn_pinyin), 'w') as f:
    f.write(header_pinyin)
    for key in keys:
      for pinyin in sorted(pinyin_map[key]):
        f.write('{}\t{}\n'.format(key, pinyin))
    with open("{}/{}".format(output_dir, 'caspal_phrase_pinyin.txt')) as fph:
      lines = fph.readlines()
    f.write('\n')
    f.write('# 以下为词组\n')
    for line in lines:
      f.write('{}'.format(line))

def fuma():
  fuma_map = {}

  lines = read_file('{}/{}'.format(output_dir, 'caspal_wubi86_fuma.txt'))
  for line in lines:
    ch, fuma = line.split('\t')
    fuma_map.setdefault(ch, set()).add(fuma)

  for ch in fuma_map:
    codes = fuma_map[ch].copy()
    for a in fuma_map[ch]:
      for b in fuma_map[ch]:
        if a != b and b.startswith(a) and a in codes:
          codes.remove(a)
    fuma_map[ch] = codes

  keys = sorted(fuma_map.keys())
  with open('{}/{}'.format(output_dir, output_fn_fuma), 'w') as f:
    f.write(header_fuma)
    for key in keys:
      for fuma in sorted(fuma_map[key]):
        f.write('{}\t{}\n'.format(key, fuma))

def main():
  pinyin()
  fuma()
  wubi()

if __name__ == '__main__':
  main()
