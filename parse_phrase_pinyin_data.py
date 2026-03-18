#!/usr/bin/env python3

from util import read_file, untone, remove_duplicates

output_dir = 'generated'
output_fn = 'caspal_phrase_pinyin.txt'


def main():
    lines = read_file('libs/phrase-pinyin-data/large_pinyin.txt')
    lines += read_file('data/extend_phrase_pinyin.txt')

    lines = [untone(x) for x in lines]
    lines = remove_duplicates(lines)

    with open('{}/{}'.format(output_dir, output_fn), 'w') as f:
        for line in lines:
            phrase, pinyin = [x.strip() for x in line.split(':', 1)]
            f.write('{}\t{}\n'.format(phrase, pinyin))


if __name__ == '__main__':
    main()
