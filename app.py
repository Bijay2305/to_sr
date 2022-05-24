from flask import Flask, redirect, request
from flask import jsonify
from stt_comparison import *
import json
vg = Flask(__name__)

@vg.route('/')
def hello_world():
    return 'VG_!'

@vg.route('/compare/<cvp_text>/<stt_text>', methods=['GET'])
def invoke_compare(cvp_text=None, stt_text=None):
    if (request.method == 'GET'):
        output = sentence_comparison(cvp_text, stt_text)
        print(type(output))
        return jsonify(output)
@vg.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    return message

@vg.route('/comparison', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):

        string_val = request.json
        print(string_val)
        #uuid = request.json.get.(string_val["uuid"])
        uuid= string_val["uuid"]
        cvp_text=string_val['CVP_TEXT']
        stt_text=string_val['STT_TEXT']
        print(cvp_text)
        print(stt_text)
        output = sentence_comparison(cvp_text, stt_text)
        output.update({"uuid": uuid})
        return jsonify(output)

    else:
        return 'Content-Type not supported!'
if __name__ == '__main__':
    #vg.run(debug=True)
    vg.run(debug=True, host='0.0.0.0', port='8443')
