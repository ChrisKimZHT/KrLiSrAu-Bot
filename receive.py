import function
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=["POST"])
def post_data():
    if request.get_json().get('message_type') == 'private':
        uid = request.get_json().get('sender').get('user_id')
        message = request.get_json().get('raw_message')
        function.keyword_user(message, uid)
    elif request.get_json().get('message_type') == 'group':
        gid = request.get_json().get('group_id')
        uid = request.get_json().get('sender').get('user_id')
        message = request.get_json().get('raw_message')
        function.keyword_group(message, uid, gid)
    return 'OK'


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5701)
