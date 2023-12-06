import { useState } from 'react';

export default function App() {
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
    
    //здесь идёт отправка на некоторый адрес flask
    fetch('/some-api', { method: form.method, body: formData });
  }

  return (
    <div>
      
        <form method="post" onSubmit={handleSubmit}>
        <button onClick={handleClick}>Авторизоваться через Яндекс ID</button>,
        <p>Нажатие на кнопку переводит на сайт, где нужно авторизироваться через ЯндексID</p>
        <p>Скопируйте OAuth токен, после чего можете закрыть страницу. Введите его в поле ниже.</p>
        <label> Введите Oauth токен сюда: <input name="yadiskAPIToken" /> </label>
        <button type="submit">Подтвердить</button>
        </form>
      
    </div>
  );
}