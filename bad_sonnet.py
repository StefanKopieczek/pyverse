import rhymelib
import random

words = list(rhymelib.words())


class Sonnet(object):
    def __init__(self):
        self.stanzas = [Quatrain(),
                        Quatrain(),
                        Quatrain(),
                        Couplet()]

    def __str__(self):
        return '\n\n'.join((str(stanza) for stanza in self.stanzas))


class Stanza(object):
    def __str__(self):
        return '\n'.join([str(line) for line in self.lines]) + '.'


class Quatrain(Stanza):
    def __init__(self):
        self.lines = [Line(), Line()]
        self.lines.append(Line(rhyme=self.lines[0].final_word))
        self.lines.append(Line(rhyme=self.lines[1].final_word))


class Couplet(Stanza):
    def __init__(self):
        self.lines = [Line()]
        self.lines.append(Line(rhyme=self.lines[0].final_word))


class Line(object):
    def __init__(self, rhyme=None):
        self.final_word = Line.choose_final_word(rhyme)
        self.contents = Line.expand_line([self.final_word])

    def __str__(self):
        return (self.contents[0][0].upper() +
                self.contents[0][1:] + ' ' +
                ' '.join(self.contents[1:]))

    @classmethod
    def choose_final_word(clazz, rhyme):
        final_word = None
        if rhyme is None:
            while True:
                final_word = random.choice(words)
                if len(sonnetworthy_rhymes(final_word)) > 0:
                    # The word has rhyming potential - let's use it!
                    break
        else:
            final_word = random.choice(sonnetworthy_rhymes(rhyme))

        return final_word

    @classmethod
    def expand_line(clazz, wordlist):
        # In no way efficient, but I don't care.
        syllables_left = 10 - sum((rhymelib.getnumsyllables(word)
                                  for word in wordlist))
        stress_needed = 1 - rhymelib.stresses(wordlist[0])[0]
        while syllables_left > 0:
            word = random.choice(words)
            num_syllables = rhymelib.getnumsyllables(word)
            stresses = rhymelib.stresses(word)
            if (num_syllables <= syllables_left and
                    (stresses[-1] == stress_needed or num_syllables == 1)):
                wordlist = [word] + wordlist
                syllables_left -= num_syllables
                stress_needed = (stress_needed + num_syllables) % 2

        return wordlist


def sonnetworthy_rhymes(word):
    return [rhyme for rhyme in rhymelib.getrhymes(word)
            if word != rhyme and
            (rhymelib.stresses(rhyme)[-1] == 1 or
             rhymelib.getnumsyllables(rhyme) == 1)]
