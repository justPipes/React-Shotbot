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



function EventButtons() {
  const labels = ['Hits', 'Giveaways', 'Takeaways','Goals', 'Shots', 'Misses','Blocked shot'];
  const [toggles, setToggles] = useState(new Array(labels.length).fill(false));

  const handleToggle = (index) => {
    setToggles((prev) => {
      const updated = [...prev];
      updated[index] = !updated[index];
      return updated;
    });
  };

  return (
    <div className="toggle-sect">
    <ButtonGroup className="slim-toggle-group">
      {labels.map((label, index) => (
        <Button
          key={index}
          variant={toggles[index] ? 'secondary' : 'outline-secondary'}
          onClick={() => handleToggle(index)}
        >
          {label}
        </Button>
      ))}
    </ButtonGroup>
    </div>
  );
}
/*


function GoalieButtons() {
    return (
      <ButtonGroup aria-label="Basic example">
        <Button variant="secondary">Shots faced</Button>
        <Button variant="secondary">Goals against</Button>
        <Button variant="secondary">Catches</Button>
        <Button variant="secondary">Rebounds from Shots</Button>
        <Button variant="secondary">Misses</Button>
      </ButtonGroup>
    );
  }

function NameDropdown() {
  const [players] = useState([]);
  const [search, setSearch] = useState('');

 // useEffect(() => {
    // Fetch data from the API
   // fetch('http://localhost:5000/api/teams')
    //  .then(res => res.json())
   //   .then(data => setPlayers(data))
  //    .catch(error => console.error('Error fetching data:', error));
  //}, []);

  const filteredPlayers = players.filter(player =>
    player.name.toLowerCase().includes(search.toLowerCase())
  );

  const handleClick = (playerName) => {
    console.log('Selected Player:', playerName);
    // You can set state or trigger other logic here
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search Player..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      <ul>
        {filteredPlayers.map(player => (
          <li key={player.name}>
            <button onClick={() => handleClick(player.name)}>
              {player.name}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}


*/


export {EventButtons,TeamToggleBttns};