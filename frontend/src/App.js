import axios from "axios";
import React, { useState } from "react";
import { Row, Col, Spinner, Container } from "react-bootstrap";
import './App.css';

function App() {
  const API_URL = 'http://127.0.0.1:8000/'
  const [aTeam, setATeam] = useState({
    characters: []
  });
  const [bTeam, setBTeam] = useState({
    characters: []
  });
  const [loading, setLoading] = useState(false)

  const generateTeams = () => {
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
      }).then(response => console.log(response)).catch(function(error) {
        console.log(error);
      });
    }
  }


  return (
    <div className="App">

      {loading 
      ? <>
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
        </>
      : <button className="btn btn-primary" onClick={() => generateTeams()}>Generar equipos</button>
      }
      {aTeam.characters.length > 0 && bTeam.characters.length > 0 && 
      <Container>
      <button className="btn btn-danger" onClick={() => runBattle()}>¡Pelear!</button>
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
    </div>
  );
}

export default App;
