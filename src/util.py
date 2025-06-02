import json
import requests
import logging
from typing import Dict

class fix:

    def position(x_pos: int, y_pos: int,side: str,zone:chr):
        '''
        Change xPos,yPos so both teams get one side of the ice 
        in respect to playing direction.
        args:
            side    side of the homeDefendingSide
            x_pos   Position of the player on the x-axis
            y_pos   Position of the player on the y-axis
            zone    The zone Code
        returns
            x_pos,y_pos as transformed values
        '''
        logging.info(f'Attempting to fix positions {x_pos},{y_pos}')
        match side:
            case 'left':
                x_pos,y_pos=-x_pos,-y_pos
        match zone:
            case 'D':
               if x_pos>-25:
                    x_pos,y_pos=-x_pos,-y_pos
            case 'N':
              if side=='left':
                x_pos,y_pos=-x_pos,-y_pos
            case 'O':
                if x_pos<25:
                    x_pos,y_pos=-x_pos,-y_pos
        return x_pos,y_pos
  

    def goal_state(entry,game_id):
        '''
        Get the the path of movement from goals scored for all players on ice
        Unless it was a shootout goal
        '''
        if entry['periodDescriptor']['periodType']=='SO':
            state='SO'
        else:
            event_id=entry['eventId']
            content=json.loads(requests.get(f"https://api-web.nhle.com/v1/ppt-replay/{game_id}/{event_id}").content)
            state=content['goal']['strength']
        return state

    def time(period: int, time: str) -> float:
        '''
        transform time from string to a float while adapting to the periods
        args:
            period
            time 
        return:
            time as a float
        '''
        t=str((period-1)*2 + int(time[:1]))+time[1:]
        mins,secs=t.split(":")
        logging.info(f'Fixed time for {period},{time}')
        return int(mins)+(int(secs)/60)    
    
    def max_val(d1: Dict[str, Dict[str, int]], d2: Dict[str, Dict[str, int]]) -> int:     
        '''
        Getting the max val of 2 dicts
        args:
            d1,d2 Input dicts
        returns:
            int: the max Value from the dicts
        '''
        return max(max([sum(x.values()) for x in d1.values()]), max([sum(x.values()) for x in d2.values()]))

    def configure_plot(ax,title:str, extent:list) -> None:
        '''
        configure the axis for the kde Plot
        '''
        ax.set_title(title)
        ax.set_xlim(extent[0], extent[1])
        ax.set_ylim(extent[2], extent[3])
        ax.tick_params(axis='both', which='both', length=0, labelsize=0)
        ax.set_xlabel("")
        ax.set_ylabel("")
        logging.info('Configured plot')
