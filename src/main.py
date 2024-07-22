import os
from flask import Flask
from flask_cors import CORS 
from control import page
#https 만을 지원하는 기능을 http에서도 지원할 수 있도록 테스트 가능하게 만듬
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__ , static_url_path='/static' , template_folder="view") #html에서 가져올 데이터는 static 에서 가지고 와라
CORS(app) #별도 서버 간에 rest api 지원을 하기 위해서 
app.secret_key = 'chatboard_server'

app.register_blueprint(page.chatboard , url_prefix = '/chatboard')


if __name__ == '__main__':
    app.run(host = '0.0.0.0' , port='8080' , debug=True)