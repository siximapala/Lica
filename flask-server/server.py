from flask import Flask, request, session, url_for, redirect
import yadisk
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/data", methods=['POST','GET'])
def handle_data():
    if request.method == 'POST':    
        data = request.get_json()
        print(data) ##полученные данные
        return 'success POST!'
    else:
        return "GET method active"


if __name__ == "__main__":
    app.run(debug=True)