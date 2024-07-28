import { Col } from "react-bootstrap"

const CharacterData = (props) => {
    const { character } = props;
    return(
    <>
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
    </>
    );
}

export default CharacterData;