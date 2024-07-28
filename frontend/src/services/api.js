import axios from "axios";

const API_URL = 'http://127.0.0.1:8000/'

const generateTeams = (resetData, setLoading, setATeam, setBTeam) => {
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


const runBattle = (aTeam, bTeam, setBattleLogs, setWinner) => {
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
      }).then(response => {
        setBattleLogs(response.data.battle_logs)
        setWinner(response.data.winner)
      }).catch(function(error) {
        console.log(error);
      });
    }
  }


const sendBattleResumeEmail = (setEmailSuccess, setLoadingEmail, getWinner, battleLogs, email) => {
    setEmailSuccess(false);
    setLoadingEmail(true)
    const battleSummary = battleLogs.map(battleLog => `
      <p>${battleLog.a_character_name} (${battleLog.a_character_hp} hp) atacó a ${battleLog.b_character_name} (${battleLog.b_character_hp} hp) con un ataque tipo ${ battleLog.a_attack_type} y le hizo ${battleLog.a_attack_points} puntos de daño.\n</p>
      <p>${battleLog.b_character_name} (${battleLog.b_character_hp} hp) atacó a ${battleLog.a_character_name} (${battleLog.a_character_hp} hp) con un ataque tipo ${ battleLog.b_attack_type} y le hizo ${battleLog.b_attack_points} puntos de daño.\n</p>
      <p>----------------------------------------------------------------------------------</p>
      `)
      battleSummary.push(`<p>¡Gana el <strong>${getWinner()}</strong>!</p>`);
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

  export { generateTeams, runBattle, sendBattleResumeEmail }