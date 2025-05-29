import table
import get
import logging
import const
import requests
import shotcard

class db:
    def make_all():
        table.make.games()
        table.make.teams()
        table.make.players()
        table.make.goals()
        table.make.shots()
        table.make.miss()
        table.make.blocks()
        table.make.giveaways()
        table.make.hits()
        table.make.takeaways()
        table.make.shotcards()

    def fill_all(data):
        table.fill.games(data['base'])
        table.fill.blocks(data['blocked-shot'])
        table.fill.goals(data['goal'])
        table.fill.miss(data['miss'])
        table.fill.hits(data['hit'])
        table.fill.shots(data['shot'])
        table.fill.takeaways(data['takeaway'])
        table.fill.giveaways(data['giveaway'])
        table.fill.players(data['players'])
    
    def init():
        all=set(get.game.all_ids())
        result=[]
        db.make_all()
        for game_id in all:
            result=get.game.game_data(game_id)
            db.fill_all(result)
            logging.info(f'Game {game_id} done')
        table.update.players()
        table.update.teams()
        return None 
    
    def update():
        # ToDo
        # Updating existing entries such as: 
        # If no goalie is in goal during a goal score, the goal state entry should be changed to eng for empty net goal
        return None
class img:

    def logos():
        for val in const.NHL_TEAMS.values():
            try:
                url=f'https://assets.nhle.com/logos/nhl/svg/{val}_light.svg'
                response = requests.get(url)
                response.raise_for_status()
                path=f'./assets/teams/{val}.svg'
                with open(path, 'wb') as file:
                    file.write(response.content)
            except requests.exceptions.RequestException as e:   
                logging.error(f'Logo for {val} not found, {e}')   
     
    def headshots():
        for url in table.query.headshots():
            try:
                response = requests.get(url)
                response.raise_for_status()
                path=f'./assets/headshots/{url[-11:-4]}'
                with open(path, 'wb') as file:
                    file.write(response.content)
            except requests.exceptions.RequestException as e:   
                logging.error(f'headshot for {url[-11:-4]} not found, {e}') 


class main:

    def all():
        db.init()
        img.logos()
        img.headshots()
        shotcard.plot.init()
        
