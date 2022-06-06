from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    user_dict = {
        'username': 'brians',
        'email': 'brians@codingtemple.com'        
    }
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']

    return render_template('index.html', user=user_dict, colors=colors)

@app.route('/test')
def test():
    return 'This is a test.'

