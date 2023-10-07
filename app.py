from flask import Flask, request, render_template
from func.chatgpt import ChatGPT

app = Flask(__name__)

search_engine = ChatGPT('./database.pkl')

@app.route("/hello")
def thread_summary():
    return 'Hello World!'

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