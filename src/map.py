import table
import table
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import const
import numpy as np
import const
import matplotlib.patches as mpatches


class make:
    def card(team_ids,events):
        # to fix:
        # y -> -y
        data=prep.data(team_ids,events)
        d=data
        plot.card(d)
        return None
    
    def test():
        conn=sqlite3.connect('./main.db')
        cursor=conn.cursor()
        q=cursor.execute('''SELECT xPos,yPos from goals where eventOwnerTeamId=8;''').fetchall()
        x=[i[0] for i in q]
        y=[i[1] for i in q]
        conn.commit()
        conn.close()
        plt.figure(figsize=(8,10))
        img=plt.imread("./assets/cards/rinkdno.png")
        extent=[-43,43, -100, 100]
        plt.imshow(img, extent=extent,aspect='auto', zorder=1)
        plt.scatter(y,x)
        plt.savefig('result.png')
        plt.close()
        

class prep:

    def data(team_ids,events):
        res=[]
        for team in team_ids:
            for event in events:
                data = table.query.cardData(team, event) 
                df = pd.DataFrame(data[event], columns=prep.OneCol(event))
                res.append(df)
        return pd.concat(res) 

    
    def OneCol(keyword):
        result=[]
        match keyword:
            case 'Takeaways':
                result=['xPos','yPos','playerId','eventOwnerTeamId']
            case 'Giveaways':
                result=['xPos','yPos','playerId','eventOwnerTeamId']
            case 'Goals':
                result=['xPos','yPos','playerId','shotType','state','goalie','eventOwnerTeamId']
            case 'Misses':
                result=['xPos','yPos','playerId','shotType','state','goalie','eventOwnerTeamId']
            case 'Blocked shot':
                result=['xPos','yPos','playerId','blockingPlayerId','reason','goalie','eventOwnerTeamId']
            case 'Misses':
                result=['xPos','yPos','playerId','shotType','reason','goalie','eventOwnerTeamId']
            case 'Hits':
                result=['xPos','yPos','hittingPlayerId','hitteePlayerId','eventOwnerTeamId']
            case 'Shots':
                result=['xPos','yPos','playerId','shotType','goalie','shotType','eventOwnerTeamId']
        return result
    
    def manyCol(keywordList:list):
        out=[]
        final=[]
        for keyword in keywordList:
            out.extend(prep.OneCol(keyword))
            final.extend(out)
        return list(set(final))
            


class plot:
    def card(data):
        plt.figure(figsize=(8,10))
        img=plt.imread("./assets/cards/rinkdno.png")
        extent=[43,-43, -100, 100]
        plt.imshow(img, extent=extent,aspect='auto', zorder=1)
        labels=np.unique(data['eventOwnerTeamId'])
        cmap = plt.cm.get_cmap('tab10', len(labels))
        team_to_color = {team_id: cmap(i) for i, team_id in enumerate(labels)}
        colors = data['eventOwnerTeamId'].map(team_to_color)
        plt.scatter(data['yPos'],data['xPos'],c=colors)
        legend_handles = [mpatches.Patch(color=team_to_color[team_id], label=const.NHL_TEAMS.get(team_id, 'Unknown')) for team_id in labels]
        plt.axis('off')
        plt.legend(handles=legend_handles, loc= 'center',ncols=8,bbox_to_anchor=(0.5,-0.1))
        plt.savefig('./assets/cards/t.png',dpi=300)
        plt.close()

    def cardKDE(data):
        fig = plt.figure(figsize=(8,10))
        img= plt.imread("./assets/rink.png")
        extent=[-43,43, -100, 100]
        fig.imshow(img, extent=extent,aspect='auto', zorder=1)
        extent=[-43,43, 0, 100]
        levels=9
        thresh=0.25
        fill=False
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
        plt.savefig(f"./assets/shotcard/{data['gameId']}.png",dpi=300)
        plt.close()