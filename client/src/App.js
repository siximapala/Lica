import { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter, Route, Routes} from 'react-router-dom';
import {Convert} from './pages/convert.js';
import {Start} from './pages/start.js';

function App() {
  const [response, setResponse] = useState({});
  return (
    <div>
      <BrowserRouter>
      <Routes>
        <Route index element={<Start setResponse={setResponse}/>} />
        <Route path='/convert' element={<Convert response={response}/>} />
      </Routes>
      </BrowserRouter>
    </div>

  );
}

export default App;