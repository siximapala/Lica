import axios from 'axios';
import './Start.css';
import { useNavigate} from 'react-router-dom';

export const Start = ({setResponse}) => {
  const client_id = '111039d461f9409a8bfabcbbbdba725b';
  const navigate = useNavigate();

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
    //в консоли в браузере можно проверить отправку
    const formJson = Object.fromEntries(formData.entries());
    //отправка json yadisk api ключа на бэк и получение ответа
    axios.post('http://localhost:5000/data', formJson)
    .then(response => setResponse(response))
    .then(navigate('/convert'))
    .catch(error => console.log(error));
  }
  return (
<div className="centered-container">    
        <button onClick={handleClick}>Авторизоваться через Яндекс ID</button>
        <p>Нажатие на кнопку переводит на сайт, где нужно авторизироваться через ЯндексID</p>
        <p>Скопируйте OAuth токен, после чего можете закрыть страницу. Введите его в поле ниже.</p>
        <form method="post" onSubmit={handleSubmit}>
        <label> Введите Oauth токен сюда: <input name="yadiskAPIToken" /> </label>
        <button type="submit">Подтвердить</button>
        </form>
      
    </div>


  );
}