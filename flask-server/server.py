from flask import Flask, request, jsonify
import yadisk

app = Flask(__name__)

@app.route("/members")
def members():
    return {"members":["Member1", "Member2", "Member3"]}

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json.get('data')
    # Обработка полученных данных
    print(data) 
    return jsonify({'message': f'Received data: {data}'})

if __name__ == "__main__":
    app.run(debug=True)