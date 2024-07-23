from flask import Blueprint , render_template , request, redirect , url_for , jsonify
import os
import json

from model.test_llm import test_llm

chatboard = Blueprint('chatboard' , __name__)

@chatboard.route('/main-page')
def mainpage():
    return render_template("main_screen.html")

@chatboard.route('/sub-page')
def subpage():
    name = request.args.get('name')
    description = request.args.get('description')
    players = request.args.get('players')
    difficulty = request.args.get('difficulty')
    age = request.args.get('age')
    playtime = request.args.get('playtime')
    image = request.args.get('image')
    print(name, description , players, difficulty, age , playtime)
    return render_template("rule_chat.html" , name=name, description=description , players=players , difficulty=difficulty, age=age , playtime=playtime , image = image)

# @chatboard.route('/rule-chat')
# def rule_chat():
#     return render_template('rule_chat.html')

# @chatboard.route('/main-screen')
# def change_sub():
#     return redirect(url_for('rule_chat'))

#JSON 파일 READ
@chatboard.route('/game_json' , methods=['GET'])
def game_json():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.abspath(os.path.join(current_dir , '..' , '..' , 'data' , 'game_info.json'))
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                return jsonify({"error": "Error decoding JSON"}), 400
    else:
        print('hi')
        return jsonify({"error": "File not found"}), 404
    print(data)
    print(jsonify(data))
    return jsonify(data)
@chatboard.route('/chatting', methods=['GET'])
def chat():
    try:
        message = request.args.get('message')
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        return test_llm(message), 200
    except Exception as e:
        chatboard.logger.error(f"Unhandled exception: {e}")
        return jsonify({'error': str(e)}), 500