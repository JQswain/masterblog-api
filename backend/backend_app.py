from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)



POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    response = POSTS.copy()

    valid_sorts = {'title', 'content'}
    valid_directions = {'asc', 'desc'}

    # If both sort and direction are provided
    if sort and direction:
        if sort not in valid_sorts or direction not in valid_directions:
            return jsonify({'error': 'sort or direction must be a valid type'}), 400
        reverse = direction == 'desc'
        response = sorted(response, key=lambda post: post[sort].lower(), reverse=reverse)

    # If only one is provided (incomplete query)
    elif sort or direction:
        return jsonify({'error': 'Both sort and direction must be provided'}), 400

    return jsonify(response)

@app.route('/api/posts', methods=['POST'])
def add_post():
    if not request.json or not 'title' in request.json or not 'content' in request.json:
        return jsonify({'error': 'Missing required parameter'}), 400
    request_data = request.get_json()
    request_data['id'] = (max(post['id'] for post in POSTS) + 1)
    POSTS.append(request_data)
    return request_data, 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({'message': f"Post with {post_id} has been deleted successfully."}), 200
    return jsonify({'message': f"Post with id {post_id} was not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            old_post = post
            data = request.get_json()
            if data['title']:
                title = data['title']
            else:
                title = old_post['title']
            if data['content']:
                content = data['content']
            else:
                content = old_post['content']
            updated_post = {
                'id': post_id,
                'title': title,
                'content': content,
            }
            POSTS[post_id - 1] = updated_post
            return jsonify(updated_post), 200

    return jsonify({'message': f"Post with id {post_id} was not found."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title', '').lower()
    content = request.args.get('content', '').lower()
    search_list = []

    for post in POSTS:
        matches_title = title in post['title'].lower() if title else True
        matches_content = content in post['content'].lower() if content else True

        if matches_title and matches_content:
            search_list.append(post)

    return jsonify(search_list), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
