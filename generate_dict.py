from datetime import datetime

from util import read_file

UNICODE_VERSION = 17

today = datetime.now().strftime('%Y.%m.%d')
version = f"unicode_{UNICODE_VERSION}_{today}"

output_dir = 'generated'
output_dict_fn_format = '{}.dict.yaml'

pinyin_id = 'caspal_pinyin_unicode'
pinyin_simp_id = f'{pinyin_id}_simp'
pinyin_trad_id = f'{pinyin_id}_trad'
pinyin_other_id = f'{pinyin_id}_other'

phrase_id = 'caspal_pinyin_phrase'

fuma_id = 'caspal_wubi_fuma'
wubi_id = 'caspal_wubi86'

output_fn_pinyin = output_dict_fn_format.format(pinyin_id)
output_fn_pinyin_simp = output_dict_fn_format.format(pinyin_simp_id)
output_fn_pinyin_trad = output_dict_fn_format.format(pinyin_trad_id)
output_fn_pinyin_other = output_dict_fn_format.format(pinyin_other_id)

output_fn_phrase = output_dict_fn_format.format(phrase_id)

output_fn_fuma_dict = output_dict_fn_format.format(fuma_id)
output_fn_wubi_dict = output_dict_fn_format.format(wubi_id)

header_template = '''# author: Caspal

---
name: {id}
version: "{v}"
sort: by_weight
use_preset_vocabulary: {p}
...

'''

header_pinyin_simp = header_template.format(id=pinyin_simp_id, v=version, p='false')
header_pinyin_trad = header_template.format(id=pinyin_trad_id, v=version, p='false')
header_pinyin_other = header_template.format(id=pinyin_other_id, v=version, p='false')

header_pinyin = '''# author: Caspal

---
name: {id}
version: "{v}"
sort: by_weight
vocabulary: essay-zh-hans
import_tables:
  - {simp_id}
  - {other_id}
  - {trad_id}
  - {phrase_id}
...

'''.format(id=pinyin_id, v=version, simp_id=pinyin_simp_id, other_id=pinyin_other_id, trad_id=pinyin_trad_id,
           phrase_id=phrase_id)

header_pinyin_phrase = header_template.format(id=phrase_id, v=version, p='false')

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


def get_variant_tables():
    simp_set = set()
    trad_set = set()
    lines = read_file('libs/OpenCC/data/dictionary/STCharacters.txt')
    for line in lines:
        s, t = line.split('\t')
        s = s.strip()
        t = t.split(' ')
        simp_set.add(s)
        for x in t:
            trad_set.add(x)

    lines = read_file('libs/OpenCC/data/dictionary/TSCharacters.txt')
    for line in lines:
        t, s = line.split('\t')
        t = t.strip()
        s = s.split(' ')
        trad_set.add(t)
        for x in s:
            simp_set.add(x)
    # not included in OpenCC
    for c in {'𰻝', '𮧵'}:
        simp_set.add(c)
    for c in {'𰻞', '韡'}:
        trad_set.add(c)
    return simp_set, trad_set


def output_dict_file(data_map: dict[str, str], output_fn: str, header: str):
    keys = sorted(data_map.keys())
    with open('{}/{}'.format(output_dir, output_fn), 'w') as f:
        f.write(header)
        for key in keys:
            for content in sorted(data_map[key]):
                f.write('{}\t{}\n'.format(key, content))


def generate_wubi_dict():
    wubi86_map = {}
    lines = read_file('{}/{}'.format(output_dir, 'caspal_wubi86.txt'))
    for line in lines:
        ch, wubi = line.split('\t')
        wubi86_map.setdefault(ch, set()).add(wubi)

    keys = sorted(wubi86_map.keys())
    with open('{}/{}'.format(output_dir, output_fn_wubi_dict), 'w') as f:
        f.write(header_wubi)
        for key in keys:
            for wubi in sorted(wubi86_map[key]):
                f.write('{}\t{}\n'.format(key, wubi))
        with open("{}/{}".format(output_dir, 'caspal_phrase_pinyin.txt')) as fph:
            lines = fph.readlines()
        f.write('\n')
        f.write('# 以下为词组\n')
        distinct_phrases = sorted({line.split('\t')[0] for line in lines})
        for phrase in distinct_phrases:
            f.write('{}\n'.format(phrase))


def pinyin():
    pinyin_simp_map = {}
    pinyin_trad_map = {}
    pinyin_other_map = {}

    simp_set, trad_set = get_variant_tables()

    lines = read_file('{}/{}'.format(output_dir, 'caspal_pinyin_freq.txt'))
    for line in lines:
        ch, pinyin_freq = line.split('\t', 1)
        included = False
        if ch in simp_set:
            pinyin_simp_map.setdefault(ch, set()).add(pinyin_freq)
            included = True
        if ch in trad_set:
            pinyin_trad_map.setdefault(ch, set()).add(pinyin_freq)
            included = True
        if not included:
            pinyin_other_map.setdefault(ch, set()).add(pinyin_freq)

    with open('{}/{}'.format(output_dir, output_fn_pinyin), 'w') as f:
        f.write(header_pinyin)

    output_dict_file(pinyin_simp_map, output_fn_pinyin_simp, header_pinyin_simp)
    output_dict_file(pinyin_trad_map, output_fn_pinyin_trad, header_pinyin_trad)
    output_dict_file(pinyin_other_map, output_fn_pinyin_other, header_pinyin_other)

    with open('{}/{}'.format(output_dir, output_fn_phrase), 'w') as f:
        f.write(header_pinyin_phrase)
        lines = read_file('{}/{}'.format(output_dir, 'caspal_phrase_pinyin.txt'))
        distinct_phrases = sorted(set(lines))
        for phrase in distinct_phrases:
            f.write('{}\n'.format(phrase))


def generate_fuma_dict():
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

    output_dict_file(fuma_map, output_fn_fuma_dict, header_fuma)


def main():
    pinyin()
    generate_fuma_dict()
    generate_wubi_dict()


if __name__ == '__main__':
    main()
