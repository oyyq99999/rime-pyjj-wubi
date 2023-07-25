#!/usr/bin/env python3

output_dir = 'generated'
output_fn = 'caspal_pyjj_wubi.dict.yaml'
output_fn_wubi = 'caspal_wubi86.dict.yaml'

header = '''# author: Caspal

---
name: caspal_pyjj_wubi
version: "2023.07.24"
sort: by_weight
use_preset_vocabulary: true
...

'''

wubi_header = '''# author: Caspal

---
name: caspal_wubi86
version: "23.07.25"
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

'''

def wubi():
  wubi86_map = {}
  with open ('{}/{}'.format(output_dir, 'caspal_wubi86.txt')) as f:
    lines = f.readlines()
  lines = [line.strip() for line in lines]
  lines = list(filter(lambda x: len(x) > 0 and x[0] != '#', lines))
  for line in lines:
    ch, wubi = line.split('\t')
    wubi86_map.setdefault(ch, set()).add(wubi)

  keys = sorted(wubi86_map.keys())
  with open('{}/{}'.format(output_dir, output_fn_wubi), 'w') as f:
    f.write(wubi_header)
    for key in keys:
      for wubi in wubi86_map[key]:
        f.write('{}\t{}\n'.format(key, wubi))
    with open("{}/{}".format(output_dir, 'caspal_phrase_pinyin.txt')) as fph:
      lines = fph.readlines()
    f.write('\n')
    f.write('# 以下为词组\n')
    for line in lines:
      f.write('{}\n'.format(line.split('\t')[0]))

def pinyin_wubi():
  pinyin_map = {}
  fuma_map = {}
  with open('{}/{}'.format(output_dir, 'caspal_pinyin.txt')) as f:
    lines = f.readlines()
  lines = [line.strip() for line in lines]
  lines = list(filter(lambda x: len(x) > 0 and x[0] != '#', lines))
  for line in lines:
    ch, pinyin = line.split('\t')
    pinyin_map.setdefault(ch, set()).add(pinyin)

  with open('{}/{}'.format(output_dir, 'caspal_wubi86_fuma.txt')) as f:
    lines = f.readlines()
  lines = [line.strip() for line in lines]
  lines = list(filter(lambda x: len(x) > 0 and x[0] != '#', lines))
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

  keys = sorted(pinyin_map.keys())
  with open('{}/{}'.format(output_dir, output_fn), 'w') as f:
    f.write(header)
    for key in keys:
      for pinyin in pinyin_map[key]:
        if key in fuma_map:
          for fuma in fuma_map[key]:
            # print(key, pinyin, fuma)
            f.write('{}\t{};{}\n'.format(key, pinyin, fuma))
        else:
          f.write('{}\t{}\n'.format(key, pinyin))
    with open("{}/{}".format(output_dir, 'caspal_phrase_pinyin.txt')) as fph:
      lines = fph.readlines()
    f.write('\n')
    f.write('# 以下为词组\n')
    for line in lines:
      f.write('{}'.format(line))

def main():
  pinyin_wubi()
  wubi()

if __name__ == '__main__':
  main()
