from bardapi import Bard
import requests, json
import flask
from flask import Flask, request, jsonify

url = "https://free.churchless.tech/v1/chat/completions"
messages = []
token = "ZQg_XuFf4Z5tg3DvkLIVZTODiwvKzcDZiuaEWFS_u6m9BSk2saWvsA9YFRI2zGQXuW159A."
bard = Bard(token=token)
VERIFY_TOKEN = "456258az"
ACCESS_TOKEN = "EAADiW3LsU4UBOz6LLQZCGKLm6W9bSWvehvzn0uVLBXdHLNCGKZAbLiUPOf314rwKC8tO3ES7O4sKogUKtpWsg0PE0h1tZBj7USBRJj5HZCYugCpNyGrQt2sXWl9DjX4NQFynjtpAaRygmcdmAZBYzJNCS0vzqj6X7nZCUr5RdTxEgKv8VOFEBkfNZBuYIwb"
API_URL = f"https://graph.facebook.com/v12.0/me/messages?access_token={ACCESS_TOKEN}"

app = Flask(__name__)

def get_response(message):
  bard_answer = bard.get_answer(message)['content']
  with open('message_history.json', 'a') as history_file:
    data = {'question': message, 'answer': bard_answer}
    json.dump(data, history_file, ensure_ascii=False)
    history_file.write('\n')
  return bard_answer


def get_result(message):
  messages.append({"role": "user", "content": message})
  resp = requests.post(url,
                       json={
                           "model": "gpt-3.5-turbo",
                           "messages": messages,
                           "stream": False
                       }).content.decode('utf-8')
  gpt_answer = json.loads(
      resp.split('\n\n')[0])['choices'][0]['message']['content']
  messages.append({'role': 'assistant', 'content': gpt_answer})
  with open('message_history_gpt.json', 'a') as history_file:
    data = {'question': message, 'answer': gpt_answer}
    json.dump(data, history_file, ensure_ascii=False)
    history_file.write('\n')
  return gpt_answer

@app.route('/', methods=['GET', 'POST'])
def webhook():
  if request.method == 'GET':
    verify_token = flask.request.args.get('hub.verify_token')
    if verify_token == VERIFY_TOKEN:
      return flask.request.args.get('hub.challenge')
    return "Invalid verification token", 403
  elif request.method == 'POST':
    data = request.get_json()
    messaging_events = data['entry'][0]['messaging']
    for event in messaging_events:
      sender = event['sender']['id']
      if 'message' in event and event['message'].get('text'):
        message_text = event['message']['text']
        if message_text.startswith('/gpt'):
          gpt_answer = get_result(message_text)
          send_message(sender, gpt_answer)
        else:
          bard_answer = get_response(message_text)
          send_message(sender, bard_answer)
    return jsonify({"message": "OK"})
  return jsonify({"message": "OK"}) 


def send_message(recipient_id, message_text):
  params = {
      "recipient": {
          "id": recipient_id
      },
      "message": {
          "text": message_text
      }
  }
  response = requests.post(API_URL, json=params)
  return response.json()


if __name__ == '__main__':
    app.run()
