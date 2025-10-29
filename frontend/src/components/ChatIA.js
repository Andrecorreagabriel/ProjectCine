import React, {useState} from "react";
import axios from "axios";
const API = process.env.REACT_APP_API_URL || "http://localhost:10000";
export default function ChatIA(){
  const [mensagem,setMensagem] = useState(""); const [resposta,setResposta] = useState("");
  async function enviar(){ const r = await axios.post(API+"/api/ia", {mensagem}); if(r.data.resposta) setResposta(r.data.resposta); else setResposta(JSON.stringify(r.data)); }
  return (<div>
    <h3>Assistente IA</h3>
    <textarea rows={3} value={mensagem} onChange={e=>setMensagem(e.target.value)} /><br/>
    <button onClick={enviar}>Enviar</button>
    {resposta && <div style={{marginTop:10, background:"#eee", padding:10}}><strong>IA:</strong><div>{resposta}</div></div>}
  </div>);
}