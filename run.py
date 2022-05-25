from flask import Flask, jsonify, make_response, request

# SSL configuration
from OpenSSL import SSL

from rasa.shared.utils.io import json_to_string
#from rasa.core.channels.channel import UserMessage
import asyncio
from rasa.core.agent import Agent
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

agent = Agent.load('/opt/app-root/src/.openshift/models/nlu-20210529-182119.tar.gz')

context = SSL.Context(SSL.SSLv23_METHOD)
context = ('/opt/epaas/certs/cert', '/opt/epaas/certs/key')

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Health Check : [Successful] [OK]"

@app.route('/sentiment', methods=['POST'])
def predict_sentiment():
    text = request.args.get('text')
    vader_analyser = SentimentIntensityAnalyzer()
    score = vader_analyser.polarity_scores(text)
    return score

@app.route('/intent', methods=['POST'])
def predict_intent():
    text = request.args.get('text')
    print("NLU model loaded. Type a message and press enter to parse it.")
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(agent.parse_message_using_nlu_interpreter(text))
    return json_to_string(result)

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port='8443')
    app.run(debug=False, host='0.0.0.0', port='8443', ssl_context=context)
