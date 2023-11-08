from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_data', methods=['POST'])
def receive_data():
    all = request.json

    return f'{all}'


if __name__ == '__main__':
    app.run(port=80)
