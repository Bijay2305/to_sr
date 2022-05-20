import string
import re
import config
import spacy
from itertools import islice
from spacy.matcher import PhraseMatcher
import re
import difflib
from difflib import SequenceMatcher
PUNCT_TO_REMOVE = string.punctuation
path = "./en_core_web_sm-3.0.0"
nlp = spacy.load(path)
all_stop_words =nlp.Defaults.stop_words
def remove_extraspace(text):
    space_pattern =r'\s+'
    space_pattern = r'\s+'
    text=re.sub(pattern=space_pattern,repl=" ",string=text)
    return text
def remove_extraspace(text):
    space_pattern =r'\s+'
    space_pattern = r'\s+'
    text=re.sub(pattern=space_pattern,repl=" ",string=text)
    return text
def text_clean(text):
    try :
        #removing non asci charecters
        text =re.sub(r'[^\x00-\x7F]+', ' ', text)
        #text=re.sub('[^A-Za-z0-9]+', '', text)
        #lower case
        text = text.lower()
        #Removing Extra SPace
        text = remove_extraspace(text)
        return text
    except Exception as e:
        print(e)
def convertTuple(tup):
    st = ' '.join(map(str, tup))
    return st
def sentence_comparison(csv_text,ref):
    try:
        input_list = text_clean(csv_text).split()
        print(input_list)
        phrases = list(window(input_list))
        patterns = [nlp(text) for text in phrases]
        print(patterns)
        sentence = nlp(text2int(text_clean(ref)))
        print(sentence)
        phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        print(phrase_matcher)
        phrase_matcher.add("VG", None, *patterns)
        matched_phrases = phrase_matcher(sentence)
        for match_id, start, end in matched_phrases:
            if start - config.prev_start > config.input_difference:
                config.actual_start = start
                config.actual_end = 0
            else:
                config.actual_end = end
            config.prev_start = start
            print("Start :" + str(config.actual_start))
            print("End :" + str(config.actual_end))
        extracted = sentence[config.actual_start:config.actual_end]
        print(str(extracted).split())
        score = SequenceMatcher(None, input_list, str(extracted).split()).ratio()
        output_dict = {"incoming_string": csv_text,
                       "TEXT_COMPARED": extracted,
                       "CONFIDENCE_SCORE": int(score*100)}
        print(output_dict)
        return output_dict
    except Exception as e:
        print(e)
def text2int(textnum, numwords={}):
    if not numwords:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        scales = ["hundred", "thousand", "million", "billion", "trillion"]
        # numwords["and"] = (1, 0)
        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)
    ordinal_words = {'first': 1, 'second': 2, 'third': 3, 'fifth': 5, 'eighth': 8, 'ninth': 9, 'twelfth': 12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]
    textnum = textnum.replace('-', ' ')
    current = result = 0
    curstring = ""
    onnumber = False
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)
            if word not in numwords:
                if onnumber:
                    curstring += repr(result + current) + " "
                if word == 'point':
                    if (curstring.split().pop(-1)).isnumeric():
                        curstring = curstring.strip() + "."
                        result = current = 0
                        onnumber = False
                else:
                    curstring += word + " "
                    result = current = 0
                    onnumber = False
            else:
                scale, increment = numwords[word]
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
    if onnumber:
        curstring += repr(result + current)
    return curstring
def window(incoming_text, n=4):
    it = iter(incoming_text)
    result = list(islice(it, n))
    if len(result) == n:
        yield " ".join(result)
    for elem in it:
        result = result[1:] + [elem,]
        yield " ".join(result)
