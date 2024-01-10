import Header from '../components/Header';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
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
    const textarea = document.querySelector('textarea');
    axios.post('http://localhost:5000/convert', true)
        .then(response => {
            const convertedText = JSON.stringify(response.data).replace(/\\n/g, '\n');
            textarea.innerHTML = convertedText;
        })
        .catch(error => console.log(error));
};

  return (
    <div className="container"> 
      <div className="left-container">
          <div>
       
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