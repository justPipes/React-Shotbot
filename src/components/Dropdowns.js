import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { Link } from 'react-router-dom';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import React from 'react';
import { handleClick } from './utils';

const NHL_TEAMS = {
  1: 'NJD', 2: 'NYI', 3: 'NYR', 4: 'PHI', 5: 'PIT', 6: 'BOS', 7: 'BUF', 8: 'MTL', 9: 'OTT', 10: 'TOR',
  13: 'FLA', 14: 'TBL', 12: 'CAR', 15: 'WSH', 16: 'CHI', 17: 'DET', 18: 'NSH', 19: 'STL', 20: 'CGY',
  21: 'COL', 22: 'EDM', 23: 'VAN', 24: 'ANA', 25: 'DAL', 26: 'LAK', 28: 'SJS', 29: 'CBJ', 30: 'MIN',
  52: 'WPG', 54: 'VGK', 55: 'SEA', 59: 'UTA'
};

function MainDropdown() {
  return (
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand as={Link} to="/">Shotbot</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="main-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Home</Nav.Link>
            <Nav.Link as={Link} to="/faq">FAQ</Nav.Link>
            <Nav.Link as={Link} to="/season">season</Nav.Link>
            <Nav.Link as={Link} to="shotcard">Shotreports</Nav.Link>
            <NavDropdown title="Players" id="player-dropdown">
              <NavDropdown.Item as={Link} to="/players/skaters">Skaters</NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/players/goalies">Goalies</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

function SeasonDropdown() {
  return (
    <DropdownButton id="dropdown-item-button" title="Seasontype">
      Season Type
      <Dropdown.Menu>
      <Dropdown.Item as="button" onClick={()=>handleClick('season_param', 'RegularSeason')}>
        RegularSeason
        </Dropdown.Item>
      <Dropdown.Item as="button" onClick={()=>handleClick('season_param', 'StanleyCup')}>
        Stanley Cup</Dropdown.Item>
      <Dropdown.Item as="button" onClick={()=>handleClick('season_param','Overall')}>
        Overall</Dropdown.Item>
      </Dropdown.Menu>
      </DropdownButton>
    );
}

function TeamDropdown() {
  return (
    <DropdownButton id="dropdown-item-button" title="Teams">
      <Dropdown.ItemText>Choose a Team</Dropdown.ItemText>
      {Object.entries(NHL_TEAMS).map(([id, team]) => (
        <Dropdown.Item key={id} as="button" onClick={() => handleClick(Number(id))}>
          {team}
        </Dropdown.Item>
      ))}
      <Dropdown.Item as="button" onClick={() => handleClick(0)}>All of them</Dropdown.Item>
    </DropdownButton>
  );
};
  

function EventDropdown() {
return (
  <DropdownButton id="dropdown-item-button" title="Events">
    <Dropdown.ItemText>Choose a Eventtype</Dropdown.ItemText>
    <Dropdown.Item as="button" onClick={()=>handleClick('event_param','hits')}>Hits</Dropdown.Item>
    <Dropdown.Item as="button" onClick={()=>handleClick('event_param','giveaway')}>Giveaways</Dropdown.Item>
    <Dropdown.Item as="button" onClick={()=>handleClick('event_param','takeaways')}>Takeaways</Dropdown.Item>
  </DropdownButton>
);
} 

function ShotCardTeamDropdown({ onTeamSelect }) {
  const handleTeamSelect = async (teamId) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/shotcard?team_id=${teamId}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });

      const data = await response.json();
      console.log('Response from backend:', data);

      if (onTeamSelect && data.images) {
        onTeamSelect(data.images);
      }
    } catch (error) {
      console.error('Error fetching shotcard data:', error);
    }
  };

return (
    <DropdownButton id="dropdown-item-button" title="Teams">
      <Dropdown.ItemText>Choose a Team</Dropdown.ItemText>
      {Object.entries(NHL_TEAMS).map(([id, team]) => (
        <Dropdown.Item key={id} as="button" onClick={() => handleTeamSelect(Number(id))}>
          {team}
        </Dropdown.Item>
      ))}
      <Dropdown.Item as="button" onClick={() => handleTeamSelect(0)}>All of them</Dropdown.Item>
    </DropdownButton>
  );
};

export {ShotCardTeamDropdown,MainDropdown,SeasonDropdown,TeamDropdown,EventDropdown};

