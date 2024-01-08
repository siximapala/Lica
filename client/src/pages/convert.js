import Header from '../components/Header';
import React, { useState } from 'react';
import './Convert.css';

export default function Convert(){
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleConvertClick = () => {
    const textarea = document.querySelector('textarea'); // получаем textarea
    textarea.value = '1'; // значение в строчке сюда прокидывать
  };

  return (
    <div className="container">
      <div className="left-container"></div>
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