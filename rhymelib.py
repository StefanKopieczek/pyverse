import cPickle
import nltk
from nltk.corpus import cmudict
from nltk.corpus import brown

from collections import defaultdict

_wordset = None
_word_to_rhyme_dict = None
_word_to_pronunciation_dict = None
_rhyme_to_words_dict = None

DATABASE_FILE = "rhyme.db"
OBSCURITY_LIMIT = 2000


class RhymeDB(object):

    _instance = None

    def __init__(self, obscurity_limit):
        self.wordset = None
        self.word_to_rhyme_dict = None
        self.word_to_pronunciation_dict = None
        self.rhyme_to_words_dict = None
        self.obscurity_limit = obscurity_limit
        self.load(obscurity_limit)

    @classmethod
    def get_instance(clazz, obscurity_limit=None):
        if obscurity_limit is None:
            obscurity_limit = OBSCURITY_LIMIT

        if clazz._instance is None:
            clazz._instance = RhymeDB(obscurity_limit=obscurity_limit)

        if clazz._instance.obscurity_limit != obscurity_limit:
            clazz._instance.load(obscurity_limit=obscurity_limit)

        return clazz._instance

    def load(self, obscurity_limit):
        print "Loading rhyme database."
        valid = True
        try:
            self.load_from_file(DATABASE_FILE)
            print "Database loaded.\n"
        except IOError:
            print "Could not find database file."
            valid = False
        if valid and self.obscurity_limit != obscurity_limit:
            print "Loaded DB doesn't match the requested parameters."
            valid = False
        if not valid:
            print "\nGenerating a new DB..."
            self.generate(obscurity_limit)
            print "New DB generated. Saving to disc...",
            self.save_to_file(DATABASE_FILE)
            print "[Saved]\n"

    def load_from_file(self, addr):
        f = open(addr, 'r')
        delegate = cPickle.load(f)
        f.close()
        self.__dict__ = delegate.__dict__

    def save_to_file(self, addr):
        f = open(addr, 'w')
        pickler = cPickle.Pickler(f)
        pickler.dump(self)
        f.close()

    def generate(self, obscurity_limit):
        _load_corpora(require_brown=(obscurity_limit is not None))
        self.wordset = RhymeDB._build_wordset(obscurity_limit=obscurity_limit)
        self.word_to_rhyme_dict = {}
        self.word_to_pronunciation_dict = {}
        self.rhyme_to_words_dict = defaultdict(set)
        self.obscurity_limit = obscurity_limit
        for word, pron in self.wordset:
            if word in self.word_to_rhyme_dict:
                continue  # Skip nonstandard pronunciations
            rhyme_type = _get_rhyme_type(pron)
            self.word_to_pronunciation_dict[word] = pron
            self.word_to_rhyme_dict[word] = rhyme_type
            self.rhyme_to_words_dict[rhyme_type].add(word)

    @classmethod
    def _build_wordset(clazz, obscurity_limit):
        words = cmudict.entries()
        if obscurity_limit is not None:
            freqs = nltk.FreqDist([w.lower() for w in brown.words()])
            words = sorted(words,
                           key=lambda x: freqs[x[0].lower()],
                           reverse=True)
            return words[:obscurity_limit]
        else:
            return list(words)


def words():
    db = RhymeDB.get_instance()
    for word, pron in db.wordset:
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


def rhymeswith(word1, word2):
    db = RhymeDB.get_instance()
    return db.word_to_rhyme_dict[word1] == db.word_to_rhyme_dict[word2]


def getrhymes(word):
    db = RhymeDB.get_instance()
    return [match for match in
            db.rhyme_to_words_dict[db.word_to_rhyme_dict[word]]
            if match != word]


def getnumsyllables(word):
    db = RhymeDB.get_instance()
    return len([sound for sound in db.word_to_pronunciation_dict[word]
                if sound[-1] in ['0', '1', '2']])


def stresses(word):
    db = RhymeDB.get_instance()
    pron = db.word_to_pronunciation_dict[word]
    vowels = [sound for sound in pron if sound[-1] in ['0', '1', '2']]
    main_stress_idx = [idx for idx, vowel in enumerate(vowels)
                       if vowel[-1] == '1'][0]
    parity = main_stress_idx % 2
    return [(idx + parity + 1) % 2 for idx in xrange(len(vowels))]


def _get_rhyme_type(pron):
    stress_list = [(sound, idx) for idx, sound in enumerate(pron)
                   if sound[-1] == '1']
    if len(stress_list) > 0:
        pron = pron[stress_list[0][1]:]
    return tuple(pron)


def _load_corpora(require_brown=True):
    from nltk.corpus import cmudict
    try:
        cmudict.entries()
    except LookupError:
        print "CMUDict corpus not found. Downloading..."
        nltk.download('cmudict')
        print "[Done]"

    if require_brown:
        from nltk.corpus import brown
        try:
            brown.words()
        except LookupError:
            print "Brown corpus not found. Downloading...",
            nltk.download('brown')
            print "[Done]"
