from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)


@app.route("/")
@app.route('/login', methods=['POST', 'GET'])
def main_page():
    message = 'Create a New Account, or Log in'
    username = ''
    if '/login' in request.base_url:
        if request.method == 'POST' and request.form['password']:
            logged_in, valid_password, new_user = data_manager.log_in(request.form)
            if not valid_password:
                return redirect(f'/?login=False&username={request.form["username"]}')
            return redirect(f'/list?username={request.form["username"]}')
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
    return render_template('list.html', user=request.args["username"], questions=questions)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000,
    )
