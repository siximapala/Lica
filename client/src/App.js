import { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter, Route, Routes} from 'react-router-dom';
import Convert from './pages/convert.js';
import Start from './pages/start.js';

export default function App() {
  
  return (
    <div>
      <BrowserRouter>
      <Routes>
        <Route index element={<Start/>} />
        <Route path='/convert' element={<Convert/>} />
      </Routes>
      </BrowserRouter>
    </div>

  );
}