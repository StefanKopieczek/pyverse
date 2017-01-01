import rhymelib
import itertools
import random

rhymelib.OBSCURITY_LIMIT = 4000


class Villanelle(object):
    def __init__(self):
        refrain_rhyme_words = get_rhyme_words(7)
        offhand_rhyme_words = get_rhyme_words(6)
        onhand_lines = map(Line, refrain_rhyme_words)
        offhand_lines = map(Line, offhand_rhyme_words)
        refrain_lines, onhand_lines = onhand_lines[:2], onhand_lines[2:]

        refrain = itertools.cycle(refrain_lines)
        onhand = iter(onhand_lines)
        offhand = iter(offhand_lines)

        stanzas = [Stanza(refrain.next(), offhand.next(), refrain.next())]

        for _ in xrange(4):
            stanzas.append(Stanza(onhand.next(), offhand.next(), refrain.next()))

        stanzas.append(Stanza(onhand.next(), offhand.next(), refrain.next(), refrain.next()))

        self.stanzas = stanzas

    def __str__(self):
        return '\n\n'.join((str(stanza) for stanza in self.stanzas))


class Stanza(object):
    def __init__(self, *args):
        self.lines = args

    def __str__(self):
        return '\n'.join([str(line) for line in self.lines]) + '.'


class Line(object):
    def __init__(self, final_word=None):
        self.final_word = final_word
        self.contents = Line.expand_line([self.final_word])

    def __str__(self):
        return (self.contents[0][0].upper() +
                self.contents[0][1:] + ' ' +
                ' '.join(self.contents[1:]))


    @classmethod
    def expand_line(clazz, wordlist):
        # In no way efficient, but I don't care.
        syllables_left = 10 - sum((rhymelib.getnumsyllables(word)
                                  for word in wordlist))
        stress_needed = 1 - rhymelib.stresses(wordlist[0])[0]
        while syllables_left > 0:
            word = random.choice(list(rhymelib.words()))
            num_syllables = rhymelib.getnumsyllables(word)
            stresses = rhymelib.stresses(word)
            if (num_syllables <= syllables_left and
                    (stresses[-1] == stress_needed or num_syllables == 1)):
                wordlist = [word] + wordlist
                syllables_left -= num_syllables
                stress_needed = (stress_needed + num_syllables) % 2

        return wordlist


def get_rhyme_words(n):
    all_words = list(rhymelib.words())
    rhyme_words = []
    while len(rhyme_words) < n:
        rhyme_words = acceptable_rhymes(random.choice(all_words))

    return rhyme_words[:n]


def acceptable_rhymes(word):
    return [rhyme for rhyme in rhymelib.getrhymes(word)
            if (rhymelib.stresses(rhyme)[-1] == 1 or
                rhymelib.getnumsyllables(rhyme) == 1)]


if __name__ == "__main__":
    print Villanelle()
