import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Filmes from "./pages/Filmes";
import Salas from "./pages/Salas";
import Ingressos from "./pages/Ingressos";
import Home from "./pages/Home";

function App() {
  return (
    <Router>
      <nav style={{padding:10, background:"#222"}}>
        <Link to="/" style={{color:"#fff", marginRight:10}}>Home</Link>
        <Link to="/filmes" style={{color:"#fff", marginRight:10}}>Filmes</Link>
        <Link to="/salas" style={{color:"#fff", marginRight:10}}>Salas</Link>
        <Link to="/ingressos" style={{color:"#fff"}}>Ingressos</Link>
      </nav>
      <div style={{padding:20}}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/filmes" element={<Filmes />} />
          <Route path="/salas" element={<Salas />} />
          <Route path="/ingressos" element={<Ingressos />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;