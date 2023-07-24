#!/usr/bin/env python3

output_dir = 'generated'
output_fn = 'caspal_pyjj_wubi.dict.yaml'

header = '''# author: Caspal

---
name: caspal_pyjj_wubi
version: "2023.07.24"
sort: by_weight
use_preset_vocabulary: false
...

'''

def main():
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



if __name__ == '__main__':
  main()
