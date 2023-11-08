from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def receive_data():
    received_data = request.json
    return jsonify(received_data)  # You can return the received data as a JSON response.

if __name__ == '__main__':
    app.run(port=80)
