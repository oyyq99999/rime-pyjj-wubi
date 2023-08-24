#!/usr/bin/env python3

import os, re
import opencc
from string import ascii_lowercase as alc
from icu import Locale

from util import read_file

input_dir = 'libs/rime-emoji/opencc'
output_dir = 'opencc'

converter = opencc.OpenCC('tw2sp')

def has_flag(translations):
  for translation in translations:
    is_flag = True
    for ch in translation:
      if ord(ch) < 0x1f1e6 or ord(ch) > 0x1f1ff:
        is_flag = False
        break
    if is_flag:
      return True
  return False

def add_flags(mappings):
  # according to https://github.com/unicode-org/cldr/blob/release-43-1/common/validity/region.xml
  # may be updated to later releases
  # reference: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
  exceptions = [
    'AN', 'BU', 'CS', 'DD', 'FX', 'SU', 'TP', 'YD', 'YU', 'ZR', # deprecated
    'DY', 'RH', # indeterminately reserved
    'HV', 'NH', 'VD', # deleted
    'EZ', 'QO', # macroregion, no flags found
    'EZ', 'UK', # exceptionally reserved
    'ZZ' # unknown
  ]
  lang = Locale('zh-Hans')
  letter_a = ord('a')
  flag_a = '\U0001f1e6'
  for x in alc:
    for y in alc:
      if x == 'x' and y != 'k':
        continue
      iso2 = (x + y).upper()
      if iso2 in exceptions:
        continue
      translated = Locale(f'-{iso2}').getDisplayCountry(lang)
      if translated != iso2:
        flag = chr(ord(flag_a) + ord(x) - letter_a) + chr(ord(flag_a) + ord(y) - letter_a)
        mappings.setdefault(translated, [])
        if flag not in mappings[translated]:
          mappings[translated].append(flag)
  return mappings

def simplify(fn):
  results = {}
  lines = read_file(f'{input_dir}/{fn}')
  need_to_add_flags = False
  for line in lines:
    text, emojis = [x.strip() for x in line.split('\t', 1)]
    emojis = [x.strip() for x in re.split(r'\s+', emojis)]
    emojis = list(filter(lambda x: len(x) > 0 and x != text, emojis))
    filtered = []
    for x in emojis:
      if x not in filtered:
        filtered.append(x)
    emojis = filtered
    if not need_to_add_flags and has_flag(emojis):
      need_to_add_flags = True
    text = converter.convert(text)
    results.setdefault(text, [])
    for x in emojis:
      if x not in results[text]:
        results[text].append(x)
  if need_to_add_flags:
    add_flags(results)
  for k in results:
    results[k] = [k] + results[k]
  return results

def main():
  for fn in os.listdir(input_dir):
    if re.search(r'\.txt$', fn):
      translated = simplify(fn)
      keys = sorted(translated.keys())
      with open(f'{output_dir}/{fn}', 'w') as fw:
        for k in keys:
          fw.write('{}\t{}\n'.format(k, ' '.join(translated[k])))

if __name__ == '__main__':
  main()
