import Header from '../components/Header';
import React, { useState, useEffect } from 'react';
import './Convert.css';

export const Convert = ({response}) => {
  const [inputValue, setInputValue] = useState('');

function parseJson(jsonData) {

    let data = JSON.parse(jsonData);

    let result = '';

    for (const key in data) {
      const file = data[key];
      result += file['Название'] + ' - ' + file['Дата создания'] + '\n';
    }

    return result;
  }

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleConvertClick = () => {
    const textarea = document.querySelector('textarea'); // получаем textarea
    textarea.value = '1'; // значение в строчке сюда прокидывать
  };

  return (
    <div className="container"> 
      <div className="left-container">
          <div>
        <p>{parseJson(JSON.stringify(response.data))}</p>
        </div>
      </div>
      <div className="right-container">
        <div className="top-section">
          <button onClick={handleConvertClick}>Преобразовать</button>
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