from flask import Flask, render_template, request, redirect, url_for
import data_manager
app = Flask(__name__)


@app.route("/")
def main_page():
    message = 'Create a New Account, or Log in'
    username = ''
    if request.args:
        if request.args['login'] == 'False':
            message = 'Wrong Password'
            username = request.args['username']
    return render_template('/main_page.html', message=message, username=username)


@app.route('/list', methods=['GET', 'POST'])
def list_posts():
    print(request.form)
    if request.method == 'POST':
        logged_in, valid_password, new_user = data_manager.log_in(request.form)
        if not valid_password:
            return redirect('/?login=False')
        if logged_in:
            user = request.form["username"]
    else:
        return redirect(f'/?login=False&username={request.form["username"]}')
    return render_template('list.html', user=user)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000,
    )
