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
  const teamIds = Object.keys(teams);
  const eventLabels = ['Hits', 'Giveaways', 'Takeaways', 'Goals', 'Shots', 'Misses', 'Blocked shot'];

  // Initialize toggles state with false (off) for each team
  const [teamToggles, setTeamToggles] = useState(
    Object.fromEntries(teamIds.map(id => [id, false]))
  );
  const [eventToggles,setEventToggles]=useState(
    new Array(eventLabels.length).fill(false));
  

  // Handle toggle action for each team
  const handleTeamToggle = (teamId) => {
    setTeamToggles((prev) => ({
      ...prev,
      [teamId]: !prev[teamId], // Toggle the state of the clicked team
    }));
  };
  const handleEventToggle=(index)=>{
    setEventToggles((prev)=>{
      const updated = [...prev];
      updated[index]=!updated[index];
      return updated;
    });
  };
  // Send activated toggles (selected teams) to backend
  const sendTogglesToBackend = async () => {
    // Get an array of active (selected) team IDs
    const activeTeams = Object.keys(teamToggles).filter(id =>teamToggles[id]);
    const activeEvents = eventLabels.filter((_,index)=>eventToggles[index]);

    if (activeTeams.length===0 && activeEvents.length===0){
      console.log('No data selected');
      return;
    }
      try {
        const response = await fetch('http://localhost:5000/api/season', {
          method: 'Post',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'  // 🔥 This is what Flask needs
          },
          
          body: JSON.stringify({ teamIds: activeTeams,
                                 events: activeEvents
          }),  // Add the selected teams as a body or params
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Backend Response:', data);
        } else {
          console.error('Error sending data to backend');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    } 
  return (
    <div className="toggle-section">
      {teamIds.map((id) => (
        <Button
          key={id}
          variant={teamToggles[id] ? 'secondary' : 'outline-secondary'}
          onClick={() => handleTeamToggle(id)}
        >
          {teams[id]}
        </Button>
      ))}

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
        <Button onClick={sendTogglesToBackend}>Send Data</Button>
      </div>
    </div>
  );
}

export {SeasonToggleButtons};