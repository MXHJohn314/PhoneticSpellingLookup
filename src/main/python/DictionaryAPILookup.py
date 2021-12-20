def make_files(speller, word):
    return DictionaryAPILookup(speller, word)

class DictionaryAPILookup:
    def __init__(self, speller, word):
        self.ipa_spelling = None
        self.syllabic_spelling = None
        self.speller = speller
        self.word = word

    def syllable_count(self):
        return len(self.syllabic_spelling)

    def get_syllable_spelling(self):
        return "-".join(self.syllabic_spelling)

    def get_phoneme_arrays(self):
        return self.ipa_spelling

    def syllable_insert(self):
        return self.syllabic_spelling

    def get_word(self):
        return self.word
