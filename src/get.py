import const 
import json
import requests
from collections import defaultdict
import util,table,const

import logging

from io import BytesIO

from PIL import Image
import cairosvg
import os
import io

class game:
           
    def all_ids():
        '''
        args:
            /
        returns:
            all_ids(List(int)):     List of gameIds for every Team in the NHL
        '''
        all_ids=[]
        for team in const.NHL_TEAMS.values():
            all_ids.extend(game.played_for_all_team(team))
        return all_ids
    
    def played_for_all_team(team):
        '''
        args:
            team(str):          teamAbbrev
        returns:
            id_list(List(int)): 
        '''
        url = f"{const.BASE_URL}club-schedule-season/{team}/20242025"
        content = json.loads(requests.get(url).content)
        id_list = []
        for elem in content['games']:
            id_list.append(elem['id'])
        return id_list
    
    def game_data(game_id:int):
        '''
        args:
            gameId(int):        gameId for the game, from which we want the event Data
        returns:
            result(dict(dict)): dict of the result
        '''
        url=f'https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play'
        content = json.loads(requests.get(url).content)
        result=defaultdict(list)
        result['base']={'id':content.get('id'),'gameType':content['gameType'],'homeTeam':content['homeTeam']['id'],
                                      'awayTeam':content['awayTeam']['id'],'date':content['gameDate'],'venue':f"{content['venue']['default']}"}
        for elem in content.get('rosterSpots'):
            result['players'].append({'id':elem.get('playerId'),'playerName':f"{elem['firstName'].get('default')+' '+elem['lastName'].get('default')}",
                                     'playerPos':elem.get('positionCode'),'headshotPath':elem.get('headshot')})
        for elem in content['plays']:
            match elem['typeDescKey']:
                case 'goal':
                    time=util.fix.time(elem['periodDescriptor'].get('number'),elem['timeInPeriod'])
                    xPos,yPos=util.fix.position(elem['details'].get('xCoord'),elem['details'].get('yCoord'),elem['details'].get('homeTeamDefendingSide'),elem['details'].get('zoneCode'))
                    result['goal'].append({'xPos':xPos,
                                            'yPos':yPos,
                                             'playerId':elem['details'].get('scoringPlayerId'),
                                            'shotType':elem['details'].get('shotType'),
                                            'zoneCode':elem['details'].get('zoneCode'),
                                            'state':util.fix.goal_state(elem,game_id),
                                           'goalie':elem['details'].get('goalieInNetId'),
                                           'eventOwnerTeamId':elem['details'].get('eventOwnerTeamId'),
                                           'eventId':elem['eventId'],'id':game_id,'time':time})
                    continue
                case 'shot-on-goal':
                    time=util.fix.time(elem['periodDescriptor'].get('number'),elem['timeInPeriod'])
                    xPos,yPos=util.fix.position(elem['details'].get('xCoord'),elem['details'].get('yCoord'),elem['details'].get('homeTeamDefendingSide'),elem['details'].get('zoneCode'))
                    result['shot'].append({'xPos':xPos,
                                            'yPos':yPos,
                                            'playerId':elem['details'].get('shootingPlayerId'),
                                            'shotType':elem['details'].get('shotType'),
                                            'zoneCode':elem['details'].get('zoneCode'),
                                            'goalie':elem['details'].get('goalieInNetId'),
                                            'eventOwnerTeamId':elem['details'].get('eventOwnerTeamId'),
                                            'eventId':elem['eventId'],'id':game_id,'time':time})
                    continue
                case 'missed-shot':
                    time=util.fix.time(elem['periodDescriptor'].get('number'),elem['timeInPeriod'])
                    xPos,yPos=util.fix.position(elem['details'].get('xCoord'),elem['details'].get('yCoord'),elem['details'].get('homeTeamDefendingSide'),elem['details'].get('zoneCode'))
                    result['miss'].append({'xPos':xPos,
                                            'yPos':yPos,
                                            'playerId':elem['details'].get('shootingPlayerId'),
                                            'shotType':elem['details'].get('shotType'),
                                            'zoneCode':elem['details'].get('zoneCode'),
                                            'goalie':elem['details'].get('goalieInNetId'),
                                            'reason':elem['details'].get('reason'),
                                            'eventOwnerTeamId':elem['details'].get('eventOwnerTeamId'),
                                            'eventId':elem['eventId'],'id':game_id,'time':time})   
                    #print(result)
                    continue             
                case 'blocked-shot':
                    time=util.fix.time(elem['periodDescriptor'].get('number'),elem['timeInPeriod'])
                    xPos,yPos=util.fix.position(elem['details'].get('xCoord'),elem['details'].get('yCoord'),elem['details'].get('homeTeamDefendingSide'),elem['details'].get('zoneCode'))
                    result['blocked-shot'].append({'xPos':xPos,
                                            'yPos':yPos,
                                            'playerId':elem['details'].get('shootingPlayerId'),
                                            'shotType':elem['details'].get('shotType'),
                                            'zoneCode':elem['details'].get('zoneCode'),
                                            'reason':elem['details'].get('reason'),
                                            'goalie':elem['details'].get('goalieInNetId'),
                                            'blockingPlayerId':elem['details'].get('blockingPlayerId'),
                                            'eventOwnerTeamId':elem['details'].get('eventOwnerTeamId'),
                                            'eventId':elem['eventId'],'id':game_id,'time':time}) 
                    #print(result)
                    continue
                case 'giveaway':
                    time=util.fix.time(elem['periodDescriptor'].get('number'),elem['timeInPeriod'])
                    xPos,yPos=util.fix.position(elem['details'].get('xCoord'),elem['details'].get('yCoord'),elem['details'].get('homeTeamDefendingSide'),elem['details'].get('zoneCode'))
                    result['giveaway'].append({'xPos':xPos,
                                               'yPos':yPos,
                                               'playerId':elem['details'].get('playerId'),
                                               'eventOwnerTeamId':elem['details'].get('eventOwnerTeamId'),
                                               'eventId':elem['eventId'],'id':game_id,'time':time})
                case 'takeaway':
                    time=util.fix.time(elem['periodDescriptor'].get('number'),elem['timeInPeriod'])
                    xPos,yPos=util.fix.position(elem['details'].get('xCoord'),elem['details'].get('yCoord'),elem['details'].get('homeTeamDefendingSide'),elem['details'].get('zoneCode'))
                    result['takeaway'].append({'xPos':xPos,
                                               'yPos':yPos,
                                               'playerId':elem['details'].get('playerId'),
                                               'eventOwnerTeamId':elem['details'].get('eventOwnerTeamId'),
                                               'eventId':elem['eventId'],'id':game_id,'time':time})

                case 'hit':
                    time=util.fix.time(elem['periodDescriptor'].get('number'),elem['timeInPeriod'])
                    xPos,yPos=util.fix.position(elem['details'].get('xCoord'),elem['details'].get('yCoord'),elem['details'].get('homeTeamDefendingSide'),elem['details'].get('zoneCode'))
                    result['hit'].append({'xPos':xPos,'yPos':yPos,
                                          'hittingPlayerId':elem['details'].get('hittingPlayerId'),
                                          'hitteePlayerId':elem['details'].get('hitteePlayerId'),
                                          'eventOwnerTeamId':elem['details'].get('eventOwnerTeamId'),
                                          'eventId':elem['eventId'],'id':game_id,'time':time})
                case _:
                    continue
        return result
    
    
class image:

    def team_img(team_abbrev:str):  
        '''
        args:
            teamAbbrev(str):    teamAbbreviation for which we want the team logo, from svg to png
        returns:
            img:                teamlogo as png
        '''
        path=f'./assets/teams/{team_abbrev}.svg'
        png_data = cairosvg.svg2png(url=path)
    
        return Image.open(BytesIO(png_data))
    

    def headshot(player_id: int):
        '''
        args:
            playerId(int):      PlayerId for who want the headshot
        returns:
            img:                headshot of the player
        '''
        path = f'./assets/headshots/{player_id}.png'
        if not os.path.exists(path):
            url = table.query.headshots(player_id)
            response = requests.get(url).content

            with open(path, 'wb') as file:
                file.write(response)
        image = Image.open(path)
        return image
    
    
    def shotcard(game_id:int):
        '''
        args:
            gameId(int):        gameId for which we want the shotreport
        returns:
            image:              Shotreportcard for the gameId
        '''
        path=f'./assets/shotcards/{game_id}.png'
        with open(path, 'rb') as image_file:
            image = image_file.read()
        return image
    
class player:

    def data(player_id):
        '''
        args:
            playerId(int):      PlayerId for who we ant the name
        returns:
            playerName(str):    playername from the Id
        '''
        return table.query.id_to_name(player_id)

class team:

    def name(teamId,gameId):
        '''
        args:
            teamId(int):        TeamId of the team for which we want the name
            gameId(int):        gameId for the game we dissect
        returns:
            teamname(str):      name of the team fro the teamId
        '''
        url=f"https://api-web.nhle.com/v1/wsc/game-story/{gameId}"
        content = json.loads(requests.get(url).content)
        if content['homeTeam']['id']==teamId:
            return content['homeTeam']['name']['default']
        else: 
            return content['awayTeam']['name']['default']
        
    def abbrev(teamId,gameId):
        '''
        args:
            teamid(int):        teamId, from which we want the abbreviation
            gameId(int):        GameId
        returns
            teamAbbrev(Str):    Team abbreviation of the team with the teamId
        '''
        url=f"https://api-web.nhle.com/v1/wsc/game-story/{gameId}"
        content = json.loads(requests.get(url).content)
        if content['homeTeam']['id']==teamId:
            return content['homeTeam']['abbrev']
        else: 
            return content['awayTeam']['abbrev']
        
