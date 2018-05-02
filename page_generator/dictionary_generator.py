import os
import re
import json
import random
import time
import gzip

from loremipsum import Generator

class TextGen:
    sentences = None
    dictionary = None

    @classmethod
    def get_generator(cls):
        if cls.sentences is None:
            word_path = TextGen.get_data_file_path("wordlist.txt.gz")
            with gzip.open(word_path, "rt", encoding="utf-8") as fin:
                cls.sentences = fin.readlines()

        if cls.dictionary is None:
            json_path = TextGen.get_data_file_path("worddict.json.gz")
            with gzip.open(json_path, "rt", encoding="utf-8") as fjson:
                cls.dictionary = json.load(fjson)

        sample = random.randint(0, len(cls.sentences) - 1)
        sentence = cls.sentences[sample]

        generator = Generator(sentence, cls.dictionary)

        return generator
    
    @staticmethod
    def get_data_file_path(filename) :
        data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
        return os.path.join(data_dir, filename)

    @staticmethod
    def clean_word_list():
        with open("webdump.txt", "r", encoding="utf-8") as fin:
            words = fin.read()

        with gzip.open("wordlist.txt.gz", "wt", encoding="utf-8") as fout:
            sentencelist = words.split(".")
            for sentence in sentencelist:
                sentence = sentence.replace(".", "")
                sentence = sentence.replace(",", "")
                parts = sentence.split(" ")
                if len(set(parts)) < 20 or len(parts) > 40:
                    continue

                fout.write(sentence + "\n")

        with gzip.open("worddict.json.gz", "wt", encoding="utf-8") as fout:
            wordlist = [w.replace(".", "").replace(",", "")
                        for w in words.split(' ')]
            dictionary = sorted(list(set(wordlist)))
            json.dump(dictionary, fout)

    @staticmethod
    def read_text():
        allwords = []
        nononalpha = re.compile(r"[\W\d]+")
        lowercase = re.compile(r"[a-z]+")
        filelist = os.listdir('papers')
        counter = 0

        for filename in filelist:
            counter += 1
            if counter % 50 == 0:
                print("Processed {} of {}".format(counter, len(filelist)))

            if not filename.endswith('.txt'):
                continue

            with open("papers/" + filename, "r", encoding="utf-8") as fin:
                words = fin.read()

            words = words.replace("\n", " ")
            words = re.sub(' +', ' ', words)
            word_list = []
            #words = [w for w in words.split(' ') if len(w) > 2]
            for word in words.split(' '):
                if re.search(nononalpha, word):
                    word_test = word.replace(".", "").replace(",", "")
                    if re.search(nononalpha, word_test):
                        continue

                if not re.search(lowercase, word):
                    continue

                word_list.append(word.lower())

            allwords.extend(word_list)

        with open("webdump.txt", "w", encoding="utf-8") as fout:
            fout.write(" ".join(allwords))

    @staticmethod
    def randomize_list():
        with gzip.open("wordlist.txt.gz", "rt", encoding="utf-8") as fin:
            sentences = fin.readlines()
            random.shuffle(sentences)

        with gzip.open("wordlist.txt.gz", "wt", encoding="utf-8") as fout:
            fout.write(sentences)


def test():
    start_time = time.time()

    generator = TextGen.get_generator()

    load_time = time.time()

    paragraphs = []

    for _ in range(10):
        paragraphs.append(generator.generate_paragraph()[2])

    finish_time = time.time()

    for text in paragraphs:
        print(text)

    print(
        "Generator created in {:.2f} seconds, average time to generate a " \
        "paragraph: {:.2f} seconds".format(
            load_time - start_time, finish_time - load_time))


if __name__ == '__main__':
    test()
