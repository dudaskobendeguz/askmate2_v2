from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)


USER = ''


@app.route("/")
@app.route('/login', methods=['POST', 'GET'])
def main_page():
    global USER
    print(request.base_url)
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
    return render_template('list.html', user=USER, questions=questions)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000,
    )
