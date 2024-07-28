const BattleLogData = (props) => {
    const { battleLog } = props;
    return(
    <>
        <div className="mb-5">
            <div><span className="a-character bold-text">{battleLog.a_character_name} ({battleLog.a_character_hp} hp)</span> atacó a 
            <span className="b-character bold-text"> {battleLog.b_character_name} ({battleLog.b_character_hp} hp)</span> con un ataque tipo 
            <span className="bold-text"> { battleLog.a_attack_type}</span> y le hizo <span className="bold-text">{battleLog.a_attack_points} puntos de daño</span></div>  
            <div><span className="b-character bold-text">{battleLog.b_character_name} ({battleLog.b_character_hp} hp)</span> atacó a 
            <span className="a-character bold-text"> {battleLog.a_character_name} ({battleLog.a_character_hp} hp)</span> con un ataque tipo 
            <span className="bold-text"> {battleLog.b_attack_type}</span> y le hizo <span className="bold-text">{battleLog.b_attack_points} puntos de daño</span></div>  
          </div>
    </>
    );
}


export default BattleLogData;