from flask import Flask
import yadisk

app = Flask(__name__)

@app.route("/members")
def members():
    return {"members":["Member1", "Member2", "Member3"]}

if __name__ == "__main__":
    app.run(debug=True)