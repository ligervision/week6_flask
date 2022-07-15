from . import bp as api
from .auth import basic_auth, token_auth
from flask import jsonify, request
from app.models import Post, User

@api.route('/token')
@basic_auth.login_required
def index():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token, 'expiration': user.token_expiration})


@api.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for field in ['email', 'username', 'password']:
        if field not in data:
            return jsonify({'error': f'{field} must be in request body'}), 400
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    user_check = User.query.filter((User.email == email)|(User.username == username)).all()
    if user_check:
        return jsonify({'error': 'A user with that username and/or email already exists.'}), 400
    new_user = User(email=email, username=username, password=password)
    return jsonify(new_user.to_dict()), 201


@api.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


@api.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@api.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get the data from request body
    data = request.json
    # Check to make sure all required fields are present
    for field in ['title', 'body']:
        if field not in data:
            # if not return a 400 response with error
            return jsonify({'error': f'{field} must be in request body'}), 400
    # Get fields from data dict
    title = data.get('title')
    body = data.get('body')
    user_id = token_auth.current_user().id
    # Add new post to database with request body info
    new_post = Post(title=title, body=body, user_id=user_id)
    return jsonify(new_post.to_dict()), 201


@api.route('/posts/<post_id>', methods=['PUT'])
@token_auth.login_required
def update_post(post_id):
    post_to_edit = Post.query.get_or_404(post_id)
    current_user = token_auth.current_user()
    if current_user != post_to_edit.author:
        return jsonify({'error': 'You do not have authorization to edit this post'}), 403
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    post_to_edit.update(**request.json)
    return jsonify(post_to_edit.to_dict())

@api.route('/posts/<post_id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    current_user = token_auth.current_user()
    if current_user != post_to_delete.author:
        return jsonify({'error': 'You do not have authorization to delete this post'}), 403
    post_to_delete.delete()
    return jsonify({'message': 'You have successfully deleted the post'})