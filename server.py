import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import data_manager, util

UPLOAD_FOLDER = './static/picture/'
USER = None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
@app.route('/login', methods=['POST', 'GET'])
@app.route('/log_out')
def main_page():
    global USER
    message = 'Create a New Account, or Log in'
    username = ''
    if '/login' in request.base_url:
        if request.method == 'POST' and request.form['password']:
            valid_password = util.log_in(request.form)
            if not valid_password:
                return redirect(f'/?login=False&username={request.form["username"]}')
            USER = request.form['username']
            return redirect(f'/list')
    elif '/log_out' in request.base_url:
        USER = None
        return redirect('/')
    else:
        if request.args:
            if request.args['login'] == 'False':
                message = 'Wrong Password'
            if request.args['username']:
                username = request.args['username']
    return render_template('main_page.html', message=message, username=username)


@app.route('/list', methods=['GET', 'POST'])
def list_posts():
    global USER
    if not USER:
        return redirect('/')
    questions = data_manager.get_questions()
    if request.args:
        questions = util.sort_questions(request.args)
    return render_template('list.html', user=USER, forum_posts=questions)


@app.route('/question/<question_id>')
def display_question(question_id):
    global USER
    if not USER:
        return redirect('/')
    if request.args:  # view=true
        util.increase_view(question_id)
    question = util.get_user_post_by_id(question_id, is_question=True)
    answers = data_manager.answers_by_question_id(question_id)
    return render_template('display_question.html', question=question, forum_posts=answers, user=USER)


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
@app.route('/add-question', methods=['POST', 'GET'])
def ask_question(question_id=None):
    global USER
    if not USER:
        return redirect('/')
    if request.method == 'POST':
        image = request.files['image']
        if image.filename != '':
            if util.allowed_file(image):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = ''
        if question_id:
            util.create_answer(request.form, question_id, USER, filename)
        else:
            question_id = util.create_question(request.form, USER, filename)
        return redirect(f'/question/{question_id}')
    if question_id:
        return render_template('add_answer.html', question_id=question_id)
    else:
        return render_template('add_question.html')


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete(question_id=None, answer_id=None):
    global USER
    if not USER:
        return redirect('/')
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
    global USER
    if not USER:
        return redirect('/')
    if question_id:
        if 'vote_up' in request.base_url:
            util.vote(question_id, is_question=True, vote=1)
        else:
            util.vote(question_id, is_question=True, vote=-1)
        return redirect("/list")
    else:
        if 'vote_up' in request.base_url:
            util.vote(answer_id, is_question=False, vote=1)
        else:
            util.vote(answer_id, is_question=False, vote=-1)
        answer = util.get_user_post_by_id(answer_id, is_question=False)
        return redirect(f'/question/{answer["question_id"]}')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8000,
    )
