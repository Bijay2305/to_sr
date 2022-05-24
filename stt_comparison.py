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
def expanded_words(phrase):
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase
def remove_extraspace(text):
    space_pattern =r'\s+'
    space_pattern = r'\s+'
    text=re.sub(pattern=space_pattern,repl=" ",string=text)
    return text


def text_clean(text):
    try:
        # removing non asci charecters
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        # text=re.sub('[^A-Za-z0-9]+', '', text)
        text = text.replace(",", "").replace('. ', ' ').replace('?', '')

        # lower case
        text = text.lower()

        # text = re.sub(r'(\b[a-z])\.(?=[a-z]\b|\s|$)', r'\1', text)

        # Removing Extra SPace
        text = remove_extraspace(text)
        return text
    except Exception as e:
        print(e)
    except Exception as e:
        print(e)

def sentence_comparison(cvp_text,ref):
    try:
        input_list = text_clean(cvp_text).split()
        print("cleaned_input_list", input_list)
        print("******")
        phrases = list(window(input_list))
        print("4 word window phrases",phrases)
        patterns = [nlp(text) for text in phrases]
        #print(patterns)
        print("uncleaned texts***\n",ref)
        sentence = nlp(text2int(expanded_words(text_clean(ref))))
        #sentence = nlp(text2int(text_clean(ref)))
        print("stt_sentence****\n",sentence)
        phrase_matcher=PhraseMatcher(nlp.vocab, attr="LOWER")
        phrase_matcher.add("VG", None, *patterns)
        matched_phrases = phrase_matcher(sentence)
        extracted = extract_phrase_match(matched_phrases,sentence)
        print("extracted",extracted)
        score = SequenceMatcher(None, input_list, str(extracted).split()).ratio()
        score = (round(score,2))*100
        compare_words(input_list,extracted)
        confidence_rate = confidence_rating(score)
        print(cvp_text)
        output_dict = {"cvp_text": str(cvp_text),
                       "stt_text": str(extracted),
                       "confidence_score": score,
                       "confidence_rate" : confidence_rate}

        return output_dict
    except Exception as e:
        print(e)
#converting text to int values
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
    ordinal_endings = [('ieth', 'y')]  # , ('th', '')]

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
                elif word == 'percent' or word == 'percentage':
                    if curstring.split().pop(-1).replace('.', '', 1).isdigit():
                        curstring = curstring.strip() + "% "
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
def confidence_rating (confidence_score):
    if confidence_score >= config.confidence_score_read:
        return "Read"
    elif ((confidence_score < config.confidence_score_read) & (confidence_score >= config.confidence_score_inter)):
        return "Indeterminate"
    else:
        return "Not Read"
def extract_phrase_match(matched_phrases,sentence):
    for match_id, start, end in matched_phrases:

        if start - config.prev_end > config.input_difference:

            if config.match_count > config.prev_match_count:
                config.prev_match_count = config.match_count

                config.max_text_loc = str(config.actual_start) + ":" + str(config.actual_end) + ":" + str(config.match_count)

            config.actual_start = start
            config.actual_end = 0
            config.match_count = 0
        else:
            config.match_count = config.match_count + 1
            config.actual_end = end

        config.prev_start = start
        config.prev_end = end

        print("Match Count :" + str(config.match_count))
        print("Start :" + str(config.actual_start))
        print("End :" + str(config.actual_end))

    if config.max_text_loc == "":
        config.max_text_loc = str(config.actual_start) + ":" + str(config.actual_end) + ":" + str(config.match_count)

    print(config.max_text_loc)
    final_index = list(map(int, config.max_text_loc.split(":")))
    extracted = sentence[final_index[0]:final_index[1]]
    print(extracted)
    return extracted
def compare_words(input_list,extracted):
    d = difflib.Differ()
    diff = d.compare(input_list, str(extracted).split())
    print('\n'.join(diff))
