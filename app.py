from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

steam_api_key = os.getenv('steam_api_key')

@app.route('/')
def home():
    return render_template('index.html')

def get_owned_games(steam_id):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_api_key}&steamid={steam_id}&format=json&include_appinfo=true"
    response = requests.get(url)
    data = response.json()
    return data['response'].get('games', [])

def suggest_games(games):
    return [game for game in games if game['playtime_forever'] < 600]

@app.route('/check_games', methods=['POST'])
def check_games():
    steam_id = request.form['steam_id']
    games = get_owned_games(steam_id)
    suggestions = suggest_games(games)
    detailed_suggestions = []
    for game in suggestions:
        game_data = {
            'name': game['name'],
            'playtime': game['playtime_forever'] // 60,
            'image_url': f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game['appid']}/capsule_sm_120.jpg"
        }
        detailed_suggestions.append(game_data)
    return render_template('result.html', suggestions=detailed_suggestions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
