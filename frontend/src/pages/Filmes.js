import React, {useEffect, useState} from "react";
import axios from "axios";
const API = process.env.REACT_APP_API_URL || "http://localhost:10000";

export default function Filmes(){
  const [filmes,setFilmes] = useState([]);
  const [novo,setNovo] = useState({titulo:"",descricao:"",genero:""});
  useEffect(()=>{ carregar(); },[]);
  async function carregar(){ const r = await axios.get(API+"/api/filmes"); setFilmes(r.data); }
  async function adicionar(){ await axios.post(API+"/api/filmes", novo); setNovo({titulo:"",descricao:"",genero:""}); carregar(); }
  return (<div>
    <h2>Filmes</h2>
    <input placeholder="Título" value={novo.titulo} onChange={e=>setNovo({...novo,titulo:e.target.value})} /> <br/>
    <input placeholder="Descrição" value={novo.descricao} onChange={e=>setNovo({...novo,descricao:e.target.value})} /> <br/>
    <input placeholder="Gênero" value={novo.genero} onChange={e=>setNovo({...novo,genero:e.target.value})} /> <br/>
    <button onClick={adicionar}>Adicionar</button>
    <ul>{filmes.map(f=><li key={f.id}>{f.titulo} - {f.genero}</li>)}</ul>
  </div>); }