from flask import Blueprint , render_template , request, redirect , url_for , jsonify
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_dir)
from src.model.Advanced_RAG.t_generation import Conversation
import json
chatboard = Blueprint('chatboard' , __name__)
conversation = Conversation()
#메인 페이지 로드
@chatboard.route('/main-page')
def mainpage():
    return render_template("main_screen.html")

#서브 페이지 로드
@chatboard.route('/sub-page')
def subpage():
    name = request.args.get('name')
    # description = request.args.get('description')
    # players = request.args.get('players')
    # difficulty = request.args.get('difficulty')
    # age = request.args.get('age')
    # playtime = request.args.get('playtime')
    # image = request.args.get('image')
    # print(name, description , players, difficulty, age , playtime)
    return render_template("rule_chat.html" , name=name)

#게임 관련 JSON 데이터 전송
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
    # print(jsonify(data))
    return jsonify(data)

#게임 관련 JSON 데이터 전송
@chatboard.route('/game_detail' , methods=['GET'])
def game_detail():
    name = request.args.get('name')
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
    for x in data['games']: 
        print(x["name"])
        if x['name'] == name:
            print("전달 내용 :", x) 
            return x , 200     
    return jsonify({"error": "Error Not JSON"}), 400


#채팅 데이터 LLM 전송
@chatboard.route('/chatting', methods=['GET'])
async def chat():
    try:
        message = request.args.get('message')
        game_name = request.args.get('name')
        players = request.args.get('players')
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        json_file_path = await get_json_path()
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                try:
                    data = json.load(json_file)
                except json.JSONDecodeError:
                    return jsonify({"error": "Error decoding JSON"}), 400
        
        target_file_name = await get_eng_name(data , game_name)
        print("메시지 :", message)
        if players == '0':
            players = 'It doesn\'t matter how many people it is'
            print(players)
        query = await conversation.generate_reply(message , target_file_name , "" , players)
        return query , 200
        # return reply(message, target_file_name), 200
    except Exception as e:
        chatboard.logger.error(f"Unhandled exception: {e}")
        return jsonify({'error': str(e)}), 500
    


#이미지 데이터 LLM 전송
@chatboard.route('/img_upload', methods=['POST'])
async def img_upload():
    try:
        # 파일 저장 경로 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        name = request.files['file']
        game_name = request.form.get('name')
        message = request.form.get('message')
        players = request.form.get('players')
        json_file_path = await get_json_path()
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                try:
                    data = json.load(json_file)
                except json.JSONDecodeError:
                    return jsonify({"error": "Error decoding JSON"}), 400
        target_file_name = await get_eng_name(data , game_name)
        UPLOAD_FOLDER = os.path.abspath(os.path.join(current_dir , '..' , '..' , 'data' , 'photo' , 'img.jpg'))
        name.save(UPLOAD_FOLDER)
        print("img_file_path" , UPLOAD_FOLDER)
        print("message :" , message)
        query = await conversation.generate_reply(message , target_file_name , UPLOAD_FOLDER , players)
        return jsonify({'data' : query}), 200
    except Exception as e:
        chatboard.logger.error(f"Unhandled exception: {e}")
        return jsonify({'error': str(e)}), 500
    

async def get_eng_name(data , game_name):
    eng_game_name = ""
    for x in data['games']:
        if x['name'] == game_name:
            eng_game_name = x['name_eng']
            break
    target_file_name = eng_game_name + '.pdf'
    print("eng_game name :" , target_file_name)
    return target_file_name

async def get_json_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.abspath(os.path.join(current_dir , '..' , '..' , 'data' , 'game_info.json'))
    return json_file_path