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
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    response = POSTS.copy()

    valid_sorts = {'title', 'content'}
    valid_directions = {'asc', 'desc'}

    if not sort and direction:
        return jsonify(response)

    elif sort not in valid_sorts or direction not in valid_directions:
        return jsonify({'error': 'sort or directions must be a valid type'}, 400)

    elif sort in valid_sorts and direction in valid_directions:
        reverse = direction == 'desc'
        response = sorted(response, key=lambda post: post[sort].lower(), reverse=reverse)

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
    title = request.args.get('title')
    content = request.args.get('content')
    search_list = []
    if title and content:
        for post in POSTS:
            matches_title = title or title.lower() in post['title'].lower()
            matches_content = content or content.lower() in post['content'].lower()

            if (title and matches_title) or (content and matches_content):
                search_list.append(post)

    return jsonify(search_list), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
