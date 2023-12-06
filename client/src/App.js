import { useEffect, useState } from 'react';
import axios from 'axios';

export default function App() {
  const [data, setData] = useState('');
  const client_id = '111039d461f9409a8bfabcbbbdba725b';

  const handleClick = () => {
    const oauthUrl = 'https://oauth.yandex.ru/authorize?response_type=token&client_id='+client_id;
    window.open(oauthUrl, '_blank');
  };


  function handleSubmit(token) {
    // Чтобы браузер не перезагрузил страницу
    token.preventDefault();

    // Читает данные из формы, в которую положили ключ
    const form = token.target;
    const formData = new FormData(form);

    //в консоле в браузере можно проверить отправку
    const formJson = Object.fromEntries(formData.entries());
    console.log(formJson);
    
    //здесь идёт пост этих данных на адрес сервера React
    axios.post('/data', {data: formJson})
      .then(response => setData(response.data))
      .catch(error => console.error(error));
  }

  return (
    <div>
      
        
        <button onClick={handleClick}>Авторизоваться через Яндекс ID</button>,
        <p>Нажатие на кнопку переводит на сайт, где нужно авторизироваться через ЯндексID</p>
        <p>Скопируйте OAuth токен, после чего можете закрыть страницу. Введите его в поле ниже.</p>
        <form method="post" onSubmit={handleSubmit}>
        <label> Введите Oauth токен сюда: <input name="yadiskAPIToken" /> </label>
        <button type="submit">Подтвердить</button>
        </form>
      
    </div>
  );
}