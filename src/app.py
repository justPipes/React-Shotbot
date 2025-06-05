from flask import Flask, send_file, request, jsonify, send_from_directory
from flask_cors import CORS,cross_origin
import table as table
import os
import threading
import sys 
import util
from flask import url_for
import logging
import map
import time

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "https://react-shotbot.onrender.com",
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],  # Alle benötigten Methoden
        "allow_headers": ["Content-Type", "Authorization"],      # Alle benötigten Headers
        "supports_credentials": True                             # Falls Cookies/JWT
    }
})

BASE_DIR = os.path.dirname(__file__)
CARDS_DIR = os.path.join(BASE_DIR, 'src', 'assets', 'card')
SHOTCARD_DIR = os.path.join(BASE_DIR, 'assets', 'shotcard/')

@app.route('/')
def index():
    return send_from_directory('../build/','index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('../build/static', path)

@app.route('/api/shotcard', methods=['GET'])
@cross_origin()
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
@cross_origin()
def serve_shotcard_image(filename):
    '''
    Serving the shotcard for the choosen team
    '''
    file_path = os.path.join(SHOTCARD_DIR, filename)
    file_path=os.path.normcase(file_path)
    print(file_path)
    if not os.path.exists(file_path):
        return jsonify({"status": "error", "message": "Filed not found"}), 404
    return send_from_directory(SHOTCARD_DIR, filename, mimetype='image/jpeg')  # or appropriate type

@app.route('/api/season', methods=['GET','POST'])
@cross_origin()
def get_data():
    '''
    Reading out the data from the seaosn page
    Creating the img and returning it
    '''
    data=request.get_json()
    img=map.make.card(data['teamIds'],data['events'])
    return send_file(img, mimetype='image/png')

@app.route('/api/season/result')
@cross_origin()
def serve_card():
    return send_from_directory('../public/static/cards/','result.png')

@app.errorhandler(Exception)
def handle_exception(e):
    '''
    General error handler
    '''
    return jsonify({"error": str(e)})
    ''''
    '''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',debug=True, port=port,threaded=True)