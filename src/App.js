
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import { MainDropdown } from './components/Dropdowns';
import Home from "./pages/Home";
import Season from "./pages/season";
import Faq from "./pages/faq";
import { Skaters, Goalies } from "./pages/players";
import { Shotcards } from "./pages/shotcard";
import './styles/App.css'; // Correct import statement

function App() {
  //
  return (
    <div className="App">
      <div className="outer"></div>
      <div className="middle">
        <Router>
          <MainDropdown />
          <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/season" element={<Season />} />
          <Route path="/players/skaters" element={<Skaters />} /> 
          <Route path="/players/goalies" element={<Goalies />} />
          <Route path='/faq' element={<Faq />} />
          <Route path='/shotcard' element={<Shotcards />} />
          </Routes>
        </Router>
      </div>
      <div className="outer"></div>
    </div>
  );
}

export default App;