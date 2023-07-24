#!/usr/bin/env python3

output_dir = 'generated'
output_fn = 'caspal_phrase_pinyin.txt'

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

def main():
  pinyin_map = {}
  with open('phrase-pinyin-data/pinyin.txt') as f:
    lines = f.readlines()
  lines = [line.strip() for line in lines]
  lines = list(filter(lambda x: len(x) > 0 and x[0] != '#', lines))

  with open('{}/{}'.format(output_dir, output_fn), 'w') as f:
    for line in lines:
      phrase, pinyin = [x.strip() for x in line.split(':', 1)]
      pinyin = untone(pinyin)
      f.write('{}\t{}\n'.format(phrase, pinyin))



if __name__ == '__main__':
  main()
