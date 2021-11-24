from flask import Flask, render_template, request, redirect, url_for

import data_manager, util

app = Flask(__name__)


USER = ''


@app.route("/")
@app.route('/login', methods=['POST', 'GET'])
def main_page():
    global USER
    message = 'Create a New Account, or Log in'
    username = ''
    if '/login' in request.base_url:
        if request.method == 'POST' and request.form['password']:
            valid_password= data_manager.log_in(request.form)
            if not valid_password:
                return redirect(f'/?login=False&username={request.form["username"]}')
            USER = request.form['username']
            return redirect(f'/list')
    else:
        if request.args:
            if request.args['login'] == 'False':
                message = 'Wrong Password'
            if request.args['username']:
                username = request.args['username']
    return render_template('/main_page.html', message=message, username=username)


@app.route('/list', methods=['GET', 'POST'])
def list_posts():
    questions = data_manager.get_questions()
    if request.args:
        questions = data_manager.sort_questions(request.args)
    return render_template('list.html', user=USER, forum_posts=questions)


@app.route('/question/<question_id>')
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.answers_by_question_id(question_id)
    return render_template('display_question.html', question=question, forum_posts=answers)


@app.route('/add-question')
def ask_question():
    global USER
    util.create_question(request.form, USER)
    question_id = 1
    return render_template('add_question.html', new_question_id=question_id)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8000,
    )
