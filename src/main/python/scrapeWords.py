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

j = [{'meta': {'id': 'bottom:1', 'uuid': '509d64b7-137a-47e2-93af-617b8fb99f18', 'src': 'learners',
               'section': 'alpha',
               'target': {'tuuid': '79223b75-6a18-42ec-9f93-fbd3df16dabf', 'tsrc': 'collegiate'},
               'highlight': 'yes',
               'stems': ['bottom', 'bottoms', 'at bottom', 'at the bottom of the pile', 'be/lie at the bottom of', 'be at the bottom of', 'lie at the bottom of', 'bottoms up', 'from the bottom of your heart', 'from top to bottom', 'get to the bottom of', 'the bottom drops/falls out', 'the bottom drops out', 'the bottom falls out', 'the bottom of the barrel', 'bottomed', 'false bottom', 'at the bottom of her/the class', 'at the bottom of her class', 'at the bottom of the class', 'hit bottom', 'scraped bottom'],
               'app-shortdef': {'hw': 'bottom:1', 'fl': 'noun', 'def': ['{bc} the lowest part, point, or level of something', '{bc} the part of something that is below or under the other parts', '{bc} the lowest point or surface inside something {bc} the part of something hollow that is furthest from the top']},
               'offensive': False},
      'hom': 1,
      'hwi': {'hw': 'bot*tom', 'prs': [{'ipa': 'ˈbɑːtəm', 'sound': {'audio': 'bottom01'}}]},
      'fl': 'noun', 'ins': [{'il': 'plural', 'ifc': '-toms', 'if': 'bot*toms'}], 'def': [{'sseq': [[
                                                                                                       [
                                                                                                           'sense',
                                                                                                              {
                                                                                                               'sn': '1 a',
                                                                                                               'sgram': 'count',
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}the lowest part, point, or level of something'],
                                                                                                                   [
                                                                                                                       'uns',
                                                                                                                       [
                                                                                                                           [
                                                                                                                               [
                                                                                                                                   'text',
                                                                                                                                   'usually singular '],
                                                                                                                               [
                                                                                                                                   'vis',
                                                                                                                                   [
                                                                                                                                       {
                                                                                                                                           't': "He's waiting at the {it}bottom{/it} of the stairs."},
                                                                                                                                       {
                                                                                                                                           't': 'Our house is at the {it}bottom{/it} of the hill.'},
                                                                                                                                       {
                                                                                                                                           't': 'The top of the wall is painted and the {it}bottom{/it} is covered in wood paneling.'},
                                                                                                                                       {
                                                                                                                                           't': 'the {it}bottom{/it} of the page/screen/list'},
                                                                                                                                       {
                                                                                                                                           't': 'Please fill out this form and sign your name at the {it}bottom{/it}.'}]]]]]]}],
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': 'b',
                                                                                                               'sgram': 'count',
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}the part of something that is below or under the other parts'],
                                                                                                                   [
                                                                                                                       'uns',
                                                                                                                       [
                                                                                                                           [
                                                                                                                               [
                                                                                                                                   'text',
                                                                                                                                   'usually singular '],
                                                                                                                               [
                                                                                                                                   'vis',
                                                                                                                                   [
                                                                                                                                       {
                                                                                                                                           't': "the ship's {it}bottom{/it} [={it}underside{/it}]"},
                                                                                                                                       {
                                                                                                                                           't': 'The bowl was signed on the {it}bottom{/it} [={it}base{/it}] by the artist.'},
                                                                                                                                       {
                                                                                                                                           't': "There's a small cut on the {it}bottom{/it} [={it}sole{/it}] of his foot."}]]]]]]}],
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': 'c',
                                                                                                               'sgram': 'count',
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}the lowest point or surface inside something {bc}the part of something hollow that is furthest from the top'],
                                                                                                                   [
                                                                                                                       'uns',
                                                                                                                       [
                                                                                                                           [
                                                                                                                               [
                                                                                                                                   'text',
                                                                                                                                   'usually singular '],
                                                                                                                               [
                                                                                                                                   'vis',
                                                                                                                                   [
                                                                                                                                       {
                                                                                                                                           't': 'I think there is still a little sugar left in the {it}bottom{/it} of the box/container.'},
                                                                                                                                       {
                                                                                                                                           't': 'The pool is so deep I could not touch the {it}bottom{/it}.'},
                                                                                                                                       {
                                                                                                                                           't': "One of the drawers has a {phrase}false bottom{/phrase}. [=a panel that looks like the drawer's bottom but that can be removed to expose more space]"}]]]]]]}],
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': 'd',
                                                                                                               'sgram': 'singular',
                                                                                                               'sls': [
                                                                                                                   'chiefly British'],
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}the part of something that is furthest away '],
                                                                                                                   [
                                                                                                                       'vis',
                                                                                                                       [
                                                                                                                           {
                                                                                                                               't': 'We sailed to the {it}bottom{/it} of the bay.'},
                                                                                                                           {
                                                                                                                               't': 'the {it}bottom{/it} of the garden'}]]]}]],
                                                                                                   [
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': '2',
                                                                                                               'sgram': 'count',
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}the part of the body on which you sit {bc}{sx|buttocks||} '],
                                                                                                                   [
                                                                                                                       'vis',
                                                                                                                       [
                                                                                                                           {
                                                                                                                               't': 'The poor baby has a rash all over his little {it}bottom{/it}.'}]]]}]],
                                                                                                   [
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': '3 a',
                                                                                                               'sgram': 'singular',
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}a position of little power in a company or organization '],
                                                                                                                   [
                                                                                                                       'vis',
                                                                                                                       [
                                                                                                                           {
                                                                                                                               't': "The company's new CEO started at the {it}bottom{/it} and worked her way up."}]]]}],
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': 'b',
                                                                                                               'sgram': 'singular',
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}a low rank or position '],
                                                                                                                   [
                                                                                                                       'vis',
                                                                                                                       [
                                                                                                                           {
                                                                                                                               't': 'Why do I always find myself rooting for the team at the {it}bottom{/it} of the league?'},
                                                                                                                           {
                                                                                                                               't': 'She graduated {phrase}at the bottom of her/the class{/phrase}. [=her grades were among the lowest in her graduating class]'}]]]}],
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': 'c',
                                                                                                               'sgram': 'noncount',
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}the worst position, level, or condition '],
                                                                                                                   [
                                                                                                                       'vis',
                                                                                                                       [
                                                                                                                           {
                                                                                                                               't': 'at the {it}bottom{/it} of the pay scale'},
                                                                                                                           {
                                                                                                                               't': "After weeks of losing value, the company's stocks have {phrase}hit bottom{/phrase}. [=reached the bottom; lost all value]"},
                                                                                                                           {
                                                                                                                               't': 'Jim has finally {phrase}scraped bottom{/phrase}. [=has finally reached the worst possible condition]'}]],
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{dx}see also {dxt|rock bottom||}{/dx}']]}]],
                                                                                                   [
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': '4 a',
                                                                                                               'sgram': 'singular',
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}the surface that is under a body of water '],
                                                                                                                   [
                                                                                                                       'vis',
                                                                                                                       [
                                                                                                                           {
                                                                                                                               't': 'the {it}bottom{/it} of the ocean'},
                                                                                                                           {
                                                                                                                               't': 'the sandy river/lake {it}bottom{/it}'}]]]}],
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': 'b',
                                                                                                               'bnote': 'bottoms',
                                                                                                               'sgram': 'plural',
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}the flat, low land along a river or stream {bc}{sx|bottomland||} '],
                                                                                                                   [
                                                                                                                       'vis',
                                                                                                                       [
                                                                                                                           {
                                                                                                                               't': 'grazing in grassy river {it}bottoms{/it}'}]]]}]],
                                                                                                   [
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': '5',
                                                                                                               'sgram': 'count',
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}a piece of clothing that is worn on the lower part of the body '],
                                                                                                                   [
                                                                                                                       'vis',
                                                                                                                       [
                                                                                                                           {
                                                                                                                               't': 'a bikini {it}bottom{/it}'}]],
                                                                                                                   [
                                                                                                                       'uns',
                                                                                                                       [
                                                                                                                           [
                                                                                                                               [
                                                                                                                                   'text',
                                                                                                                                   'often plural '],
                                                                                                                               [
                                                                                                                                   'vis',
                                                                                                                                   [
                                                                                                                                       {
                                                                                                                                           't': 'pajama {it}bottoms{/it}'}]]]]],
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '']]}]],
                                                                                                   [
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': '6',
                                                                                                               'sgram': 'singular',
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}the second half of an inning in baseball '],
                                                                                                                   [
                                                                                                                       'vis',
                                                                                                                       [
                                                                                                                           {
                                                                                                                               't': 'They tied the score in the {it}bottom{/it} of the ninth inning.'}]]]}]],
                                                                                                   [
                                                                                                       [
                                                                                                           'sense',
                                                                                                           {
                                                                                                               'sn': '7',
                                                                                                               'sgram': 'noncount',
                                                                                                               'sls': [
                                                                                                                   'chiefly British'],
                                                                                                               'dt': [
                                                                                                                   [
                                                                                                                       'text',
                                                                                                                       '{bc}the lowest gear of a car '],
                                                                                                                   [
                                                                                                                       'vis',
                                                                                                                       [
                                                                                                                           {
                                                                                                                               't': 'Stay in {it}bottom{/it} [={it}bottom gear{/it}] until you reach the top of the hill.'}]]]}]]]}],
      'uros': [{'ure': 'bot*tomed', 'prs': [{'ipa': 'ˈbɑːtəmd', 'sound': {'audio': 'bottom02'}}],
                'fl': 'adjective', 'utxt': [['vis', [{'t': 'flat {it}bottomed{/it} boats'}]]]}],
      'dros': [{'drp': 'at bottom', 'def': [{'sseq': [[['sense', {'sls': ['chiefly British'],
                                                                  'dt': [['text',
                                                                          '{bc}in reality {bc}{sx|really||} '],
                                                                         ['vis', [{
                                                                                      't': 'The song is, {it}at bottom{/it} [={it}in truth{/it}], a lullaby.'},
                                                                                  {
                                                                                      't': 'He is very shy, {it}at bottom{/it}.'}]]]}]]]}]},
               {'drp': 'at the bottom of the pile', 'def': [
                   {'sseq': [[['sense', {'dt': [['text', '{dx}see {dxt|pile:1||}{/dx}']]}]]]}]},
               {'drp': 'be/lie at the bottom of', 'def': [{'sseq': [[['sense',
                                                                      {'sls': ['chiefly British'],
                                                                       'dt': [['text',
                                                                               '{bc}to be the source or originator of (something) '],
                                                                              ['vis', [{
                                                                                           't': "I think I know who's {it}at the bottom of{/it} [={it}behind{/it}] these pranks."}]]]}]]]}]},
               {'drp': 'bottoms up', 'def': [{'sseq': [[['sense', {'sls': ['informal'], 'dt': [
                   ['uns', [[['text', 'used as a toast or to tell people to finish their drinks '],
                             ['vis', [{
                                          't': "Here's to the groom-to-be! {it}Bottoms up{/it}!"}]]]]]]}]]]}]},
               {'drp': 'from the bottom of your heart',
                'def': [{'sseq': [[['sense', {'dt': [['text', '{dx}see {dxt|heart||}{/dx}']]}]]]}]},
               {'drp': 'from top to bottom',
                'def': [{'sseq': [[['sense', {'dt': [['text', '{dx}see {dxt|top:1||}{/dx}']]}]]]}]},
               {'drp': 'get to the bottom of', 'def': [{'sseq': [[['sense', {
                   'dt': [['text', '{bc}to find out the true reason for or cause of (something) '],
                          ['vis', [{
                                       't': 'Police are working furiously to {it}get to the bottom of{/it} this recent string of violent crimes.'}]]]}]]]}]},
               {'drp': 'the bottom drops/falls out', 'def': [{'sseq': [[['sense', {'dt': [['snote',
                                                                                           [['t',
                                                                                             'If {it}the bottom drops/falls out{/it} of something, it suddenly fails or becomes unable to continue in a normal and effective way.'],
                                                                                            ['vis',
                                                                                             [{
                                                                                                  't': 'Analysts warn that recent changes in the region may result in {it}the bottom dropping out{/it} of the oil market. [=may cause the oil market to collapse]'},
                                                                                              {
                                                                                                  't': 'When the accident happened, she felt {it}the bottom drop out{/it} of her world. [=she felt her world collapse]'}]]]]]}]]]}]},
               {'drp': 'the bottom of the barrel', 'def': [{'sseq': [[['sense', {
                   'dt': [['text', '{bc}the lowest possible condition, level, etc. '], ['vis', [{
                                                                                                    't': 'After the divorce, Tim felt he had reached/hit {it}the bottom of the barrel{/it}.'},
                                                                                                {
                                                                                                    't': 'The excessive coverage of the scandal signals that the news media may have finally hit/reached {it}the bottom of the barrel{/it}.'},
                                                                                                {
                                                                                                    't': 'Salaries in the industry are scraping/hitting {it}the bottom of the barrel{/it}. [=salaries in the industry are very low]'}]]]}]]]}]}],
      'shortdef': ['the lowest part, point, or level of something—usually singular',
                   'the part of something that is below or under the other parts—usually singular',
                   'the lowest point or surface inside something : the part of something hollow that is furthest from the top—usually singular']},
     {'meta': {'id': 'bottom:2', 'uuid': '1bfbcfa2-9573-4290-82b4-bfb0e4c9b3b4', 'src': 'learners',
               'section': 'alpha',
               'target': {'tuuid': 'a5037e1d-996f-45cd-bc0e-e45cfc1b3327', 'tsrc': 'collegiate'},
               'highlight': 'yes', 'stems': ['bottom', 'bet your bottom dollar'],
               'app-shortdef': {'hw': 'bottom:2', 'fl': 'adjective',
                                'def': ['{bc} in the lowest position',
                                        '{bc} living at the lowest level of an ocean or lake']},
               'offensive': False}, 'hom': 2,
      'hwi': {'hw': 'bottom', 'altprs': [{'ipa': 'ˈbɑːtəm'}]}, 'fl': 'adjective',
      'lbs': ['always used before a noun'], 'def': [{'sseq': [[['sense', {'sn': '1', 'dt': [
         ['text', '{bc}in the lowest position '], ['vis',
                                                   [{'t': 'the {it}bottom{/it} rung of the ladder'},
                                                    {'t': 'the {it}bottom{/it} drawer/shelf'},
                                                    {'t': 'her {it}bottom{/it} lip'}, {
                                                        't': "Somebody's fingerprints are all along the {it}bottom{/it} edge of the photograph."}]],
         ['text', '{dx}see also {dxt|bottom line||}{/dx}']]}]], [['sense', {'sn': '2', 'dt': [
         ['text', '{bc}living at the lowest level of an ocean or lake '],
         ['vis', [{'t': '{it}bottom{/it} fish'}]]]}]]]}], 'dros': [{'drp': 'bet your bottom dollar',
                                                                    'def': [{'sseq': [[['sense', {
                                                                        'dt': [['text',
                                                                                '{dx}see {dxt|bet:2||}{/dx}']]}]]]}]}],
      'shortdef': ['in the lowest position', 'living at the lowest level of an ocean or lake']}, {
         'meta': {'id': 'bottom:3', 'uuid': 'd09ef23e-af37-49f7-a060-8392c18e6915',
                  'src': 'learners', 'section': 'alpha',
                  'target': {'tuuid': '77d4c126-45ba-4e38-aa59-3a14f9f7a1df', 'tsrc': 'collegiate'},
                  'stems': ['bottom', 'bottomed', 'bottomer', 'bottomers', 'bottoming', 'bottoms',
                            'bottom out'], 'app-shortdef': {'hw': 'bottom:3', 'fl': 'verb', 'def': [
                 '{bc} to reach a lowest or worst point usually before beginning to rise or improve']},
                  'offensive': False}, 'hom': 3,
         'hwi': {'hw': 'bottom', 'altprs': [{'ipa': 'ˈbɑːtəm'}]}, 'fl': 'verb',
         'ins': [{'ifc': '-toms', 'if': 'bottoms'}, {'ifc': '-tomed', 'if': 'bottomed'},
                 {'ifc': '-tom*ing', 'if': 'bottom*ing'}], 'dros': [
            {'drp': 'bottom out', 'gram': 'phrasal verb', 'def': [{'sseq': [[['sense', {'dt': [
                ['text',
                 '{bc}to reach a lowest or worst point usually before beginning to rise or improve '],
                ['vis', [{
                             't': 'Real estate prices seem to have {it}bottomed out{/it}, and sellers can expect to get higher prices in coming months.'},
                         {'t': 'The team {it}bottomed out{/it} in last place.'}]]]}]]]}]}],
         'shortdef': []}, {
         'meta': {'id': 'bottom drawer', 'uuid': '8e1dddc7-76ab-4fd4-a7ff-5c048eb3af00',
                  'src': 'learners', 'section': 'alpha',
                  'stems': ['bottom drawer', 'bottom drawers'],
                  'app-shortdef': {'hw': 'bottom drawer', 'fl': 'noun',
                                   'def': ['{it}British{/it}']}, 'offensive': False},
         'hwi': {'hw': 'bottom drawer'}, 'fl': 'noun',
         'ins': [{'il': 'plural', 'ifc': '~ -ers', 'if': 'bottom drawers'}], 'gram': 'count',
         'def': [{'sseq': [[['sense', {'sls': ['British'], 'dt': [
             ['text', '{bc}{sx|hope chest|vis', [{'t': '{it}bottom-up{/it} management'}]],
             ['text', '{dx}opposite {dxt|top-down||}{/dx}']]}]]]}], 'shortdef': [
            'progressing upward from the lowest levels : controlled or directed from the lower levels']},
     {'meta': {'id': 'Foggy Bottom', 'uuid': 'd0a7143d-7463-4302-8100-4e762e3137be',
               'src': 'learners', 'section': 'alpha',
               'target': {'tuuid': 'a0c6d050-e164-4fce-9b2a-977f7f1278b1', 'tsrc': 'collegiate'},
               'stems': ['foggy bottom', 'foggy bottoms'],
               'app-shortdef': {'hw': 'Foggy Bottom', 'fl': 'noun',
                                'def': ['{it}informal{/it} {bc} the U.S. Department of State']},
               'offensive': False}, 'hwi': {'hw': 'Foggy Bottom'}, 'fl': 'noun', 'gram': 'singular',
      'def': [{'sseq': [[['sense', {'sls': ['informal'],
                                    'dt': [['text', '{bc}the U.S. Department of State']]}]]]}],
      'shortdef': ['the U.S. Department of State']}, {
         'meta': {'id': 'rock bottom', 'uuid': '0ace6e1a-3f7a-4c5a-b06f-574c8bba8209',
                  'src': 'learners', 'section': 'alpha',
                  'target': {'tuuid': 'ba915990-67aa-4990-b949-03f29ffd088e', 'tsrc': 'collegiate'},
                  'stems': ['rock bottom', 'rock bottoms', 'hit/reached rock bottom',
                            'hit rock bottom', 'reached rock bottom'],
                  'app-shortdef': {'hw': 'rock bottom', 'fl': 'noun',
                                   'def': ['{bc} the lowest possible level or point']},
                  'offensive': False}, 'hwi': {'hw': 'rock bottom'}, 'fl': 'noun',
         'gram': 'noncount', 'def': [{'sseq': [[['sense', {
            'dt': [['text', '{bc}the lowest possible level or point '], ['vis', [{
                                                                                     't': 'Prices have {phrase}hit/reached rock bottom{/phrase}. [=have reached the lowest point they can reach]'},
                                                                                 {
                                                                                     't': 'After years of heavy drug use, she has finally {it}reached rock bottom{/it}.'},
                                                                                 {
                                                                                     't': 'Their marriage has {it}hit rock bottom{/it}.'}]]]}]]]}],
         'shortdef': ['the lowest possible level or point']}]
