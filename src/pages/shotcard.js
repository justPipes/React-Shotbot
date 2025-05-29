import { useState } from "react";
import { ShotCardTeamDropdown } from "../components/Dropdowns";
import { CardDisplay } from "../components/CardDisplay";

function Shotcards() {
  const [imagePaths, setImagePaths] = useState([]);

  const handleTeamSelect = (paths) => {
    setImagePaths(paths);
  };

  return (
    <>
      <div className="mb-3">
        Shotbot was created to create shotreports. Choose a team and take a look at the cards.
      </div>

      <div className="mb-4">
        <ShotCardTeamDropdown onTeamSelect={handleTeamSelect} />
      </div>

      <CardDisplay images={imagePaths} />
    </>
  );
}

export { Shotcards };