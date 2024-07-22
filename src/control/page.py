from flask import Blueprint , render_template , request, redirect , url_for , jsonify
chatboard = Blueprint('chatboard' , __name__)

@chatboard.route('/main-page')
def mainpage():
    return render_template("main_screen.html")

@chatboard.route('/sub-page')
def subpage():
    return render_template("rule_chat.html")

# @chatboard.route('/rule-chat')
# def rule_chat():
#     return render_template('rule_chat.html')

# @chatboard.route('/main-screen')
# def change_sub():
#     return redirect(url_for('rule_chat'))