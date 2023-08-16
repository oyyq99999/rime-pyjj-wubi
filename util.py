
import re

def get_code_points():
  code_points = {'all': set(), 'uni': set(), 'pua': set()}
  code_points['pua'].update(range(0xe000, 0xf8ff + 1))
  code_points['pua'].update(range(0xf0000, 0x10ffff + 1))
  expected_size = 0

  # CJK Unified Ideographs Extension A
  expected_size += 6582 + 10
  code_points['uni'].update(range(0x3400, 0x4db5 + 1))
  code_points['uni'].update(range(0x4db6, 0x4dbf + 1))
  code_points['all'].update(range(0x3400, 0x4dbf + 1))
  assert len(code_points['all']) == expected_size

  # CJK Unified Ideographs
  expected_size += 20902 + 22 + 8 + 8 + 1 + 9 + 21 + 5 + 13 + 3
  code_points['uni'].update(range(0x4e00, 0x9fa5 + 1))
  code_points['uni'].update(range(0x9fa6, 0x9fff + 1))
  code_points['all'].update(range(0x4e00, 0x9fff + 1))
  assert len(code_points['all']) == expected_size

  # CJK Unified Ideographs Extension B
  expected_size += 42711 + 7 + 2
  code_points['uni'].update(range(0x20000, 0x2a6d6 + 1))
  code_points['uni'].update(range(0x2a6d7, 0x2a6df + 1))
  code_points['all'].update(range(0x20000, 0x2a6df + 1))
  assert len(code_points['all']) == expected_size

  # CJK Unified Ideographs Extension C
  expected_size += 4149 + 4 + 1
  code_points['uni'].update(range(0x2a700, 0x2b739 + 1))
  code_points['all'].update(range(0x2a700, 0x2b739 + 1))
  assert len(code_points['all']) == expected_size

  # CJK Unified Ideographs Extension D
  expected_size += 222
  code_points['uni'].update(range(0x2b740, 0x2b81d + 1))
  code_points['all'].update(range(0x2b740, 0x2b81d + 1))
  assert len(code_points['all']) == expected_size

  # CJK Unified Ideographs Extension E
  expected_size += 5762
  code_points['uni'].update(range(0x2b820, 0x2cea1 + 1))
  code_points['all'].update(range(0x2b820, 0x2cea1 + 1))
  assert len(code_points['all']) == expected_size

  # CJK Unified Ideographs Extension F
  expected_size += 7473
  code_points['uni'].update(range(0x2ceb0, 0x2ebe0 + 1))
  code_points['all'].update(range(0x2ceb0, 0x2ebe0 + 1))
  assert len(code_points['all']) == expected_size

  # CJK Unified Ideographs Extension G
  expected_size += 4939
  code_points['uni'].update(range(0x30000, 0x3134a + 1))
  code_points['all'].update(range(0x30000, 0x3134a + 1))
  assert len(code_points['all']) == expected_size

  # CJK Unified Ideographs Extension H
  expected_size += 4192
  code_points['uni'].update(range(0x31350, 0x323af + 1))
  code_points['all'].update(range(0x31350, 0x323af + 1))
  assert len(code_points['all']) == expected_size

  # CJK Compatibility Ideographs
  expected_size += 302 + 2 + 59 + 3 + 106
  code_points['all'].update(range(0xf900, 0xfa6d + 1))
  code_points['all'].update(range(0xfa70, 0xfad9 + 1))
  assert len(code_points['all']) == expected_size

  # CJK Compatibility Supplement
  expected_size += 542
  code_points['all'].update(range(0x2f800, 0x2fa1d + 1))
  assert len(code_points['all']) == expected_size

  # CJK Radicals Supplement
  expected_size += 26 + 89
  code_points['all'].update(range(0x2e80, 0x2e99 + 1))
  code_points['all'].update(range(0x2e9b, 0x2ef3 + 1))
  assert len(code_points['all']) == expected_size

  # Kangxi Radicals
  expected_size += 214
  code_points['all'].update(range(0x2f00, 0x2fd5 + 1))
  assert len(code_points['all']) == expected_size

  # CJK Symbols and Punctuation
  expected_size += 56 + 3 + 3 + 1 + 1
  code_points['all'].update(range(0x3000, 0x303f + 1))
  assert len(code_points['all']) == expected_size

  # Kanbun
  expected_size += 16
  code_points['all'].update(range(0x3190, 0x319f + 1))
  assert len(code_points['all']) == expected_size

  # CJK Strokes
  expected_size += 16 + 20
  code_points['all'].update(range(0x31c0, 0x31e3 + 1))
  assert len(code_points['all']) == expected_size

  # Enclosed CJK Letters and Months
  expected_size += 36 + 12 + 49 + 12 + 47 + 1
  code_points['all'].update(range(0x3220, 0x324f + 1))
  code_points['all'].update(range(0x3280, 0x32b0 + 1))
  code_points['all'].update(range(0x32c0, 0x32cb + 1))
  code_points['all'].update(range(0x32d0, 0x32ff + 1))
  assert len(code_points['all']) == expected_size

  # CJK Compatibility
  expected_size += 25 + 5 + 31
  code_points['all'].update(range(0x3358, 0x3370 + 1))
  code_points['all'].update(range(0x337b, 0x337f + 1))
  code_points['all'].update(range(0x33e0, 0x33fe + 1))
  assert len(code_points['all']) == expected_size

  # Enclosed Ideographic Supplement
  expected_size += 34 + 9 + 1 + 9 + 2
  code_points['all'].update(range(0x1f210, 0x1f23b + 1))
  code_points['all'].update(range(0x1f240, 0x1f248 + 1))
  code_points['all'].update(range(0x1f250, 0x1f251 + 1))
  assert len(code_points['all']) == expected_size

  return code_points

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
