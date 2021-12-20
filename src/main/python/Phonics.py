"""import com.google.gson.Gson;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.ResponseBody;

import java.io.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.*;
"""
import json as js
import time
import re
import mysql.connector
import configparser
import requests
import DictionaryApiLookup as dapi

"""private final Gson gson;
private final String learner_key;
private final String uni_key;
private final String rankCsv;
private final String phonemeCsv;
private OkHttpClient client;
private final String server;
private final String password;
private final Properties prop;
private final String schema;
private final String username;
private static Connection conn;
private long totalIpaTime;
private long ipaTime;
private long syllableTime;
private long totalSyllableTime;"""


class Phonics:
    def __init__(self, phonetic_map_csv, common_words, ini='config.ini'):
        self.ipa = None
        self.totalIpa_time = 0
        self.ipa_time = 0
        self.syllable_time = 0
        self.total_syllable_time = 0
        self.rankCsv = phonetic_map_csv
        self.phonemeCsv = common_words

        config = configparser.ConfigParser()
        config.read(ini)
        server = config['database.local']['server']
        database = config['database.local']['database']
        user_ = config['database.local']['user']
        password_ = config['database.local']['password']
        self.learner_key = config['dictionary.com']['learners_key']
        self.uni_key = config['dictionary.com']['uni_key']

        self.conn = mysql.connector.connect(
            host=server,
            user=user_,
            password=password_
        )
        self.conn.database = database
        print(f'connected to {user_}@{server}/{database}')
        self.conn.cursor().execute('use syllables')


    def get_ipa_spelling(self, w):
        start = time.time()
        w = w.tolower()
        api_url = f"https://www.dictionaryapi.com/api/v3/references/learners" \
                  f"/json/{w}?key={self.learner_key}"
        ipa = ""
        out = ""
        small_start = time.time()
        req = requests.get(api_url)
        try:
            word_json = js.loads(req.content)
            self.ipa_time += (time.time() - small_start)
            ipa = word_json["ipa"]
            if not ipa.startswith("\\u"):
                if "\\u" in ipa:
                    return None
                out += ipa.substring(0, ipa.indexOf("\\u"))
                ipa = ipa.substring(ipa.indexOf("\\u"))
            split = ipa.split("\\\\u")
            if split[0].equals(""):
                split_temp = [split[i + 1] for i in range(len(split))]
            for chunk in split:
                subs = chunk[0:4]
                out += f'{chr(int(subs))}'
                if len(chunk) > 4:
                    out += chunk[4:]
        except:
            Exception("IDK what happened...")
        self.total_ipa_time += time.thread_time_ns() - start
        return out


    def get_syllable_spelling(self, w):
        start = time.time_ns()
        w = w.tolower()
        api_url = f"https://www.dictionaryapi.com/api/v3/references/collegiate" \
                  f"/json/{w}?key={self.uni_key}"
        req = requests.get(api_url)
        interval_start = time.time_ns()
        try:
            word_json = js.loads(req.content)
            self.ipa_time += (time.time() - interval_start)
            ipa = word_json["ipa"]
            self.syllable_time += time.time_ns() - interval_start
            ss = ipa["hwi"]
            self.total_syllable_time += time.time_ns() - start
            return ss.substring(5, ss.indexOf(",") - 1)
        except:
            Exception()
        self.total_syllable_time += time.time_ns() - start


    def insert_words(self, pathname):
        self.conn.prepared = True
        self.conn.autocommit = False
        # create PreparedStatements and indexes for them
        inserts = [
            "INSERT INTO words(word) VALUES (:1)",
            "INSERT INTO ranks(word, rank_) VALUES (:1, :2)",
            "INSERT INTO frequencies(word, frequency) VALUES (:1, :2)",
            "INSERT IGNORE INTO syllables(word, syllable) VALUES (:1, :2)",
            "INSERT IGNORE INTO phonemes(word, phoneme) VALUES (:1, :2)"
        ]
        insertion_tuples = {
            'words': [],
            'ranks': [],
            'frequencies': [],
            'syllables': [],
            'phonemes': []
        }

        for counter, line_ in enumerate(open(pathname).readlines()):
            rank, word, frequency = line_.split(",")
            ipa_spelling = self.get_ipa_spelling(word)
            # don't process this word if there is an issue with the dictionary's api
            if not ipa_spelling:
                print(f"remove entry {counter} for {word}, no valid ipa")
                continue
            # put all the fields in their places for all statements
            if counter > 0 and counter % 500 == 0:
                for outer_list in insertion_tuples:
                    outer_list += [[]]
            insertion_tuples['words'][-1].append((word,))
            insertion_tuples['ranks'][-1].append((word, rank))
            insertion_tuples['frequencies'][-1].append((word, frequency))
            insertion_tuples['syllables'][-1].append((word, self.get_syllable_spelling(word)))
            insertion_tuples['phonemes'][-1].append((word, self.get_ipa_spelling(word)))
            cursor = self.conn.cursor()
            for sql_insert_query, batch_tuples in zip(inserts, insertion_tuples):
                for batch_tuple in batch_tuples:
                    cursor.executemany(sql_insert_query, batch_tuple)

        for insert in inserts:
            insert.executeBatch()
        self.conn.commit()
        self.conn.autocommit = True
        print(f"ipa request time: {self.ipa_time}"
              f"\ntotal ipa process time: {self.ipa_time}"
              f"\nsyllable request time: {self.totalIpa_time}"
              f"\ntotal syllable process time: {self.total_syllable_time}"
        )


    def close(self):
        self.conn.close()


    def create_ipa_map_table(self, pathname):
        self.conn.autocommit = False
        lines = [i.split() for i in open(pathname).readlines()]
        lines = [(int(a[0]), a[1], int(a[2])) for a in lines]
        cursor = self.conn.cursor()
        sql_string = 'INSERT IGNORE INTO phonetic_map (word, phonetic_spelling) VALUES (:1, :2)'
        cursor.executemany(sql_string, lines)
        print(f"processed {len(lines)} lookups")


def main():
    phonics = Phonics()
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    # server = config['database.local']['server']
    # database = config['database.local']['database']
    # user_ = config['database.local']['user']
    # password_ = config['database.local']['password']
    #
    # conn = mysql.connector.connect(
    #     host=server,
    #     user=user_,
    #     password=password_
    # )
    #
    # phone = Phonics("C:/Users/Galacticwafer/IdeaProjects/5000MostCommonWordsRank.csv",
    #                 "5000MostCommonWordsPhonemes.csv")
    # cursor = conn.cursor
    # conn.autocommit = False
    #
    # pathname = "C:/ProgramData/MySQL/MySQL Server 8.0/Data/5000MostCommonWordsRank3.csv"
    # phone.insert_words(pathname)
    # words_sql = 'INSERT INTO words(word) VALUES (:1)'
    # ranks_sql = 'INSERT INTO ranks(word, rank_) VALUES (' + ')'
    # frequencies_sql = 'INSERT INTO frequencies(word, frequency) VALUES (:1, :2)'
    # words_syllables_sql = 'INSERT INTO words_syllables(worFd, syllable, position) VALUES (:1, :2, ' \
    #                      ':3)'
    # wordsPhonemes_sql = 'INSERT INTO words_phonemes(word, phoneme, position) VALUES (:1, :2, :3)'
    # words = ranks = frequencies = words_syllables = wordsPhonemes = []
    # word_count = wordSyllableCount = wordPhonemeCount = 0
    #
    # word_list = open(pathname).readlines()
    #
    # for word_count, line in enumerate(word_list):
    #     rank, word, frequency = line.split(",")
    #     words.append((word,))
    #     ranks.append((word, rank))
    #     frequencies.append((word, frequency))
    #     syllables = phone.get_syllable_spelling(word)
    #     phonemes = phone.get_ipa_spelling(word)
    #     # wordSyllableCount = getCount(words_syllables, wordCount, wordSyllableCount, word,
    #     # syllables, syllables.length)
    #     # wordPhonemeCount = getCount(wordsPhonemes, wordCount, wordPhonemeCount, word,
    #     # syllables, phonemes.length());
    #     if word_count % 500 == 0:
    #         words.executeBatch()
    #         # //ranks.executeBatch()
    #         # //frequencies.executeBatch()
    #         print(word_count)
    # words.executeBatch()
    # conn.commit()
    # conn.autocommit = True
    # phone.close()


if __name__ == '__main__()':
    main()