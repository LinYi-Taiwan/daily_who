from flask import Flask, request, render_template, jsonify, Response
from func.chatgpt import ChatGPT
from handlers.error_handlers import method_not_allowed, page_not_found, internal_server_error

from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

search_engine = ChatGPT('./database.pkl')

# set app configs
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# flask swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Todo List API"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


# 錯誤處理
app.errorhandler(405)(method_not_allowed)
app.errorhandler(404)(page_not_found)
app.errorhandler(500)(internal_server_error)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        question = request.form.get('user_input')
        result = search_engine.get_similarity(question)
    else:
        question = 'No question.'
        result = 'No result.'

    return render_template('index.html', response=result)


def create_response(status, message, data):
    return {
        "status": status,
        "message": message,
        "data": data
    }


@app.route('/gpt/similarity', methods=['POST'])
def get_article_similarity() -> Response:
    if request.method != 'POST':
        result = create_response(400, "Invalid request", None)
        return jsonify(result)

    data = request.get_json()
    user_input = data.get('user_input')
    # 當使用者輸入的資料為空值時，回傳400
    if not user_input:
        result = create_response(
            400, "Invalid request, input can not be empty.", None)
    else:
        similarity_result = search_engine.get_similarity(user_input)
        if similarity_result is not None:
            result = create_response(200, "Success", similarity_result)
        else:
            result = create_response(500, "Internal Server Error", None)

    return jsonify(result)
