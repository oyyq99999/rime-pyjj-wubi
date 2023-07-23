#!/usr/bin/env python3

import re

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
  for fn in files:
    with open(fn) as f:
      lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [re.sub(r'^\s*#.*|---|\.\.\.|^.*[-:z].*|^\S\S+\t.*', '', l) for l in lines]
    lines = list(filter(lambda x: len(x) > 0, lines))
    for line in lines:
      ch, code = [x.strip() for x in line.split('\t', 1)]
      wubi86_map.setdefault(ch, [])
      code = re.sub(r'\t\d+', '', code)
      codes = code.split('\t')
      for c in codes:
        pass
    print(len(wubi86_map))
    # break

if __name__ == '__main__':
  main()
