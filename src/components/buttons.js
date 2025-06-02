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


export {EventButtons,TeamToggleBttns};