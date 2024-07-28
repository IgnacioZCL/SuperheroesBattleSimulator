import axios from "axios";
import React, { useState } from "react";
import { Row, Col, Spinner, Container, Alert } from "react-bootstrap";
import './App.css';

function App() {
  const API_URL = 'http://127.0.0.1:8000/'
  const [aTeam, setATeam] = useState({
    characters: []
  });
  const [bTeam, setBTeam] = useState({
    characters: []
  });
  const [battleLogs, setBattleLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingEmail, setLoadingEmail] = useState(false);
  const [email, setEmail] = useState('');
  const [emailSuccess, setEmailSuccess] = useState(false)

  const resetData = () => {
    setBattleLogs([]);
    setLoading(false);
    setEmail('');
    setEmailSuccess(false)
  }
  
  const generateTeams = () => {
    resetData();
    setLoading(true);
    axios.get(`${API_URL}generate_teams/`).then((response) => {
      setATeam(response.data.a_team)
      setBTeam(response.data.b_team)
      setLoading(false)
    }).catch(function(error) {
      console.log(error);
    });
  }

  const runBattle = () => {
    if (aTeam.characters.length > 0 && bTeam.characters.length > 0) {
      const data = {
        a_team: aTeam,
        b_team: bTeam
      }
  
      axios.post(`${API_URL}simulate_battle/`, JSON.stringify(data), {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        }
      }).then(response => setBattleLogs(response.data.battle_logs)).catch(function(error) {
        console.log(error);
      });
    }
  }

  const sendBattleResumeEmail = () => {
    setLoadingEmail(true)
    const battleSummary = battleLogs.map(battleLog => `
      ${battleLog.a_character_name} (${battleLog.a_character_hp} hp) atacó a ${battleLog.b_character_name} (${battleLog.b_character_hp} hp) con un ataque tipo ${ battleLog.a_attack_type} y le hizo ${battleLog.a_attack_points} puntos de daño.\n
      ${battleLog.b_character_name} (${battleLog.b_character_hp} hp) atacó a ${battleLog.a_character_name} (${battleLog.a_character_hp} hp) con un ataque tipo ${ battleLog.b_attack_type} y le hizo ${battleLog.b_attack_points} puntos de daño.\n
      ----------------------------------------------------------------------------------`)
    const data = {
      receiver: email,
      battle_summary: battleSummary.join('')
    }
    axios.post(`${API_URL}send_battle/`, JSON.stringify(data), {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      }
    }).then(response => {
      setEmailSuccess(true)
      setLoadingEmail(false)
    }).catch(function(error) {
      console.log(error);
    });
  }

  const validateTeams = () => aTeam.characters.length > 0 && bTeam.characters.length > 0


  return (
    <div className="App p-5">
      <div>
        <h1>Batallas de súperheroes</h1>
        <p>Esta aplicación consume la API de SuperHeroes API para obtener personajes de forma aleatoria con sus estadísticas y permite simular batallas.
        </p>
      </div>
      <Row className="mb-5">
      {loading 
      ? <Col>
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
        </Col>
      : 
      <>
        <Col>
          <button className="btn btn-primary margin-right" onClick={() => generateTeams()}>Generar equipos</button>
          {validateTeams() && <button className="btn btn-danger" onClick={() => runBattle()}>¡Pelear!</button>}
        </Col>
          
      </>
      }
      </Row>
      {validateTeams() && 
      <Container>
        <Row className="a-team mb-5 p-3">
          <h2>Equipo Azul</h2>
          {aTeam.characters.map(character => (
            <Col className="p-3" key={character.id}>
              <img className="character-image mb-2" src={character.image} alt={character.name}/>
              <h5>Nombre: {character.name}</h5>
              <div>Combate: {character.combat}</div>
              <div>Poder: {character.power}</div>
              <div>Inteligencia: {character.intelligence}</div>
              <div>Velocidad: {character.speed}</div>
              <div>Fuerza: {character.strength}</div>
              <div>Durabilidad: {character.durability}</div>
              <div>Alineacion: {character.alignment}</div>
            </Col>
          ))}
        </Row>
        <Row className="b-team p-3">
          <h2>Equipo Rojo</h2>
          {bTeam.characters.map(character => (
            <Col className="p-3" key={character.id}>
              <img className="character-image mb-2" src={character.image} alt={character.name}/>
              <h5>Nombre: {character.name}</h5>
              <div>Combate: {character.combat}</div>
              <div>Poder: {character.power}</div>
              <div>Inteligencia: {character.intelligence}</div>
              <div>Velocidad: {character.speed}</div>
              <div>Fuerza: {character.strength}</div>
              <div>Durabilidad: {character.durability}</div>
              <div>Alineacion: {character.alignment}</div>
            </Col>
          ))}
        </Row>
      </Container>
      }

      {battleLogs && battleLogs.length > 0 && 
      <>
        <Row>
          {battleLogs.map(battleLog => 
          <div className="mb-5">
            <div><span className="a-character bold-text">{battleLog.a_character_name} ({battleLog.a_character_hp} hp)</span> atacó a 
            <span className="b-character bold-text"> {battleLog.b_character_name} ({battleLog.b_character_hp} hp)</span> con un ataque tipo 
            <span className="bold-text"> { battleLog.a_attack_type}</span> y le hizo <span className="bold-text">{battleLog.a_attack_points} puntos de daño</span></div>  
            <div><span className="b-character bold-text">{battleLog.b_character_name} ({battleLog.b_character_hp} hp)</span> atacó a 
            <span className="a-character bold-text"> {battleLog.a_character_name} ({battleLog.a_character_hp} hp)</span> con un ataque tipo 
            <span className="bold-text"> {battleLog.b_attack_type}</span> y le hizo <span className="bold-text">{battleLog.b_attack_points} puntos de daño</span></div>  
          </div>)}
        </Row>
        <Row className="justify-content-center">
          <Col xs={3}>
            <input className="form-control w-20 mb-3" type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
            {loadingEmail ? <Spinner animation="border" role="status"><span className="visually-hidden">Loading...</span></Spinner>: <button className="btn btn-danger mb-3" onClick={() => sendBattleResumeEmail()}>Enviar resumen al correo</button>}
            {emailSuccess && <Alert variant="success">¡Resumen enviado!</Alert>}
          </Col>
        </Row>
        
      </>}
    </div>
  );
}

export default App;
