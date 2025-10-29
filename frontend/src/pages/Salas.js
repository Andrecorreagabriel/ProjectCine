import React, {useEffect, useState} from "react";
import axios from "axios";
const API = process.env.REACT_APP_API_URL || "http://localhost:10000";

export default function Salas(){
  const [salas,setSalas] = useState([]);
  const [nova,setNova] = useState({nome:"",capacidade:""});
  useEffect(()=>{ carregar(); },[]);
  async function carregar(){ const r = await axios.get(API+"/api/salas"); setSalas(r.data); }
  async function adicionar(){ await axios.post(API+"/api/salas", nova); setNova({nome:"",capacidade:""}); carregar(); }
  return (<div>
    <h2>Salas</h2>
    <input placeholder="Nome" value={nova.nome} onChange={e=>setNova({...nova,nome:e.target.value})} /> <br/>
    <input placeholder="Capacidade" value={nova.capacidade} onChange={e=>setNova({...nova,capacidade:e.target.value})} /> <br/>
    <button onClick={adicionar}>Adicionar</button>
    <ul>{salas.map(s=><li key={s.id}>{s.nome} - {s.capacidade}</li>)}</ul>
  </div>); }