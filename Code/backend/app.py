from application import app
from application.video_chatbot import VideoChat
from application.code_chat import CodeChat
from application.support_chat import SupportChat
from flask import Flask, request,jsonify
from flask_cors import CORS

CORS(app)

videoChatbot = VideoChat()
codeChatbot = CodeChat()
SupportChatbot = SupportChat() 

@app.route('/videochat', methods=['POST'])
def chat():
   data = request.json
   user_input = data['message']
   response = videoChatbot.chat(user_input)
   return jsonify({'response':response})

@app.route('/codechat', methods=['POST'])
def code_chat():
   data = request.json
   user_input = data['message']
   response = codeChatbot.chat(user_input)
   return jsonify({'response':response})

@app.route('/supportchat', methods=['POST'])
def support_chat():
   data = request.json
   user_input = data['message']
   response = SupportChatbot.chat(user_input)
   return jsonify({'response':response})


if __name__ == '__main__':
   app.run(debug=True, port=2000, host='0.0.0.0')