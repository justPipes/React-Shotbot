import logging

NHL_TEAMS = {
        1: 'NJD', 2: 'NYI', 3: 'NYR', 4: 'PHI', 5: 'PIT', 6: 'BOS', 7: 'BUF', 8: 'MTL', 9: 'OTT', 10: 'TOR',
        13: 'FLA', 14: 'TBL', 12: 'CAR', 15: 'WSH', 16: 'CHI', 17: 'DET', 18: 'NSH', 19: 'STL', 20: 'CGY',
        21: 'COL', 22: 'EDM', 23: 'VAN', 24: 'ANA', 25: 'DAL', 26: 'LAK', 28: 'SJS', 29: 'CBJ', 30: 'MIN',
        52: 'WPG', 54: 'VGK', 55: 'SEA', 59: 'UTA'
    }

EVENT_DICT={'Hits':'hits', 'Giveaways':'giveaway', 'Takeaways':'takeaway', 'Goals':'goals', 'Shots':'shots', 'Misses':'miss', 'Blocked shot':'blocks'}
EVENT_COLS={'Hits':'xPos,yPos,hittingPlayerId,hitteePlayerId,eventOwnerTeamId', 'Giveaways':'xPos,yPos,playerId,eventOwnerTeamId', 'Takeaways':'xPos,yPos,playerId,eventOwnerTeamId', 'Goals':'xPos,yPos,playerID,shotType,state,goalie,eventOwnerTeamId', 'Shots':'xPos,yPos,playerID,shotType,goalie,eventOwnerTeamId', 'Misses':'xPos,yPos,playerId,ShotType,goalie,reason,eventOwnerTeamId', 'Blocked shot':'xPos,yPos,playerID,reason,goalie,blockingPlayerId,eventOwnerTeamId'}
BASE_URL = "https://api-web.nhle.com/v1/"

def configure_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='log.txt',
                        filemode='a') 

configure_logging()