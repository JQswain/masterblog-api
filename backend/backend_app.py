from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)

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



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
