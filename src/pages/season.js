import Rink from './assets/rinkdno.png';
import { SeasonToggleButtons } from '../components/teamToggle';


function Season() {
  return (
    <div>
        <p>Choose an event and the teams for which you want the events displayed and press send Data.</p>
        <p>Separted into offensive,neutral and defensive zone from the point-of-view for the acting team.</p>
        <SeasonToggleButtons/>
        <img src={Rink} alt="Logo" />
    </div>
  );
}

export default Season;