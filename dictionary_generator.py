import os
import re
import json
from loremipsum import Generator
import random
import time

class TextGen :
    sentences = None
    dictionary = None
    
    @classmethod
    def getGenerator(cls) :
        if cls.sentences is None :
            with open("wordlist.txt", "r",encoding="utf-8") as fin :
                cls.sentences = fin.readlines()
         
        if cls.dictionary is None:   
            with open("worddict.json", "r",encoding="utf-8") as fjson : 
                cls.dictionary = json.load(fjson)

        sample = random.randint(0, len(cls.sentences) - 1) 
        sentence = cls.sentences[sample]
           
        generator = Generator(sentence, cls.dictionary)      
        
        return generator
    
    @staticmethod
    def cleanWordList() : 
        with open("wordlist1.txt", "r",encoding="utf-8") as fin :
            words = fin.read()   
        
        with open("wordlist.txt", "w",encoding="utf-8") as fout :    
            sentencelist = words.split(".")
            for sentence in sentencelist :
                sentence = sentence.replace(".","")
                sentence = sentence.replace(",","")   
                parts = sentence.split(" ")
                if len(set(parts)) < 20 or len(parts) > 40:
                    continue
                
                fout.write(sentence + "\n")
                
        with open("worddict.json", "w",encoding="utf-8") as fout : 
            wordlist = [w.replace(".","").replace(",","") for w in words.split(' ')]
            dictionary = sorted(list(set(wordlist)))
            json.dump(dictionary, fout)

        
    @staticmethod
    def readText() :
        allwords = []
        nononalpha = re.compile("[\W\d]+")
        lowercase = re.compile("[a-z]+")
        filelist = os.listdir('papers')
        counter = 0
        
        for f in filelist :
            counter += 1
            if counter % 50 == 0 :
                print("Processed {} of {}".format(counter, len(filelist)))
                
            if not f.endswith('.txt' ):
                continue
        
            with open("papers/" + f, "r", encoding="utf-8") as fin :
                words = fin.read()
                
            words = words.replace("\n"," ")
            
            
            # words = re.sub('\W+',' ', words)
            words = re.sub(' +',' ', words)
            words2 = []
            #words = [w for w in words.split(' ') if len(w) > 2]
            for w in words.split(' ') :
                if re.search(nononalpha, w) :
                    w2 = w.replace(".","")
                    w2 = w2.replace(",","")  
                    if re.search(nononalpha, w2) :
                        continue
                
                if not re.search(lowercase, w) :
                    continue                
                
                words2.append(w.lower())
            
            allwords.extend(words2)
          
        with open("wordlist1.txt", "w", encoding="utf-8") as fout :
            fout.write(" ".join(allwords))
        


if __name__ == '__main__' :
    #TextGen.readText()
    
    TextGen.cleanWordList()
    
    start = time.time()
    
    g = TextGen.getGenerator()
    
    load = time.time()
    
    p1 = g.generate_paragraph()[2]
    p2 = g.generate_paragraph()[2]
    p3 = g.generate_paragraph()[2]
    
    para = time.time()
    
    print(p1)
    print(p2)
    print(p3)
    
    print("Generator in %.3f and 3 paragraphs in %.3f" % (load - start, para - load))