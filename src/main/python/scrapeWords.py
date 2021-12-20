import mysql.connector
import configparser
import json


class LayoutGenerator:
    def __init__(self, ini='config.ini'):
        self.layout = {
        }
        config = configparser.ConfigParser()
        config.read(ini)
        server = config['database.local']['server']
        database = config['database.local']['database']
        user_ = config['database.local']['user']
        password_ = config['database.local']['password']

        self.conn = mysql.connector.connect(
            host=server,
            user=user_,
            password=password_
        )
        self.conn.database = database
        print(f'connected to {user_}@{server}/{database}')
        self.conn.cursor().execute('use syllables')

    def create_tables(self, path):
        csv_file = open(path, 'rb')
        j = json
        c = self.conn.cursor()
        c.execute('use stenography')

        ipa_chars = {}
        syllables = {}
        words = {}

        word_count = 0
        syllable_count = 0
        char_count = 0

        words_insert = []
        syllables_insert = []
        phonemes_insert = []
        frequencies_insert = []
        syllables_phonemes_insert = []

        for line in csv_file:
            word_count += 1
            split = line.split(',')
            word_count, word = self.add(words, word)
            chars = split[1:len(split) - 1]
            for unicode in chars:
                syllable = json.loads('{\"sound\":\"\\' + unicode + '\"}')['sound']
                syllable_count, syllable = self.add(syllables, syllable)
                # add batch to
                for char in syllables:
                    char_count, _ = self.add(chars, char)
                    
                
        c.execute('select * from syllables')
        data = c.fetchall()
        sounds = {}
        out = ''

        """
        words (id int, word);
        syllables(id,syllables);
        phonemes(id,phoneme);
        frequencies(id,freq);
        words_syllables(word_id,syllable_id,position);
        syllables_phonemes(syllable_id,phoneme_id,position);
        """
        for id, unicode in data:
            syllable = j.loads('{\"sound\":\"\\' + unicode + '\"}')['sound']
            for char in syllable:
                if char in sounds:
                    sounds[char] += 1
                else:
                    sounds[char] = 1
                    out += char + '\n'
        print(out)

        def close():
            self.conn.close()


gen = LayoutGenerator()
gen.create_tables('5000MostCommonWordsPhonemes.csv')
gen.close()
