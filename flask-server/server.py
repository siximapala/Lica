from flask import Flask, request, session, url_for, redirect
import yadisk
from flask_cors import CORS
import literature_script
from yadisk_class import *


app = Flask(__name__)
CORS(app)


@app.route("/data", methods=['POST','GET'])
def handle_data():
    if request.method == 'POST':    
        data = request.get_json()
        print(data) ##полученные данные
        yandex_api_function = I_yadisk("y0_AgAAAABF_QebAAr1PwAAAAD0J7_iFf1mi2K1TICY7B-19b5bS3gXuzE")
        dataForConvert = yandex_api_function.get_files_name("Lica")
        return dataForConvert
    else:
        return "GET method active"



if __name__ == "__main__":
    app.run(debug=True)