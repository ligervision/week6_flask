from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

from . import routes