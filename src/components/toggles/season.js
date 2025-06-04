import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import React, { useState } from 'react';
import './ToggleButtons.css';


const teams = {
  1: 'NJD', 2: 'NYI', 3: 'NYR', 4: 'PHI', 5: 'PIT', 6: 'BOS', 7: 'BUF', 8: 'MTL', 9: 'OTT', 10: 'TOR',
  13: 'FLA', 14: 'TBL', 12: 'CAR', 15: 'WSH', 16: 'CHI', 17: 'DET', 18: 'NSH', 19: 'STL', 20: 'CGY',
  21: 'COL', 22: 'EDM', 23: 'VAN', 24: 'ANA', 25: 'DAL', 26: 'LAK', 28: 'SJS', 29: 'CBJ', 30: 'MIN',
  52: 'WPG', 54: 'VGK', 55: 'SEA', 59: 'UTA'
};

function SeasonToggleButtons() {
  const [imageUrl, setImageUrl] = useState(null);
  const teamIds = Object.keys(teams);
  const eventLabels = ['Hits', 'Giveaways', 'Takeaways', 'Goals', 'Shots', 'Misses', 'Blocked shot'];
  
  const [teamToggles, setTeamToggles] = useState(
      Object.fromEntries(teamIds.map(id => [id, false]))
      );
  const [eventToggles,setEventToggles]=useState(
      new Array(eventLabels.length).fill(false)
      );
  const handleTeamToggle = (teamId) => {
      setTeamToggles((prev) => ({
      ...prev,
      [teamId]: !prev[teamId], 
      }));
    };
  const handleEventToggle=(index)=>{
      setEventToggles((prev)=>{
      const updated = [...prev];
      updated[index]=!updated[index];
      return updated;
      });
    };
const sendTogglesToBackend = async () => {
  console.log(process.env.REACT_APP_API_URL);
  const activeTeams = Object.keys(teamToggles).filter(id => teamToggles[id]);
  const activeEvents = eventLabels.filter((_, index) => eventToggles[index]);

  try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/season`, {
      method: 'POST',
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
        'Accept' :'application/json'
      },
      body: JSON.stringify({
        teamIds: activeTeams,
        events: activeEvents,
      }),
    });

    const blob = await response.blob();
    const imgUrl = URL.createObjectURL(blob);
    setImageUrl(imgUrl);
  } catch (error) {
    console.error('Error sending POST request:', error);
  }
};

   
return (
  <div className="toggle-selection">
    {teamIds.map((id) => (
      <Button
        key={id}
        variant={teamToggles[id] ? 'secondary' : 'outline-secondary'}
        onClick={() => handleTeamToggle(id)}
      >
        {teams[id]}
      </Button>
    ))}
    <hr className="my-3" />

    <ButtonGroup className="toggle-sect">
      {eventLabels.map((label, index) => (
        <Button
          key={index}
          variant={eventToggles[index] ? 'secondary' : 'outline-secondary'}
          onClick={() => handleEventToggle(index)}
        >
          {label}
        </Button>
      ))}
    </ButtonGroup>

    <div className="mt-3">
      <Button onClick={sendTogglesToBackend} type="button">
        Send Data
      </Button>
    </div>
  {imageUrl && (
  <div className="mt-3">
    <img src={imageUrl} alt="Generated Chart" style={{ maxWidth: '100%' }} />
  </div>
)}
    
  </div>
);

}

export { SeasonToggleButtons };