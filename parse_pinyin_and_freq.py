import re

from util import get_code_points, read_file, remove_duplicates, untone

output_dir = 'generated'
output_fn = 'caspal_pinyin_freq.txt'


def get_jieba_data() -> dict[str, int]:
    jieba_data = {}
    lines = read_file('libs/jieba/extra_dict/dict.txt.big')
    for line in lines:
        split = line.split()
        if len(split) < 2:
            # print(line)
            continue
        ch = split[0]
        freq = int(split[1])
        jieba_data[ch] = freq
    return jieba_data


def parse_phrase_pinyin_data(jieba_data: dict[str, int]) -> dict[str, dict[str, int]]:
    char_pinyin_freq_map = {}
    pinyin_char_freq_map = {}
    lines = read_file('libs/phrase-pinyin-data/large_pinyin.txt')
    lines += read_file('data/extend_phrase_pinyin.txt')

    lines = [untone(x) for x in lines]
    lines = remove_duplicates(lines)

    for line in lines:
        phrase, pinyins = [x.strip() for x in line.split(':', 1)]
        pinyins = pinyins.split()
        assert len(phrase) == len(pinyins)
        freq = jieba_data.get(phrase, 1)
        for i in range(len(phrase)):
            ch = phrase[i]
            pinyin = pinyins[i]
            char_pinyin_freq = char_pinyin_freq_map.get(ch, {})
            char_pinyin_freq[pinyin] = char_pinyin_freq.get(pinyin, 0) + freq
            char_pinyin_freq_map[ch] = char_pinyin_freq

            pinyin_char_freq = pinyin_char_freq_map.get(pinyin, {})
            pinyin_char_freq[ch] = pinyin_char_freq.get(ch, 0) + freq
            pinyin_char_freq_map[pinyin] = pinyin_char_freq
    return char_pinyin_freq_map


def add_pinyin_data(char_pinyin_freq_map):
    lines = read_file('libs/pinyin-data/pinyin.txt')
    lines += read_file('data/overwrite_pinyin.txt')
    code_points = get_code_points()
    for line in lines:
        code, pinyins = [x.strip() for x in line.split(':', 1)]
        cp = int(code[2:], 16)
        if cp not in code_points['all'] and cp not in code_points['pua']:
            print('Non-CJK Ideograph {}({}) found'.format(chr(cp), code))
        ch = chr(cp)
        char_pinyin_freq = char_pinyin_freq_map.get(ch, {})
        for pinyin in pinyins.split(','):
            py = untone(pinyin.strip())
            if re.search(r'^[^aeiouv]+$|[^a-z]', py):
                continue
            char_pinyin_freq[py] = char_pinyin_freq.get(py, 0) + 1
        char_pinyin_freq_map[ch] = char_pinyin_freq

    for ch in char_pinyin_freq_map:
        if not char_pinyin_freq_map[ch]:
            print(ch, f'U+{ord(ch):X}', 'no pinyin')
            del char_pinyin_freq_map[ch]


def format_percentage(num):
    return f"{round(num * 100, 2):g}%"


def main():
    jieba_data = get_jieba_data()
    pinyin_freq_map = parse_phrase_pinyin_data(jieba_data)
    add_pinyin_data(pinyin_freq_map)

    chars = sorted(pinyin_freq_map.keys())

    with open('{}/{}'.format(output_dir, output_fn), 'w') as f:
        for ch in chars:
            pinyins = [k for k, v in sorted(pinyin_freq_map[ch].items(), key=lambda item: item[1], reverse=True)]
            length = len(pinyins)
            total_freq = sum(pinyin_freq_map[ch].values())
            if length > 1:
                for pinyin in pinyins:
                    freq_str = format_percentage(pinyin_freq_map[ch][pinyin] / total_freq)
                    f.write('{}\t{}\t{}\n'.format(ch, pinyin, freq_str))
            elif length == 1:
                f.write('{}\t{}\n'.format(ch, pinyins[0]))


if __name__ == '__main__':
    main()
