vpath %.txt data:generated:opencc:libs/OpenCC/data/dictionary
vpath wubi86%.dict.yaml libs/rime-wubi:libs/rime-wubi86-ext
vpath %.dict.yaml generated

VENV = .venv
PYTHON = $(VENV)/bin/python
UV = uv
export UNICODE_VERSION = 17

pinyin_txts := caspal_pinyin_freq.txt caspal_phrase_pinyin.txt
pinyin_dicts := caspal_pinyin_phrase.dict.yaml caspal_pinyin_unicode$(UNICODE_VERSION).dict.yaml \
	caspal_pinyin_unicode$(UNICODE_VERSION)_simp.dict.yaml caspal_pinyin_unicode$(UNICODE_VERSION)_trad.dict.yaml \
	caspal_pinyin_unicode$(UNICODE_VERSION)_other.dict.yaml
opencc_txts := STCharacters.txt TSCharacters.txt

phrase_pinyin_sources := libs/phrase-pinyin-data/large_pinyin.txt extend_phrase_pinyin.txt
pinyin_freq_sources := libs/jieba/extra_dict/dict.txt.big $(phrase_pinyin_sources) libs/pinyin-data/pinyin.txt overwrite_pinyin.txt


wubi_sources := wubi86.dict.yaml wubi86.basiccmpl.dict.yaml \
	wubi86.extacmpl.dict.yaml wubi86.extbcmpl.dict.yaml \
	wubi86.extc.dict.yaml wubi86.extccmpl.dict.yaml \
	wubi86.extd.dict.yaml wubi86.exte.dict.yaml \
	wubi86.extf.dict.yaml wubi86.extg.dict.yaml \
	wubi86.exth.dict.yaml

wubi_txts := caspal_wubi86.txt caspal_wubi86_fuma.txt
wubi_dicts := caspal_wubi86.dict.yaml caspal_wubi_fuma.dict.yaml

dicts = $(pinyin_dicts) $(wubi_dicts)

emojis := emoji_category.txt emoji_word.txt
emoji_sources := libs/rime-emoji/opencc/emoji_category.txt libs/rime-emoji/opencc/emoji_word.txt

.PHONY : $(VENV) all clean

all : $(VENV) $(dicts) $(emojis)

$(VENV):
	$(UV) sync

$(dicts) &: $(pinyin_txts) $(wubi_txts) $(opencc_txts) generate_dict.py
	$(PYTHON) generate_dict.py

caspal_pinyin_freq.txt : $(pinyin_freq_sources) parse_pinyin_and_freq.py
	$(PYTHON) parse_pinyin_and_freq.py

caspal_phrase_pinyin.txt : $(phrase_pinyin_sources) parse_phrase_pinyin_data.py
	$(PYTHON) parse_phrase_pinyin_data.py

$(wubi_txts) &: $(wubi_sources) combine_wubi.py
	$(PYTHON) combine_wubi.py

$(emojis) &: $(emoji_sources) simplified_emoji.py
	$(PYTHON) simplified_emoji.py

clean :
	rm -rf generated/*
	rm -f opencc/*.txt

