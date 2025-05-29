from flask import Flask, send_file, request, jsonify, send_from_directory
from flask_cors import CORS,cross_origin
import table as table
import os
import sys 
import util
from flask import url_for
import logging
import map

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

BASE_DIR = os.path.dirname(__file__)
CARDS_DIR = os.path.join(BASE_DIR, 'src', 'assets', 'card')
SHOTCARD_DIR = os.path.join(BASE_DIR, 'assets', 'shotcard/')



@app.route('/api/shotcard', methods=['GET'])
def get_shotcard():
    '''
    Returns the shotcard corresponding to the user choice
    Users chooses the team for which the reports should be displayed
    '''
    try:
        team_id = request.args.get('team_id')
        if team_id is None:
            return jsonify({'error': 'team_id param is missing'}), 400
        games = [row[0] for row in table.query.getGamesForTeam(team_id)]
        image_urls = [
        url_for('serve_shotcard_image', filename=f"{game}.png", _external=True)
        for game in games
        if os.path.exists(os.path.join('assets/shotcard', f"{game}.png"))
        ]
        return jsonify({"status": "success", "images": image_urls})
    except Exception as e:
        print(f"Error: {e}")  #
        return jsonify({'error': str(e)}), 500

@app.route('/api/shotcard/<filename>')
def serve_shotcard_image(filename):
    file_path = os.path.join(SHOTCARD_DIR, filename)
    file_path=os.path.normcase(file_path)
    print(file_path)
    if not os.path.exists(file_path):
        return jsonify({"status": "error", "message": "Filed not found"}), 404
    return send_from_directory(SHOTCARD_DIR, filename, mimetype='image/jpeg')  # or appropriate type

@app.route('/api/season', methods=['POST'])
@cross_origin()  
def get_data():
    data = request.get_json()  
    team_ids=list([int(x) for x in data.get('teamIds')])
    map.make.card(team_ids,data.get('events'))
   
    return jsonify({'message': 'Done'})


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000,threaded=True)