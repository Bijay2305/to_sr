from flask import Flask, redirect, request
import asyncio
from flask import jsonify
from stt_comparison import *
import json
from OpenSSL import SSL
import spacy
from spacy.matcher import PhraseMatcher
import asyncio
def loadmodel():
    path = "./en_core_web_sm-3.0.0"
    print("loading the model\n")
    #global nlp
    nlp = spacy.load(path)
    return nlp

#context = SSL.Context(SSL.SSLv23_METHOD)
#context = ('/opt/epaas/certs/cert', '/opt/epaas/certs/key')

vg = Flask(__name__)

@vg.route('/')
def health_check():
    return "Health Check : [Successful] [OK]"

@vg.route('/comparison', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        string_val = request.json
        print(string_val)
        #uuid = request.json.get.(string_val["uuid"])

        uuid= string_val["callId"]
        cvp_text=string_val['textToValidate']
        stt_text=string_val['spokenText']

        input_list = text_clean(cvp_text).split()
        phrases = list(window(input_list))
        """asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        nlp =loop.run_until_complete(loadmodel())"""
        nlp = loadmodel()
        patterns = [nlp(text) for text in phrases]
        sentence = nlp(text2int(expanded_words(text_clean(stt_text))))
        phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        phrase_matcher.add("VG", None, *patterns)
        matched_phrases = phrase_matcher(sentence)
        extracted = extract_phrase_match(matched_phrases, sentence)
        score = SequenceMatcher(None, input_list, str(extracted).split()).ratio()
        score = (round(score, 2)) * 100
        compare_words(input_list, extracted)
        confidence_rate = confidence_rating(score)
        output = {"validatedText": str(cvp_text),
                       "spokenText": str(extracted),
                       "confidenceScore": score,
                       "confidenceRate": confidence_rate,
                       "callId": uuid}
        print(output)
        return jsonify(output)

    else:
        return 'Content-Type not supported!'
@vg.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    return message

if __name__ == '__main__':
    #vg.run(debug=True)
    #vg.run(debug=False, host='0.0.0.0', port='8443',ssl_context=context)
    print("----------loading the spacy model first plz wait-----")
    #loadmodel()
    vg.run(debug=False, host='0.0.0.0', port='8443')
