# app.py
from flask import Flask, render_template, jsonify, request
from money import MoneySplitter

app = Flask(__name__)

@app.route('/')
def index():
    money_splitter = MoneySplitter()
    result = money_splitter.run_splitter()
    payers = list(result.keys())

    return render_template('index.html', payers=payers, receivers=payers)

@app.route('/run_script', methods=['GET'])
def run_script():
    money_splitter = MoneySplitter()
    result = money_splitter.run_splitter()

    return jsonify({"data": result})

if __name__ == '__main__':
    app.run(debug=True)
