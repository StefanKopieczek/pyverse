import nltk
from nltk.corpus import cmudict
from nltk.corpus import brown

from collections import defaultdict

_wordset = None
_word_to_rhyme_dict = None
_word_to_pronunciation_dict = None
_rhyme_to_words_dict = None

USE_TEST_DICT = False
WORDSET_LENGTH = 2000


def requireswordset(f):
    def requireswordset_inner(*args, **kwargs):
        global _wordset
        if _wordset is None:
            _wordset = _get_wordset()
        return f(*args, **kwargs)

    return requireswordset_inner


def requiresdicts(f):
    def requiresdicts_inner(*args, **kwargs):
        if (_word_to_rhyme_dict is None or
                _rhyme_to_words_dict is None or
                _word_to_pronunciation_dict is None):
                load_rhyme_dicts()
        return f(*args, **kwargs)

    return requiresdicts_inner


@requireswordset
def words():
    for word, pron in _wordset:
        yield word


def lowercase_args(f):
    def lowercase_args_inner(*args, **kwargs):
        args = [arg if not hasattr(arg, 'lower') else arg.lower()
                for arg in args]
        for key in kwargs:
            if hasattr(kwargs[key], 'lower'):
                kwargs[key] = kwargs[key].lower()
        return f(*args, **kwargs)

    return lowercase_args_inner


@requiresdicts
@lowercase_args
def rhymeswith(word1, word2):
    global _word_to_rhyme_dict
    return _word_to_rhyme_dict[word1] == _word_to_rhyme_dict[word2]


@requiresdicts
@lowercase_args
def getrhymes(word):
    global _rhyme_to_words_dict
    return [match for match in _rhyme_to_words_dict[_word_to_rhyme_dict[word]]
            if match != word]


@requiresdicts
@lowercase_args
def getnumsyllables(word):
    global _word_to_pronunciation_dict
    return len([sound for sound in _word_to_pronunciation_dict[word]
                if sound[-1] in ['0', '1', '2']])


@requiresdicts
@lowercase_args
def stresses(word):
    global _word_to_pronunciation_dict
    pron = _word_to_pronunciation_dict[word]
    vowels = [sound for sound in pron if sound[-1] in ['0', '1', '2']]
    main_stress_idx = [idx for idx, vowel in enumerate(vowels)
                       if vowel[-1] == '1'][0]
    parity = main_stress_idx % 2
    return [(idx + parity + 1) % 2 for idx in xrange(len(vowels))]


@requireswordset
def load_rhyme_dicts():
    global _word_to_rhyme_dict
    global _rhyme_to_words_dict
    global _word_to_pronunciation_dict
    _word_to_rhyme_dict = {}
    _word_to_pronunciation_dict = {}
    _rhyme_to_words_dict = defaultdict(set)
    for word, pron in _wordset:
        if word in _word_to_rhyme_dict:
            continue # Skip nonstandard pronunciations
        rhyme_type = _get_rhyme_type(pron)
        _word_to_pronunciation_dict[word] = pron
        _word_to_rhyme_dict[word] = rhyme_type
        _rhyme_to_words_dict[rhyme_type].add(word)


def _get_rhyme_type(pron):
    stress_list = [(sound, idx) for idx, sound in enumerate(pron)
                   if sound[-1] == '1']
    if len(stress_list) > 0:
        pron = pron[stress_list[0][1]:]
    return tuple(pron)


def _get_wordset():
    global USE_TEST_DICT
    if USE_TEST_DICT:
        return cmudict.entries()[:100]
    else:
        words = cmudict.entries()
        freqs = nltk.FreqDist([w.lower() for w in brown.words()])
        words = sorted(words, key=lambda x: freqs[x[0].lower()], reverse=True)
        return words[:WORDSET_LENGTH]
        return cmudict.entries()
