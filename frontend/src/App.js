import React, { useState } from "react";
import { Row, Col, Spinner, Container, Alert } from "react-bootstrap";
import { generateTeams, runBattle, sendBattleResumeEmail } from "./services/api";
import CharacterData from "./components/CharacterData";
import BattleLogData from "./components/BattleLogData";
import './App.css';

function App() {
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
  const [emailSuccess, setEmailSuccess] = useState(false);
  const [winner, setWinner] = useState('');

  const resetData = () => {
    setBattleLogs([]);
    setLoading(false);
    setEmail('');
    setEmailSuccess(false);
    setWinner('');
  }

  const getWinner = () =>  winner === 'a_team' ? 'Equipo Azul' : 'Equipo Rojo';

  const validateTeams = () => aTeam.characters.length > 0 && bTeam.characters.length > 0


  return (
    <div className="App p-5">
      <div>
        <h1>Batallas de superhéroes</h1>
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
          <button className="btn btn-primary margin-right" onClick={() => generateTeams(resetData, setLoading, setATeam, setBTeam)}>Generar equipos</button>
          {validateTeams() && <button className="btn btn-danger" onClick={() => runBattle(aTeam, bTeam, setBattleLogs, setWinner)}>¡Pelear!</button>}
        </Col>
          
      </>
      }
      </Row>
      {validateTeams() && 
      <Container>
        <Row className="a-team mb-5 p-3">
          <h2>Equipo Azul</h2>
          {aTeam.characters.map(character => <CharacterData character={character}/>)}
        </Row>
        <Row className="b-team p-3">
          <h2>Equipo Rojo</h2>
          {bTeam.characters.map(character => <CharacterData character={character}/>)}
        </Row>
      </Container>
      }

      {battleLogs && battleLogs.length > 0 && 
      <>
        <Row>
          {battleLogs.map(battleLog => <BattleLogData battleLog={battleLog}/>)}

          <div className="mb-5">¡Gana el <strong>{getWinner()}</strong>!</div>

        </Row>
        <Row className="justify-content-center">
          <Col xs={3}>
            <input className="form-control w-20 mb-3" type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
            {loadingEmail 
            ? <Spinner animation="border" role="status"><span className="visually-hidden">Loading...</span></Spinner>
            : <button className="btn btn-danger mb-3" onClick={() => sendBattleResumeEmail(setEmailSuccess, setLoadingEmail, getWinner, battleLogs, email)}>Enviar resumen al correo</button>}
            {emailSuccess && <Alert variant="success">¡Resumen enviado!</Alert>}
          </Col>
        </Row>
        
      </>}
    </div>
  );
}

export default App;
