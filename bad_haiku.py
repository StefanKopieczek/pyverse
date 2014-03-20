import rhymelib
import random

rhymelib.OBSCURITY_LIMIT = 1000


class Haiku(object):
    def __init__(self):
        self.lines = [Line(5), Line(7), Line(5)]

    def __str__(self):
        return '\n'.join((str(line) for line in self.lines)) + '.'


class Line(object):
    def __init__(self, syllables):
        self.contents = self.write_line(syllables)

    def __str__(self):
        return (self.contents[0][0].upper() +
                self.contents[0][1:] + ' ' +
                ' '.join(self.contents[1:]))

    def write_line(self, syllables):
        # In no way efficient, but I don't care.
        syllables_left = syllables
        words = []
        while syllables_left > 0:
            word = random.choice(list(rhymelib.words()))
            num_syllables = rhymelib.getnumsyllables(word)
            if num_syllables <= syllables_left:
                syllables_left -= num_syllables
                words.append(word)

        return words


if __name__ == "__main__":
    print Haiku()
