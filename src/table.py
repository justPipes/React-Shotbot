import requests
import sqlite3
import json
from collections import defaultdict
#import util as util
import os
from typing import List
import pandas as pd
import const
import logging
import get
from PIL import Image
import const

class make:

    def teams():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor() 
        cursor.execute('''CREATE TABLE IF NOT EXISTS teams(teamId Integer PRIMARY KEY, teamAbbrev Text, teamName Text, teamPlace text, teamVenue text,conference Text, division Text); ''')
        conn.commit()
        conn.close()

    def games():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS games (gameId INTEGER ,gameType INTEGER,homeTeam INTEGER,awayTeam INTEGER,date TEXT,venue TEXT);''')
        conn.commit()
        conn.close()
    
    def players():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS players
                       (playerId INTEGER PRIMARY KEY,playerName TEXT,playerHeight INTEGER,playerWeight INTEGER,birthCity TEXT,birthState Text,birthday text, country Text, playerPos TEXT,playerTeam TEXT,headshotPath TEXT);''')
        conn.commit()
        conn.close()

    def goals():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS goals(
                       gameId INTEGER,xPos INTEGER, yPOS INTEGER, playerId INTEGER,shotType TEXT,zoneCode TEXT,state TEXT, goalie INTEGER, eventOwnerTeamId INTEGER,eventId Integer,time Float); ''')
        conn.commit()
        conn.close()

    def miss():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS miss(
                       gameId INTEGER,xPos INTEGER, yPOS INTEGER, playerId INTEGER,shotType TEXT,zoneCode TEXT,goalie INTEGER, eventOwnerTeamId INTEGER,reason TEXT,eventId Integer,time Float); ''')
        conn.commit()
        conn.close()

    def shots():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS shots(
                       gameId INTEGER,xPos INTEGER, yPOS INTEGER, playerId INTEGER,shotType TEXT,zoneCode TEXT,goalie INTEGER,reason TEXT, eventOwnerTeamId INTEGER,eventId Integer,time Float); ''')
        conn.commit()
        conn.close()

    def blocks():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS blocks(
                       gameId INTEGER,xPos INTEGER, yPOS INTEGER, playerId INTEGER,shotType TEXT,zoneCode TEXT,reason TEXT,goalie INTEGER,blockingPlayerId INTEGER, eventOwnerTeamId INTEGER,eventId Integer,time Float); ''')
        conn.commit()
        conn.close()

    def hits():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE hits(
                       gameId INTEGER,xPos INTEGER,yPos INTEGER,hittingPlayerId INTEGER, hitteePlayerId INTEGER,eventOwnerTeamId INTEGER,eventId INTEGER,time float,zoneCode TEXT);''')
        conn.commit()
        conn.close()

    def takeaways():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE takeaway(
                       gameId INTEGER,xPos INTEGER,yPos INTEGER,playerId INTEGER,eventOwnerTeamId INTEGER,eventId INTEGER,zoneCode TEXT,time float);''')
        conn.commit()
        conn.close()

    def giveaways():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE giveaway(
                       gameId INTEGER,xPos INTEGER,yPos INTEGER,playerId INTEGER,eventOwnerTeamId INTEGER,eventId INTEGER,zoneCode TEXT,time float);''')
        conn.commit()
        conn.close()

    def shotcards():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS shotcards(gameId INTEGER,imgFilepath TEXT);''')
        conn.commit()
        conn.close()
    
    def faceoff():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS faceoff(gameId INTEGER,eventOwnerTeamId Integer, winningPlayerId Integer, loosingPlayerId Integer,xPos Integer,yPos Integer,time Float,eventId Integer,zoneCode TEXT);''')
        conn.commit()
        conn.close()
    
    def penalty():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS penalty(gameId INTEGER,eventOwnerTeamId Integer, commitedByPlayerId Integer, drawingPlayerId Integer,xPos Integer,yPos Integer,type Text, descKey Text, duration Integer,time Float,eventId Integer,zoneCode TEXT);''')
        conn.commit()
        conn.close()
    
    def stoppage():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS stoppage(gameId INTEGER,reason Text,time Float,eventId Integer,zoneCode TEXT);''')
        conn.commit()
        conn.close() 


class fill:
        
    def games(data):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        cursor.execute('''INSERT INTO games (gameId,gameType,homeTeam, awayTeam,date,venue) VALUES(?,?,?,?,?,?)''',
            (data.get('id'),data.get('gameType'),data.get('homeTeam'),data.get('awayTeam'),data.get('date'),data.get('venue')))
        conn.commit()
        conn.close()
    
    def goals(d):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        for entry in d:
            cursor.execute('''INSERT INTO goals (gameId,xPos,yPos,playerId,shotType,zonecode,goalie,state,eventOwnerTeamId,eventId,time) VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
                        (entry.get("id"),entry.get('xPos'),entry.get('yPos'),entry.get('playerId'),entry.get('shotType'),
                         entry.get('zoneCode'),entry.get('goalie'),entry.get('state'),entry.get('eventOwnerTeamId'),entry.get('eventId'),entry.get('time')))
            logging.info(f'Goals filled for game {entry.get("id")}')
        conn.commit()
        conn.close()


    def shots(d):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        for entry in d:
            cursor.execute('''INSERT INTO shots (gameId,xPos,yPos,playerId,shotType,zonecode,goalie,eventOwnerTeamId,eventId,time) VALUES(?,?,?,?,?,?,?,?,?,?)''',
                        (entry.get("id"),entry.get('xPos'),entry.get('yPos'),entry.get('playerId'),entry.get('shotType'),entry.get('zoneCode'),entry.get('goalie'),entry.get('eventOwnerTeamId'),entry.get('eventId'),entry.get('time')))
            logging.info(f'Shots filled for game {entry.get("id")}')
        conn.commit()
        conn.close()


    def miss(d):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        for entry in d:
            cursor.execute('''INSERT INTO miss (gameId,xPos,yPos,playerId,shotType,zonecode,goalie,reason,eventOwnerTeamId,eventId,time) VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
                        (entry.get("id"),entry.get('xPos'),entry.get('yPos'),entry.get('playerId'),entry.get('shotType'),entry.get('zoneCode'),entry.get('goalie'),entry.get('reason'),entry.get('eventOwnerTeamId'),entry.get('eventId'),entry.get('time')))
            logging.info(f'Misses filled for game {entry.get("id")}')
        conn.commit()
        conn.close()
      
    def blocks(d):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        for entry in d:
            cursor.execute('''INSERT INTO blocks(gameId,xPos,yPos,playerId,shotType,zonecode,goalie,reason,blockingPlayerId,eventOwnerTeamId,eventId,time) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''',
                        (entry.get("id"),entry.get('xPos'),entry.get('yPos'),entry.get('playerId'),entry.get('shotType'),entry.get('zoneCode'),entry.get('goalie'),entry.get('reason'),entry.get('blockingPlayerId'),entry.get('eventOwnerTeamId'),entry.get('eventId'),entry.get('time')))
            logging.info(f'Blocks filled for game {entry.get("id")}')
        conn.commit()
        conn.close()

    def hits(d):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        for entry in d:
            cursor.execute('''INSERT INTO hits(gameId,xPos,yPos,hittingPlayerId,hitteePlayerId,eventOwnerTeamId,eventId,time) 
                           VALUES(?,?,?,?,?,?,?,?)''',
                        (entry.get("id"),entry.get('xPos'),entry.get('yPos'),entry.get('hittingPlayerId'),entry.get('hitteePlayerId'),entry.get('eventOwnerTeamId'),entry.get('eventId'),entry.get('time')))
            logging.info(f'hits filled for game {entry.get("id")}')
        conn.commit()
        conn.close()

    def takeaways(d):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        for entry in d:
            cursor.execute('''INSERT INTO takeaway(gameId,xPos,yPos,playerId,eventOwnerTeamId,eventId,time) 
                           VALUES(?,?,?,?,?,?,?)''',
                        (entry.get("id"),entry.get('xPos'),entry.get('yPos'),entry.get('playerId'),entry.get('eventOwnerTeamId'),entry.get('eventId'),entry.get('time')))
            logging.info(f'takeaways filled for game {entry.get("id")}')
        conn.commit()
        conn.close()


    def giveaways(d):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        for entry in d:
            cursor.execute('''INSERT INTO giveaway(gameId,xPos,yPos,playerId,eventOwnerTeamId,eventId,time) 
                           VALUES(?,?,?,?,?,?,?)''',
                        (entry.get("id"),entry.get('xPos'),entry.get('yPos'),entry.get('playerId'),entry.get('eventOwnerTeamId'),entry.get('eventId'),entry.get('time')))
            logging.info(f'Giveaways filled for game {entry.get("id")}')
        conn.commit()
        conn.close()
    
    def players(data):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        for entry in data:
            cursor.execute('''INSERT OR IGNORE INTO players(playerId,playerName,playerPos,headshotpath) 
                           VALUES(?,?,?,?)''',
                        (entry.get("id"),entry.get('playerName'),entry.get('playerPos'),entry.get('headshotPath')))
            logging.info(f'Players filled for game {entry.get("id")}')
        conn.commit()
        conn.close()
    
    def teams():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        for key in const.NHL_TEAMS.keys():
            url=f'https://api.nhle.com/stats/rest/en/team/id/{key}'
            content = json.loads(requests.get(url).content)
            cursor.execute('''INSERT OR IGNORE INTO teams(teamId,teamAbbrev,teamName) 
                           VALUES(?,?,?)''',
                        (content['data'][0]['id'],
                         content['data'][0]['triCode'],
                         content['data'][0]['fullName']
                        ))
        conn.commit()
        conn.close()

    def all(data):
        logging.info(data)
        fill.games(data['base'])
        fill.blocks(data['blocked-shot'])
        fill.goals(data['goal'])
        fill.miss(data['miss'])
        fill.hits(data['hit'])
        fill.shots(data['shot'])
        fill.takeaways(data['takeaway'])
        fill.giveaways(data['giveaway'])
        fill.teams()

class query:
    
    def team_data(team_id):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        req=cursor.execute('''SELECT teamAbbrev,teamName from teams where teamdId=?''',(team_id,)).fetchall()
        conn.commit()
        conn.close()
        return req
    
    def id_to_name(player_id):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        req=cursor.execute('''SELECT playerName from players where playerId=?''',(player_id,)).fetchone()[0]
        conn.commit()
        conn.close()
        name=req[0]+". "+req.split(" ")[1]
        return name

    def player_list():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        req=cursor.execute('''SELECT playerId from players Order by playerId)''').fetchall()
        conn.commit()
        conn.close()
        return req

    def headshots(player_id):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        req=cursor.execute('''SELECT headshotPath from players where playerId=?''',(player_id,)).fetchall()
        conn.commit()
        conn.close()
        return req[0][0]
    
    def team_logos(team_id):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        req=cursor.execute('''SELECT teamAbbrev from teams where teamId=?''',(team_id,)).fetchall()
        conn.commit()
        conn.close()
        return req

    
    def gameIds():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        req=cursor.execute('''SELECT gameId from games Order by gameId''').fetchall()
        conn.commit()
        conn.close()
        return req
    
    def gameIdsReg():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        req=cursor.execute('''SELECT gameId FROM games where gameType=2 or gameType=3 Order by gameId''').fetchall()
        conn.commit()
        conn.close()
        return req

    def shotCardParams():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        req=cursor.execute('''SELECT homeTeam,awayTeam,gameId from games Order by gameId''').fetchall()
        conn.commit()
        conn.close()
        return req
    
    def shotCardParamsReg():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        req=cursor.execute('''SELECT homeTeam,awayTeam,gameId from games where gameType=2 or gameType=3 Order by gameId ''').fetchall()
        conn.commit()
        conn.close()
        return req

    
    def singleCardParams(homeTeamId,awayTeamId,game_id):

        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        homeTeam=get.team.name(homeTeamId,game_id)
        homeTeamAbbrev=get.team.abbrev(homeTeamId,game_id)
        awayTeam=get.team.name(awayTeamId,game_id)
        awayTeamAbbrev=get.team.abbrev(awayTeamId,game_id)
        venue=cursor.execute('''SELECT venue from games where gameId=?''',(game_id,)).fetchone()[0]
        date=cursor.execute('''SELECT date from games where gameId=?''',(game_id,)).fetchone()[0]
        conn.commit()
        conn.close()
        return {'homeTeam':homeTeam ,'homeTeamId':homeTeamId,'homeTeamAbbrev':homeTeamAbbrev,
                'awayTeam':awayTeam,'awayTeamId':awayTeamId,'awayTeamAbbrev':awayTeamAbbrev,
                'venue':venue,'date':date,'gameId':game_id}

    def getGamesForTeam(team_id:int):
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        req=cursor.execute('''SELECT gameId from games where homeTeam=? or awayTeam=?''',(team_id,team_id,)).fetchall()
        conn.commit()
        conn.close()
        return req
    
    def cardData(team,event):
        queryList=[]
        req={}
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        match event:
            case 'Hits':
                query=f'SELECT xPos,yPos,hittingPlayerId,hitteePlayerId,eventOwnerTeamId from hits where eventOwnerTeamId = {team}'                    
                queryList.append(query)
            case 'Giveaways':
                query=f'SELECT xPos,yPos,playerId,eventOwnerTeamId from giveaway where eventOwnerTeamId ={team}'
                queryList.append(query)
            case 'Takeaways':
                query=f'SELECT xPos,yPos,playerId,eventOwnerTeamId from takeaway where eventOwnerTeamId ={team}'
                queryList.append(query)
            case 'Goals':
                query=f'SELECT xPos,yPos,playerId,shotType,state,goalie,eventOwnerTeamId from goals where eventOwnerTeamId ={team}'
                queryList.append(query)
            case 'Shots':
                query=f'SELECT xPos,yPos,playerId,shotType,goalie,shotType,eventOwnerTeamId from shots where eventOwnerTeamId ={team}'
                queryList.append(query)
            case 'Misses':
                query=f'SELECT xPos,yPos,playerId,shotType,goalie,reason,eventOwnerTeamId from miss where eventOwnerTeamId ={team}'
                queryList.append(query)
            case 'Blocked shot':
                query=f'SELECT xPos,yPos,playerId,reason,goalie,blockingPlayerId,eventOwnerTeamId from blocks where eventOwnerTeamId = {team}'
                queryList.append(query)
        req.update({f'{event}':cursor.execute(query).fetchall()})
        conn.close()
        return req
    
class update:

    def players():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        req=cursor.execute('''SELECT playerId from players Order by playerId''').fetchall()  
        for (player_id,) in req:
            
            url = f'https://api-web.nhle.com/v1/player/{player_id}/landing'
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch data for playerId {player_id}")
                continue
            content = response.json()
            weight = content.get('weightInKilograms')
            height = content.get('heightInCentimeters')
            city = content.get('birthCity').get('default') if content.get('birthCity') and content.get('birthCity').get('default') else content.get('birthCity') if content.get('birthCity') else None            
            country = content.get('birthCountry')
            state= content.get('birthStateProvince').get('default') if content.get('birthStateProvince') and content.get('birthStateProvince').get('default') else content.get('birthStateProvince') if content.get('birthStateProvince') else None
            birthday = content.get('birthDate')
            position = content.get('position')
            team = content.get('currentTeamAbbrev')
            headshot = content.get('headshot')
            cursor.execute('''
                UPDATE players
                SET playerHeight = ?, 
                    playerWeight = ?, 
                    birthCity = ?, 
                    birthState = ?, 
                    birthday = ?, 
                    country = ?, 
                    playerPos = ?, 
                    playerTeam = ?, 
                    headshotPath = ?
                WHERE playerId = ?
                ''', (height, weight, city, state, birthday, country, position, team, headshot, player_id))
            conn.commit()
        conn.close()