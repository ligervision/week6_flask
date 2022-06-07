from app import app
from flask import render_template, redirect, url_for
from app.forms import SignUpForm

#  routes -- How each endpoint should run

@app.route("/")
def index():
    user_dict = {
        'username': 'brians',
        'email': 'brians@codingtemple.com'        
    }
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']

    return render_template('index.html', user=user_dict, colors=colors)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('HELLO THIS WAS A HUGE SUCCESS!')
        # Get the data from the form fields
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
        # Add the user to the database

        # Show message of success/failure

        # redirect back to the homepage
        return redirect(url_for('index'))
        
    return render_template('signup.html', form=form)
