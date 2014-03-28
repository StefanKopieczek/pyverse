import random


class VersePack(object):
    def __init__(self):
        # TODO
        pass

    def similar_words(self, word, threshold=0.5):
        # Mockup - TODO
        return ["death", "doom", "gloom", "breath"]

    def choose_words(self, syllables, start_list=None, end_list=None):
        return None  # TODO

    def select_trigram(self, word1, word2=None, reverse=True):
        options = self.get_trigrams(word1, word2=word2, reverse=reverse)
        cumulative_probability = 0
        critical_point = random.random()
        for trigram, chance in options:
            cumulative_probability += chance
            if cumulative_probability >= critical_point:
                return trigram

    def get_trigrams(self, word1, word2=None, reverse=True):
        # Mockup - TODO
        if word2 is None:
            word2 = "banana"

        word3 = "chimp"

        if reverse:
            word1, word3 = word3, word1

        results = [tuple(word1, word2, word3), 0.5]

        # Normalize the possible trigrams, so the probabilities sum to 1.
        total_frequency = sum((chance for trigram, chance in results))
        results = [(trigram, float(chance)/total_frequency)
                   for trigram, chance in results]

        return results
