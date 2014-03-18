import rhymelib
import random

rhymelib.OBSCURITY_LIMIT = 1000


class Limerick(object):
    def __init__(self):
        self.lines = [PrimaryLine()]
        self.lines.append(PrimaryLine(rhyme=self.lines[0].final_word))
        self.lines.append(SecondaryLine())
        self.lines.append(SecondaryLine(rhyme=self.lines[2].final_word))
        self.lines.append(PrimaryLine(rhyme=self.lines[0].final_word))

    def __str__(self):
        return '\n'.join((str(line) for line in self.lines)) + '.'


class Line(object):
    def __init__(self, rhyme=None):
        self.final_word = self.__class__.choose_final_word(rhyme)
        self.contents = self.__class__.expand_line([self.final_word])

    def __str__(self):
        return (self.contents[0][0].upper() +
                self.contents[0][1:] + ' ' +
                ' '.join(self.contents[1:]))

    @classmethod
    def choose_final_word(clazz, rhyme):
        final_word = None
        if rhyme is None:
            while True:
                final_word = random.choice(list(rhymelib.words()))
                if len(limericky_rhymes(final_word)) > 0:
                    # The word has rhyming potential - let's use it!
                    break
        else:
            final_word = random.choice(limericky_rhymes(rhyme))

        return final_word

    @classmethod
    def expand_line(clazz, wordlist):
        # In no way efficient, but I don't care.
        syllables_left = clazz.syllables - sum((rhymelib.getnumsyllables(word)
                                               for word in wordlist))
        stress_needed = 1 if (syllables_left % 3 == 0) else 0

        while syllables_left > 0:
            word = random.choice(list(rhymelib.words()))
            num_syllables = rhymelib.getnumsyllables(word)
            stresses = rhymelib.stresses(word)
            if (num_syllables <= syllables_left and
                    (stresses[-1] == stress_needed or num_syllables == 1)):
                wordlist = [word] + wordlist
                syllables_left -= num_syllables
                stress_needed = 1 if (syllables_left % 3 == 0) else 0

        return wordlist


class PrimaryLine(Line):
    syllables = 9


class SecondaryLine(Line):
    syllables = 6


def limericky_rhymes(word):
    return [rhyme for rhyme in rhymelib.getrhymes(word)
            if word != rhyme and
            (rhymelib.stresses(rhyme)[-1] == 1 or
             rhymelib.getnumsyllables(rhyme) == 1)]


if __name__ == "__main__":
    print Limerick()
