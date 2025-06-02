import logging
import sqlite3
import json
from typing import List, Tuple,Dict,Union,DefaultDict
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
import seaborn as sns
import util,table,get



class fetch:

    def kdePlot(teamId:int,gameId:str)->List[Tuple[int,int]]:
        '''
        Contains query for the KDE plots which calculate the density of shotpositions
        on the ice for a team.
        '''
        conn = sqlite3.connect('./main.db')
        cursor = conn.cursor()
        query=f'SELECT xPos,yPos FROM shots where eventOwnerTeamId={teamId} and gameId={gameId} UNION ALL SELECT xPos,yPos FROM miss WHERE eventOwnerTeamId={teamId} and gameId={gameId} UNION ALL SELECT xPos,yPos FROM goals WHERE eventOwnerTeamId={teamId} and gameId={gameId};'
        content = cursor.execute(query).fetchall()
        conn.close()
        logging.info(f'Fetched KDE data for {gameId} for team {teamId} from database')
        return content
    
    def tablePlot(teamId: int, gameId: str) -> List[Tuple[int, str]]:
        '''
        Contains query for the table with numbers for a team:
        goals, misses, hits on the post/crossbar, shots blocked by opponent or teammate.
        '''
        conn = sqlite3.connect('./main.db')
        cursor = conn.cursor()
        try:
            query = '''
            SELECT COUNT(*), 'On goal' AS reason FROM shots WHERE eventOwnerTeamId = ? AND gameId = ?
            UNION ALL SELECT COUNT(*), 'Goal' AS reason FROM goals WHERE eventOwnerTeamId = ? AND gameId = ?
            UNION ALL SELECT COUNT(*), 'miss' AS reason FROM miss WHERE eventOwnerTeamId = ? AND gameId = ? AND reason NOT LIKE '%post%' AND reason != 'hit-crossbar'
            UNION ALL SELECT COUNT(*), 'metal' AS reason FROM miss WHERE eventOwnerTeamId = ? AND gameId = ? AND (reason LIKE '%post%' OR reason = 'hit-crossbar')
            UNION ALL SELECT COUNT(*), 'OppBlock' AS reason FROM blocks WHERE eventOwnerTeamId = ? AND gameId = ? AND reason = 'blocked'
            UNION ALL SELECT COUNT(*), 'TeamBlock' AS reason FROM blocks WHERE eventOwnerTeamId = ? AND gameId = ? AND reason != 'blocked';
            '''
            c = cursor.execute(query, (teamId, gameId, teamId, gameId, teamId, gameId, teamId, gameId, teamId, gameId, teamId, gameId)).fetchall()
            logging.info(f'Fetched table data for {gameId} for team {teamId} from database')
        except sqlite3.Error as e:
            logging.error(f'Database error: {e}')
            c = []
        finally:
            conn.close()
        return c
    
    def shotTypePlot(teamId: int, gameId: str) -> List[Tuple[str, int]]:
        '''
        Contains query for the plot of different shot types (wrist shot, slap shot, etc.) for a team.
        '''
        conn = sqlite3.connect('./main.db')
        cursor = conn.cursor()
        try:
            query = f'''
            SELECT shotType, COUNT(shotType)
            FROM (
                SELECT shotType FROM miss WHERE eventOwnerTeamId = ? AND gameId = ?
                UNION ALL SELECT shotType FROM shots WHERE eventOwnerTeamId = ? AND gameId = ?
                UNION ALL SELECT shotType FROM goals WHERE eventOwnerTeamId = ? AND gameId = ?
            )
            GROUP BY shotType
            ORDER BY shotType;
        '''
            c = cursor.execute(query, (teamId, gameId, teamId, gameId, teamId, gameId)).fetchall()
            logging.info(f'Fetched shotType data for {gameId} for team {teamId} from database')
        except sqlite3.Error as e:
            logging.error(f'Database error: {e}')
            c = []
        finally:
            conn.close()
        return c
    
    def targetByPeriod(teamId: int, gameId: str) -> List[Tuple[int, str, str]]:
        '''
        Contains query which returns the different targets of shots grouped by period of the game for a team.
        Only for regular game time, no OT implemented yet.
        '''
        conn = sqlite3.connect('./main.db')
        cursor = conn.cursor()
        try:
            query = f'''
            SELECT
                COUNT(*),
                CASE
                    WHEN time > 0 AND time <= 20 THEN 'P1'
                    WHEN time > 20 AND time <= 40 THEN 'P2'
                    WHEN time > 40 AND time <= 60 THEN 'P3'
                END AS time_range,
                reason
            FROM (
                SELECT time, 'on goal' AS reason FROM shots WHERE eventOwnerTeamId = ? AND gameId = ?
                UNION ALL
                SELECT time, 'goal' AS reason FROM goals WHERE eventOwnerTeamId = ? AND gameId = ?
                UNION ALL
                SELECT time, 'miss' AS reason FROM miss WHERE eventOwnerTeamId = ? AND gameId = ? AND reason NOT LIKE '%post%' AND reason != 'hit-crossbar'
                UNION ALL
                SELECT time, 'metal' AS reason FROM miss WHERE eventOwnerTeamId = ? AND gameId = ? AND (reason LIKE '%post%' OR reason = 'hit-crossbar')
                UNION ALL
                SELECT time, 'blocked' AS reason FROM blocks WHERE eventOwnerTeamId = ? AND gameId = ? AND reason = 'blocked'
                UNION ALL
                SELECT time, 'teammate-blocked' AS reason FROM blocks WHERE eventOwnerTeamId = ? AND gameId = ? AND reason != 'blocked'
            ) AS data
            WHERE time > 0 AND time <= 60
            GROUP BY time_range, reason;
            '''
            c = cursor.execute(query, (teamId, gameId, teamId, gameId, teamId, gameId, teamId, gameId, teamId, gameId, teamId, gameId)).fetchall()
            logging.info(f'Fetched shot data by period for {gameId} for team {teamId} from database')
        except sqlite3.Error as e:
            logging.error(f'Database error: {e}')
            c = []
        finally:
            conn.close()
        return c
    
    def targetByShooter(teamId: int, gameId: str) -> List[Tuple[int, str, int]]:
        '''
        Contains query that looks up the different shot targets (miss, goal, on goal, etc.)
        for each shooter of a team. Currently limited to the top 4 shooters.
        '''
        conn = sqlite3.connect('./main.db')
        cursor = conn.cursor()
        try:
            query = f'''
            WITH reason_counts AS (
                SELECT playerId, reason, COUNT(reason) AS reasonCount
                FROM (
                    SELECT playerId, time, 'on goal' AS reason
                    FROM shots
                    WHERE eventOwnerTeamId = ? AND gameId = ?
                    UNION ALL
                    SELECT playerId, time, 'goal' AS reason
                    FROM goals
                    WHERE eventOwnerTeamId = ? AND gameId = ?
                    UNION ALL
                    SELECT playerId, time,
                        CASE
                            WHEN reason IN ('hit-crossbar', 'hit-post') THEN 'metal'
                            ELSE 'miss'
                        END AS reason
                    FROM miss
                    WHERE eventOwnerTeamId = ? AND gameId = ?
                    UNION ALL
                    SELECT playerId, time, reason
                    FROM blocks
                    WHERE eventOwnerTeamId = ? AND gameId = ?
                ) AS combined_results
                GROUP BY playerId, reason
            ), shooter_totals AS (
                SELECT rc.playerId, SUM(rc.reasonCount) AS totalReasonCount
                FROM reason_counts rc
                GROUP BY rc.playerId
            ), ranked_shooters AS (
                SELECT rc.playerId, rc.reason, rc.reasonCount,
                    ROW_NUMBER() OVER (PARTITION BY rc.playerId ORDER BY rc.reasonCount DESC) AS reasonRank,
                    st.totalReasonCount,
                    DENSE_RANK() OVER (ORDER BY st.totalReasonCount DESC) AS shooterRank
                FROM reason_counts rc
                JOIN shooter_totals st ON rc.playerId = st.playerId
            ), top_shooters AS (
                SELECT playerId
                FROM ranked_shooters
                GROUP BY playerId
                ORDER BY MIN(shooterRank)
                LIMIT 4
            )
            SELECT rs.playerId, rs.reason, rs.reasonCount
            FROM ranked_shooters rs
            JOIN top_shooters ts ON rs.playerId = ts.playerId
            ORDER BY rs.totalReasonCount DESC, rs.playerId, rs.reasonRank;
            '''
            c = cursor.execute(query, (teamId, gameId, teamId, gameId, teamId, gameId, teamId, gameId)).fetchall()
            logging.info(f'Fetched target by shooter data for {gameId} for team {teamId} from database')
        except sqlite3.Error as e:
            logging.error(f'Database error: {e}')
            c = []
        finally:
            conn.close()
        return c
    
class prepare:
    '''
    Preparing the params from the shotcard.get class
    
    '''

    def params(game_id:int):
        return table.query.singleCardParams(game_id)
    
    def kde(id_home: int, id_away: int, gameId: int) -> Dict[str, pd.DataFrame]:
        '''
        Kernel Density Estimation of the list of shotpositions for each team
        args:
            id_home(int):       team Id of the home Team
            id_away(int):       team Id of the away Team
            gameId(int):        the Id of the game
        returns   
            dict:           the result of the KDE 
        '''
        positions_home=fetch.kdePlot(id_home,gameId)
        positions_away=fetch.kdePlot(id_away,gameId)
        data_home=pd.DataFrame({'xPos':[-x[0] for x in positions_home],'yPos':[x[1] for x in positions_home],'team': f'{id_home}'})
        data_away=pd.DataFrame({'xPos':[x[0] for x in positions_away],'yPos':[x[1] for x in positions_away],'team': f'{id_away}'})
        combined_data = pd.concat([data_home, data_away])
        return {'data_home':data_home,'data_away':data_away,'combined_data':combined_data}

    def shooters_by_area(id_home: int, id_away: int, gameId: int) -> Dict[str, DefaultDict[str, Dict[str, int]]]:
        '''
            Reordering the list of target counts by players as a dict

            args:
                id_home(int):       team Id of the home Team
                id_away(int):       team Id of the away Team
                gameId(int):        the Id of the game
            returns
                d_home(dict):       the players, their shot targets and 
                                    associated counts as a dict for the home team
                d_away(dict):       the players, their shot targets and 
                                    associated counts as a dict for the away team
        '''
        d_home= defaultdict(lambda:defaultdict(int))
        d_away= defaultdict(lambda:defaultdict(int))
        for (player,reason,count) in fetch.targetByShooter(id_home,gameId):
            d_home[player][reason]+=count
        for (player,reason,count) in fetch.targetByShooter(id_away,gameId):
            d_away[player][reason]+=count
        return {'d_home':d_home,'d_away':d_away}


    def shot_types(id_home: int, id_away: int, gameId: int) -> Dict[str, Union[int, List[Tuple[str, int]]]]:
        '''
        args:
            id_home(int):      team Id of the home Team
            id_away(int):      team Id of the away Team
            gameId(int):    the Id of the game
        returns
            dict:           different shot types and sum of shots per team as a dict
        '''
        shot_types_home=fetch.shotTypePlot(id_home,gameId)
        shot_types_away=fetch.shotTypePlot(id_away,gameId)
        shot_sums_home=sum([x[1] for x in shot_types_home])
        shot_sums_away=sum([x[1] for x in shot_types_away])
        return {'shot_sums_home':shot_sums_home,'shot_sums_away':shot_sums_away,
            'shot_types_home':shot_types_home,'shot_types_away':shot_types_away}

    def table(id_home: int, id_away: int, gameId: int) -> Dict[str, List[List[Union[str, int]]]]:
        '''
        args:
            id_home(int):      team Id of the home Team
            id_away(int):      team Id of the away Team
            gameId(int):    the Id of the game
        returns
            dict:           the table data as a dict
        '''
        table_home=fetch.tablePlot(id_home,gameId)
        table_away=fetch.tablePlot(id_away,gameId)
        table_data = [[' ', ' ', ' '],
            [sum([x[0] for x in table_home]), 'Total Shots', sum([x[0] for x in table_away])],
            [table_home[1][0], 'Goals', table_away[1][0]],
            [table_home[0][0], 'On Goal', table_away[0][0]],
            [table_home[2][0], 'Misses', table_away[2][0]],
            [table_home[3][0],'Post/bar',table_away[3][0]],
            [table_home[4][0],'Opponent blocked',table_away[4][0]],
            [table_home[5][0],'Teammate blocked',table_away[5][0]]]
        return {'table_data':table_data}

    def targets_by_period(id_home: int, id_away: int, gameId: int) -> Dict[str, DefaultDict[str, Dict[str, int]]]:
        '''
        args:
            id_home(int):      team Id of the home Team
            id_away(int):      team Id of the away Team
            gameId(int):    the Id of the game
        returns
            dict:           the counts of the targets with the period as a dict
        '''
        event_counts_home= defaultdict(lambda: defaultdict(lambda:defaultdict))
        event_counts_away= defaultdict(lambda: defaultdict(lambda:defaultdict))
        for elem in fetch.targetByPeriod(id_home,gameId):
            event_counts_home[str(elem[1])][elem[2]]=elem[0]
        for elem in fetch.targetByPeriod(id_away,gameId):
            event_counts_away[elem[1]][elem[2]]=elem[0]
        return {'event_counts_home':event_counts_home,'event_counts_away':event_counts_away}

    def all(id_home:int,id_away:int,gameId: int):
        '''
        Taking all the results of the functions above and put them into
        a dict structure to be easily callable
        '''
        data={}
        data.update(table.query.singleCardParams(id_home,id_away,gameId))

        #data.update(prepare.params(gameId))
        data.update(prepare.kde(id_home, id_away,gameId))
        data.update(prepare.shooters_by_area(id_home, id_away,gameId))
        data.update(prepare.shot_types(id_home, id_away,gameId))
        data.update(prepare.table(id_home, id_away,gameId))
        data.update(prepare.targets_by_period(id_home, id_away,gameId))
        return data
    
class plot:
    '''
    Plotting the data from shotcard.prepare
    '''

    def params(data):
        '''
        Defining the data for the different subplots and the main plot
        as well as the event colors and event shots
        args:
            data(dict):                 takes in data
        returns:
            kde_home,kde_ab,kde_ab(ax):    axis for the kdePlots
            targetPlot(ax):             axis for the targets by shooters plot
            typePlot(ax):               axis for the shot type per team plot
            tablePlt(ax):               axis for the table of the shots
            period(ax):                 axis for the targets by period plot
            color_shots(dict):          the colors for the different types of shots
            event_colors(dict):         the colors for the different types of shot targets
        '''

        fig = plt.figure(figsize=(8,10))
        gs= gridspec.GridSpec(3, 3, figure=fig)

        kde_home =  fig.add_subplot(gs[0, 0])
        kde_ab = fig.add_subplot(gs[0, 1])
        kde_away = fig.add_subplot(gs[0, 2])
        targetPlot=  fig.add_subplot(gs[2, 0])
        typePlot=  fig.add_subplot(gs[1, 2])
        tablePlt = fig.add_subplot(gs[1,0])
        period = fig.add_subplot(gs[2,2])

        cmap = plt.get_cmap('tab20c')
        event_colors = {'goal':cmap(1%20), 'on goal':cmap(3%20),'blocked':cmap(5%20),
                'teammate-blocked':cmap(7%20),'miss':cmap(9%20),'metal':cmap(11%20)}
        color_shots={'snap':'tab:red','wrist':'tab:blue','slap':'tab:green','tip-in':'tab:cyan','backhand':'tab:orange','poke':'tab:purple',
              'deflected':'tab:olive','wrap-around':'tab:pink','bat':'tab:brown'}           
        logging.info(f"Created the plot param for game {data}")
        return {'kde_home':kde_home,'kde_away':kde_away,'kde_ab':kde_ab,'targetPlot':targetPlot,'typePlot':typePlot,'tablePlt':tablePlt,'period':period,'event_colors':event_colors,'color_shots':color_shots,
                'fig':fig,'plt':plt}


    def kde_plots(data,kde_home,kde_ab,kde_away):
        '''
        Plotting the kernel density estimation of positions
        '''
        img_rink = plt.imread("./assets/rink.png")
        extent=[-43,43, 0, 100]
        levels=9
        thresh=0.25
        fill=False

        kde_home.imshow(img_rink, extent=extent,aspect='auto', zorder=1)
        sns.kdeplot(data=data['data_home'],
            warn_singular=False,
            x="yPos",
            y="xPos",
            levels=levels,
            thresh=thresh,
            fill=fill,
            ax=kde_home,
            color='red',
            extent=extent)
        util.fix.configure_plot(kde_home, f"{data['homeTeamAbbrev']}'s shotpositions", extent)
        logging.info(f"Created KDE Plot for {data['homeTeamAbbrev']}")

        kde_ab.imshow(img_rink, extent=extent,aspect='auto', zorder=1)
        sns.kdeplot(data=data['combined_data'],
            x="yPos",
            y="xPos",
            fill=fill,
            ax=kde_ab,
            levels=levels,
            thresh=thresh,
            hue='team',
            legend=False,
            extent=extent,
            warn_singular=False,
            palette={f"{data['homeTeamId']}": 'red', f"{data['awayTeamId']}": 'blue'})
        logging.info(f"Created KDE Plot for both teams")
        util.fix.configure_plot(kde_ab, f"{data['homeTeamAbbrev']} vs. {data['awayTeamAbbrev']} shotpositions", extent)

        kde_away.imshow(img_rink, extent=extent,aspect='auto', zorder=1)
        sns.kdeplot(data=data['data_away'],
            warn_singular=False,
            x="yPos",
            y="xPos",
            fill=fill,
            thresh=thresh,
            ax=kde_away,
            levels=levels,
            color='blue',
            extent=extent)
        util.fix.configure_plot(kde_away, f"{data['awayTeamAbbrev']}'s shotpositions", extent)
        logging.info(f"Created KDE Plot for {data['awayTeamAbbrev']}")

    def target_plot(data,targetPlot,event_colors):
        '''
        Plotting, the shot target for the top 4 shooters per team
        '''
        x_pos = 0
        for entry in data['d_home']:
            bottom = 0
            for key in data['d_home'][entry].keys():
                targetPlot.bar(x_pos, data['d_home'][entry][key], bottom=bottom, color=event_colors.get(key), label=key)
                bottom += data['d_home'][entry][key]
            imagebox_pl = OffsetImage(get.image.headshot(entry), zoom=0.05, resample=True)
            targetPlot.add_artist(AnnotationBbox(imagebox_pl, (x_pos, bottom + 0.75), frameon=False))
            x_pos += 1
        x_pos = 4
        for entry in data['d_away']:
            bottom = 0
            for key in data['d_away'][entry].keys():
                targetPlot.bar(x_pos, data['d_away'][entry][key], bottom=bottom, color=event_colors.get(key), label=key)
                bottom += data['d_away'][entry][key]
            imagebox_pl = OffsetImage(get.image.headshot(entry), zoom=0.05, resample=True)
            targetPlot.add_artist(AnnotationBbox(imagebox_pl, (x_pos, bottom + 1), frameon=False))
            x_pos += 1
        maxVal=util.fix.max_val(data['d_home'],data['d_away'])

        targetPlot.set_ylim(0, maxVal+4)
        targetPlot.set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
        targetPlot.set_xticklabels([table.query.id_to_name(x) for x in data['d_home'].keys()] + [table.query.id_to_name(x) for x in data['d_away'].keys()], rotation=90)
        targetPlot.set_title("Shooters by target")
        logging.info(f"Created target plot for {data['homeTeamAbbrev']} vs {data['awayTeamAbbrev']}")


    def shot_types_plot(data,typePlot,color_shots):
        '''
        Plotting the different shot types for each team
        normalized to 100&
        '''
        bottom=0
        typePlot.set_xticks(ticks=[0,1],labels=[data['homeTeamAbbrev'],data['awayTeamAbbrev']])
        for elem in data['shot_types_home']:
            typePlot.bar(0,elem[1]/data['shot_sums_home'],bottom=bottom,color=color_shots.get(elem[0]))
            bottom+=elem[1]/data['shot_sums_home']
        logging.info(f"Created shotTypePlot for {data['homeTeamAbbrev']}")
        bottom=0
        for elem in data['shot_types_away']:
            typePlot.bar(1,elem[1]/data['shot_sums_away'],bottom=bottom,color=color_shots.get(elem[0]))
            bottom+=elem[1]/data['shot_sums_away']
        logging.info(f"Created shotTypePlot for {data['awayTeamAbbrev']}")

        handles, labels = [], []
        for shot_type, color in color_shots.items():
            handles.append(plt.Line2D([0], [0], color=color, lw=4, label=shot_type))
            labels.append(shot_type)
            typePlot.legend(handles, labels,loc='center left', bbox_to_anchor=(-1.25,0.5), ncols=1,fontsize='small')
        typePlot.set_title("Shots by Shottype")
        logging.info(f"Created complete shotTypePlot for {data['homeTeamAbbrev']} vs {data['awayTeamAbbrev']}")

    def table(data,tablePlt):
        img_table_a=OffsetImage(get.image.team_img(data['homeTeamAbbrev']),zoom=0.045,resample=True)
        img_table_b=OffsetImage(get.image.team_img(data['awayTeamAbbrev']),zoom=0.045,resample=True)
        annotation_a = AnnotationBbox(img_table_a, (0.09, 0.55), frameon=False)
        annotation_b = AnnotationBbox(img_table_b, (1 - 0.09, 0.55), frameon=False)
        tablePlt.add_artist(annotation_a)
        tablePlt.add_artist(annotation_b) 

        tablePlt.table(cellText=data['table_data'],edges='open',colWidths=[0.5,2.5,0.5],bbox=[0,0.125,1,0.5],cellLoc='center')

        tablePlt.set_ylim(0,0.8)
        tablePlt.axis('off')
        textstr="Made with SQL & Python\nThanks to the NHL API"
        tablePlt.text(1.2, -1, textstr, fontsize=10,verticalalignment='top')
        logging.info('Created table Plot')

    def targetByPeriod(data,period,event_colors):
        '''
        Plotting the shot targets by time period by absolute values
        '''
        bottom_a,bottom_b=[],[]

        for key in data['event_counts_home'].keys():
            y_pos = {"P1": 2, "P2": 1, "P3": 0}
            bottom=0
            for k in data['event_counts_home'][key].keys():
                period.barh(y_pos.get(key), -data['event_counts_home'][key][k], 
                            left=bottom, label=k, color=event_colors.get(k))
                bottom -= data['event_counts_home'][key][k]
            bottom_a.append(bottom) 
        max_a=abs(min(bottom_a))
        period.axvline()
        for key in data['event_counts_away'].keys():
            y_pos = {"P1": 2, "P2": 1, "P3": 0}
            bottom=0
            for k in data['event_counts_away'][key].keys():
                period.barh(y_pos.get(key), data['event_counts_away'][key][k], 
                        left=bottom, label=k, color=event_colors.get(k))
                bottom += data['event_counts_away'][key][k]  # Update the bottom value for the next segment
            bottom_b.append(bottom) 
        max_b=abs(max(bottom_b))
        max_total=max(max_a,max_b)

        unique_labels = {}
        for elem in prepare.targets_by_period(data['homeTeamId'],data['awayTeamId'],data['gameId']) :
            if elem[2] not in unique_labels: unique_labels[elem[2]] = event_colors.get(elem[2])


        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))  # Remove duplicate labels
        period.legend(by_label.values(), by_label.keys(), title="Events",loc='lower left',bbox_to_anchor=(-1.25,0.3))
        period.set_xticks([-(max_total/2),max_total/2])
        period.set_xticklabels([data['homeTeamAbbrev'],data['awayTeamAbbrev']])
        period.get_xaxis().set_visible(True)
        period.set_title("Shots by Reg. period")
        period.set_xlim(-max_total, max_total) 
        period.set_yticks([2, 1,0], labels=["1st", "2nd", "3rd"])
        logging.info('Created ShotTarget by Period shot')


    def final(data):
        '''
        putting all the subplots together into a single fig
        '''
        param=plot.params(data)
        plot.kde_plots(data,param['kde_home'],param['kde_ab'],param['kde_away'])
        plot.target_plot(data,param['targetPlot'],param['event_colors'])
        plot.shot_types_plot(data,param['typePlot'],param['color_shots'])
        plot.targetByPeriod(data,param['period'],param['event_colors'])
        plot.table(data,param['tablePlt'])
        title=f"{data['homeTeam']} vs {data['awayTeam']} Shot overview\n{data['date']} - {data['venue']}"
        param['fig'].suptitle(title, fontsize=16)
        logging.info(f"Created final plot for game {data['gameId']}")
        plt.savefig(f"./assets/shotcard/{data['gameId']}.png",dpi=300)
        plt.close()
        logging.info(f"saved final plot for game {data['gameId']}")
    
    def init():
       
        for (homeTeam,awayTeam,gameId) in table.query.shotCardParamsReg():
                data=prepare.all(homeTeam,awayTeam,gameId)
                plot.final(data)

class retrieve:

    def Card(game_id):
        path='./assets/shotcards/{game_id}'
        return path

