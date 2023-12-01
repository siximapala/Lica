import {useState/*создание переменной useState, для получения данных из бэкенда, рендерить данные на странице*/,
 useEffect /*получать бэкенд API для рендера*/} from 'react';

export default function App() {
  
const [data, setData] = useState([{}])
useEffect(() =>{
    fetch("/members").then(
      
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])


  return (
    <div>
    {(typeof data.members === 'undefined') ? (<p>
      Loading...
    </p>) : (data.members.map((member, i) =>
    (
      <p key={i}> {member}</p>
    ))
    )}
  </div>
  );
}