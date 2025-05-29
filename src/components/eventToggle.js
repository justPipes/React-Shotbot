import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import React, { useState } from 'react';
import './ToggleButtons.css';

function EventToggles() {
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
export {EventToggles}