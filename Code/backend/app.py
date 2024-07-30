from application import app
from application.video_chatbot import VideoChat
from flask import Flask, request,jsonify
from flask_cors import CORS

CORS(app)

videoChatbot = VideoChat()

@app.route('/videochat', methods=['POST'])

def chat():
   data = request.json
   user_input = data['message']
   response = videoChatbot.chat(user_input)
   return jsonify({'response':response})


if __name__ == '__main__':
   app.run(debug=True, port=2000, host='0.0.0.0')