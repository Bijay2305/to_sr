from flask import Flask, redirect, request
from flask import jsonify
from stt_comparison import *

vg = Flask(__name__)


@vg.route('/')
def hello_world():
    return 'VG_!'


@vg.route('/compare/<cvp_text>/<stt_text>', methods=['GET'])
def invoke_compare(cvp_text=None, stt_text=None):
    if (request.method == 'GET'):
        print(type(cvp_text))
        print(type(stt_text))
        incoming_string = "Enroll your Card and you can get a promotional APR of 1.99%"
        ref = "Oh yeah, definitely so essentially 'cause if it will be enrolling your card. You'll be getting a promotional APR of around 1.99 on your new purchases during a promotional period of 9 billing cycles." \
              "I could go through some important information for you, I mean need to repeat the last one. I said, but if you are OK with this, I could go through with that information sure." \
              "K. Thank you so about the rates again and roll your card And you get a promotional APR of one point 99% on your purchases during a promotional period of 9 billing cycles." \
              "Beginning the day after you enroll after the promotional period ends the APR that will apply to any unpaid balances on these purchases will be the standard purchase APR on your account."
        # output = sentence_comparison(incoming_string, ref)
        output = sentence_comparison(cvp_text, stt_text)
        print(type(output))
        return jsonify(output)
        #return "csvp_text"
    return cvp_text
@vg.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }


if __name__ == '__main__':
    vg.run(debug=True)
    #vg.run(debug=False, host='0.0.0.0', port='8443')
