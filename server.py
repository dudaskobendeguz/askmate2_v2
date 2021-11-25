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
            valid_password= util.log_in(request.form)
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
    return render_template('main_page.html', message=message, username=username)


@app.route('/list', methods=['GET', 'POST'])
def list_posts():
    questions = data_manager.get_questions()
    if request.args:
        questions = util.sort_questions(request.args)
    return render_template('list.html', user=USER, forum_posts=questions)


@app.route('/question/<question_id>')
def display_question(question_id):
    global USER
    question = util.get_user_post_by_id(question_id, is_question=True)
    answers = data_manager.answers_by_question_id(question_id)
    return render_template('display_question.html', question=question, forum_posts=answers, user=USER)


@app.route('/add-question')
def ask_question():
    global USER
    util.create_question(request.form, USER)
    question_id = 1
    return render_template('add_question.html')


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete(question_id=None, answer_id=None):
    if question_id:
        util.delete_question(question_id)
    else:
        util.delete_answer(answer_id)
    return redirect('/list')


@app.route('/question/<question_id>/vote_up')
@app.route('/question/<question_id>/vote_down')
@app.route('/answer/<answer_id>/vote_up')
@app.route('/answer/<answer_id>/vote_down')
def vote(question_id=None, answer_id=None):
    if question_id:
        if 'vote_up' in request.base_url:
            util.vote(question_id, is_question=True, vote=1)
        else:
            util.vote(question_id, is_question=True, vote=-1)
    else:
        if 'vote_up' in request.base_url:
            util.vote(answer_id, is_question=False, vote=1)
        else:
            util.vote(answer_id, is_question=False, vote=-1)
    return redirect("/list")

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8000,
    )
