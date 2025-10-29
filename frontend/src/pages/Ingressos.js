import React, {useEffect, useState} from "react";
import axios from "axios";
const API = process.env.REACT_APP_API_URL || "http://localhost:10000";
export default function Ingressos(){
  const [ingressos,setIngressos] = useState([]);
  const [novo,setNovo] = useState({filme_id:"",sala_id:"",horario:"",preco:""});
  useEffect(()=>{ carregar(); },[]);
  async function carregar(){ const r = await axios.get(API+"/api/ingressos"); setIngressos(r.data); }
  async function adicionar(){ await axios.post(API+"/api/ingressos", novo); setNovo({filme_id:"",sala_id:"",horario:"",preco:""}); carregar(); }
  return (<div>
    <h2>Ingressos</h2>
    <input placeholder="ID Filme" value={novo.filme_id} onChange={e=>setNovo({...novo,filme_id:e.target.value})} /><br/>
    <input placeholder="ID Sala" value={novo.sala_id} onChange={e=>setNovo({...novo,sala_id:e.target.value})} /><br/>
    <input placeholder="Horário" value={novo.horario} onChange={e=>setNovo({...novo,horario:e.target.value})} /><br/>
    <input placeholder="Preço" value={novo.preco} onChange={e=>setNovo({...novo,preco:e.target.value})} /><br/>
    <button onClick={adicionar}>Adicionar</button>
    <ul>{ingressos.map(i=><li key={i.id}>Filme {i.filme_id} - Sala {i.sala_id} - {i.horario} - R${i.preco}</li>)}</ul>
  </div>); }