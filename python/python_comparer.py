"""
@author: maddieskopicki
"""
import math

class TextModel():
    """blueprint for objects that model a body of text"""
    
    def __init__(self, model_name):
        """constructs a new TextModel object by accepting a string model_name 
        as a parameter and initializing the proper attributes"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}
        
    def __repr__(self):
        """returns a string that includes the name of the model as well as the 
        sizes of the dictionaries for each feature of the text"""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of various punctuational endings: ' + str(len(self.punctuation)) 
        return s      
        
    def add_string(self, s):
        """adds a string of text s to the model by augmenting the feature 
        dictionaries defined in the constructor."""
        count = 0
        sentence_endings = '.!?'
        for char in s:
            if char == ' ':
                count += 1
            elif char in sentence_endings:
                if count >= 0:
                    sen_length = count + 1
                    if sen_length in self.sentence_lengths:
                        self.sentence_lengths[sen_length] += 1
                    else:
                        self.sentence_lengths[sen_length] = 1
                count = -1
        if count > 0:
            sen_length = count + 1
            if sen_length in self.sentence_lengths:
                self.sentence_lengths[sen_length] += 1
            else:
                self.sentence_lengths[sen_length] = 1
        
        for punc in s:
            if punc in sentence_endings:
                if punc in self.punctuation:
                    self.punctuation[punc] += 1
                else:
                    self.punctuation[punc] = 1
        word_list = clean_text(s)
        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
            length = len(w)
            if length in self.word_lengths:
                self.word_lengths[length] += 1
            else:
                self.word_lengths[length] = 1
            stems = stem(w)
            if stems in self.stems:
                self.stems[stems] += 1
            else:
                self.stems[stems] = 1
    
    def add_file(self, filename):
        """adds all of the text in the file identified by filename 
        to the model"""
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        file = f.read()
        self.add_string(file)
        f.close()
        
    def save_model(self):
        """saves the TextModel object self by writing its various feature 
        dictionaries to files"""
        f1 = open(self.name + '_' + 'words', 'w')
        f1.write(str(self.words))
        f1.close()
        
        f2 = open(self.name + '_' + 'word_lengths', 'w')
        f2.write(str(self.word_lengths))
        f2.close()
        
        f3 = open(self.name + '_' + 'stems', 'w')
        f3.write(str(self.stems))
        f3.close()
        
        f4 = open(self.name + '_' + 'sentence_lengths', 'w')
        f4.write(str(self.sentence_lengths))
        f4.close()
        
        f5 = open(self.name + '_' + 'punctuations', 'w')
        f5.write(str(self.punctuation))
        f5.close()
        
        
    def read_model(self):
        """reads the stored dictionaries for the called TextModel object from 
        their files and assigns them to the attributes of the called TextModel"""
        words = open(self.name + '_words', 'r')
        word_str = words.read()
        words.close()
        readmodel_word = dict(eval(word_str))
        self.words = readmodel_word
        
        lengths = open(self.name + '_word_lengths', 'r')
        length_str = lengths.read()
        lengths.close()
        readmodel_length = dict(eval(length_str))
        self.word_lengths = readmodel_length
        
        stems = open(self.name + '_stems', 'r')
        stems_str = stems.read()
        stems.close()
        readmodel_stem = dict(eval(stems_str))
        self.stems = readmodel_stem
        
        sen_lengths = open(self.name + '_sentence_lengths', 'r')
        sen_length_str = sen_lengths.read()
        sen_lengths.close()
        readmodel_sen_length = dict(eval(sen_length_str))
        self.sentence_lengths = readmodel_sen_length
        
        puncs = open(self.name + '_punctuations', 'r')
        punc_str = puncs.read()
        puncs.close()
        readmodel_punc = dict(eval(punc_str))
        self.punctuation = readmodel_punc
        
    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores measuring the 
        similarity of self and other – one score for each type of feature ."""
        log_score = []
    
        word_score = compare_dictionaries(other.words, self.words)
        log_score += [word_score]
        
        word_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        log_score += [word_length_score]
        
        stems_score = compare_dictionaries(other.stems, self.stems)
        log_score += [stems_score]
        
        sentence_length_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        log_score += [sentence_length_score]
        
        punctuation_score = compare_dictionaries(other.punctuation, self.punctuation)
        log_score += [punctuation_score]
        
        return log_score
    
    def classify(self, source1, source2):
        """compares the called TextModel object (self) to two other “source” 
        TextModel objects (source1 and source2) and determines which of these 
        other TextModels is the more likely source of the called TextModel"""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for', source1.name, ':', scores1)
        print('scores for', source2.name, ':', scores2)
        more_source1 = 0
        more_source2 = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                more_source1 += 1
            else:
                more_source2  += 1
        if more_source1 > more_source2:
            print(self.name, 'is more likely to have come from', source1.name)
        else:
            print(self.name, 'is more likely to have come from', source2.name)
            
def clean_text(txt):
    """takes a string of text txt as a parameter and returns a list 
    containing the words in txt after it has been “cleaned”."""
    txtval = txt
    txtval = txtval.lower()
    for symbol in """.,?"'!;:""":
        txtval = txtval.replace(symbol, '')
    txtval = txtval.split()
    return txtval

def stem(s):
    """accepts a string as a parameter and returns the stem of s"""
    if s[-1:] == 's':
        s = s[:-1]
    if s[-1:] == 'ful':
        s = s[:-3]
    if s[-2:] == 'ly':
        s = s[:-2]
    if s[-3:] == 'ing':
        if len(s) > 5:
            if s[-4] == s[-5]:
                s = s[:-4]
        s = s[:-3]
    if s[-3:] == 'ies':
        s = s[:-2]
    if s[-3:] == 'ish':
        if len(s) > 4:
            if s[-4] == s[-5]:
                s = s[:-4]
            else:
                s = s[:-3]
    if s[-2:] == 'ed':
        s = s[:-2]
    return s

def compare_dictionaries(d1, d2):
    """takes two feature dictionaries d1 and d2 as inputs, and computes and 
    returns their log similarity score"""
    score = 0
    total = 0
    for word in d1:
        total += d1[word]
    for word in d2:
        if word in d1:
            score += (math.log(d1[word] / total) * d2[word])
        else:
            score += (math.log(0.5 / total) * d2[word])
    return score
            
def run_tests():
    """obtains text for textmodeling and comparrison to other forms. Utilizes 
    two ficticious forms (Epics and Fairytales) to compare the works of Homer 
    and Hans Christian Andersen"""
    source1 = TextModel('Homer')
    source1.add_file('homer_o.txt')

    source2 = TextModel('Andersen')
    source2.add_file('hca.txt')

    new1 = TextModel('Romeo and Juliet')
    new1.add_file('raj.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel('Grimms Tales')
    new2.add_file('grim.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('Frankenstein')
    new3.add_file('frank.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('The Iliad')
    new4.add_file('homer_i.txt')
    new4.classify(source1, source2)
    
    
    
    
                
                
                
                
                
                
                
