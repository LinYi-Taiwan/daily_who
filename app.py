from flask import Flask, request, render_template
from func.chatgpt import ChatGPT
import requests

app = Flask(__name__)

search_engine = ChatGPT('./database.pkl')

@app.route("/get-gist")
def thread_summary():
    response = requests.get('https://gist.github.com/LinYi-Taiwan/a700aba96211f0ec2e2d158fe7531a90.json')
    response.raise_for_status()  # 如果請求出錯，這將引發一個異常
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def search():
    # query = request.args.to_dict()
    if request.method == 'POST':
        question = request.form.get('user_input')
        result = search_engine.get_simarity(question)
    else:
        question = 'No question.'
        result = 'No result.'

    return render_template('index.html', response=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)