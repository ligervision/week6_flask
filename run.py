from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_context():
    return {'db': db, 'Post': Post, 'User': User}