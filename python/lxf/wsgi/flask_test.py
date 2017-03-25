from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/signin', methods=['GET'])
def sign_form():
    return render_template('sign.html')


@app.route('/signin', methods=['POST'])
def sign():
    username = request.form['username']
    passwd = request.form['password']
    if username == 'root' and passwd == '1234':
        return render_template('sign-ok.html', username=username)

    return render_template('sign.html', message='wrong', username=username)


if __name__ == '__main__':
    app.run()
