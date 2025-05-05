import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Home } from './views/NewsList.tsx';
import { NewsDetail } from './views/NewsDetail.tsx';
import { Navbar } from './components/Navbar.tsx';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/news/:id" element={<NewsDetail />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;