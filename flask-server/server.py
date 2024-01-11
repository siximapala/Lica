from flask import Flask, request, session, url_for, redirect
import yadisk
from flask_cors import CORS
from literature_script import get_all
from yadisk_class import *


app = Flask(__name__)
CORS(app)


yandex_api_token = str()

@app.route("/data", methods=['POST','GET'])
def handle_data():
    if request.method == 'POST':    
        data = request.get_json()

        global yandex_api_token 
        yandex_api_token = str(data)[20:-2:] ##полученный токен
        yandex_api_function = I_yadisk(yandex_api_token)
        try:
            dataForConvert = yandex_api_function.get_files_name("Lica")
        except:
            return "ERROR: НЕКОРРЕКТНЫЙ ТОКЕН ИЛИ ПАПКИ 'LICA' НЕ СУЩЕСТВУЕТ НА УКАЗАННОМ ПРОСТРАНСТВЕ."
        
        return dataForConvert
    else:
        return "GET method active"

@app.route("/convert", methods=['POST','GET'])
def handle_convert():
    if request.method == 'POST':
        yandex_api_function = I_yadisk(yandex_api_token)
        try:
            converted_data = get_all(yandex_api_function.download_all_files())
            return converted_data
        except:
            return "ERROR! ВЕРНИТЕСЬ НА ГЛАВНУЮ СТРАНИЦУ ДЛЯ РЕИНИЦИАЛИЗАЦИИ ТОКЕНА"



if __name__ == "__main__":
    app.run(debug=True)