import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Convert.css';
import { useNavigate} from 'react-router-dom';

export const Convert = ({response}) => {
  const [inputValue, setInputValue] = useState('');
  const navigate = useNavigate();

function parseJson(jsonData) {
    let data = JSON.parse(jsonData);
    let result = 'Эти доступные документы будут преобразованы:<br><br>';
    for (const key in data) {
      const file = data[key];
      result += file['Название'] + '.<br> Дата создания: ' + file['Дата создания']+'.<br> Размер: ' + Math.floor(file['Размер']/1024/1024*1000)/1000+'МБ.' + '<br><br>';
    }
    return result;
  }

  if (response.data != undefined){
    let infoAboutFiles = document.getElementById('filesInfo');
    if (response.data != "ERROR: НЕКОРРЕКТНЫЙ ТОКЕН ИЛИ ПАПКИ 'LICA' НЕ СУЩЕСТВУЕТ НА УКАЗАННОМ ПРОСТРАНСТВЕ."){
      let dataToShow = parseJson(JSON.stringify(response.data));
      infoAboutFiles.innerHTML = dataToShow;
    }
    else{
      infoAboutFiles.innerHTML = response.data;
    }
  }
  


  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleConvertClick = () => {
    const textarea = document.querySelector('textarea');
    const buttonText = document.querySelector('button');
    buttonText.textContent = "Преобразование..."
    buttonText.disabled = true;

    axios.post('http://localhost:5000/convert', true)
        .then(response => {
            let convertedText;
            console.log(response.data)
            if (response.data == "ERROR! ВЕРНИТЕСЬ НА ГЛАВНУЮ СТРАНИЦУ ДЛЯ РЕИНИЦИАЛИЗАЦИИ ТОКЕНА"){
              convertedText = response.data
            }
            else {
              convertedText = response.data.replace(/\\n/g, '\n');
            }
            textarea.innerHTML = convertedText;
            buttonText.textContent = "Преобразовать"
            buttonText.disabled = false;
        })
        .catch(error => console.log(error))
  
};

  return (
    <div className="container"> 
      <div className="left-container">
      <p id="filesInfo">Загрузка данных...</p>
      </div>
      <div className="right-container">
        <div className="top-section">
          <button disabled={false} onClick={handleConvertClick}>Преобразовать</button>
        </div>
        <div className="bottom-section">
        <textarea
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Здесь будет информация об источнике литературы. Также здесь можно изменять его под свои нужды и писать что-то своё."
          />
        </div>
      </div>
    </div>
  );
}