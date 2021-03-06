import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
from time import sleep

f = open('C:/Users/Public/Documents/key.txt', 'r')
key = f.read()
f.close()

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': key,
}

params = urllib.parse.urlencode({
    # Request parameters
})

player_roster = ['budbudhardy','flaresman','Dead1n5ide','RustlingSpore','sashwank','ManChivster','UBERmatto','Fro5tShark']
for name in player_roster:
    sleep(5)
    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", f"/stats/h5/players/{name}/matches?modes=custom", "{body}", headers)
        response = conn.getresponse()
        my_bytes_value = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    my_json = my_bytes_value.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    match_id_list = []
    for info in data['Results']:
        match_id= info['Id']['MatchId']
        match_id_list.append(match_id)
    player_kills_count = []
    player_death_count = []
    player_assist_count = []
    for info in data['Results']:
        player_kills = info['Players'][0]['TotalKills']
        player_kills_count.append(player_kills)
        player_deaths = info['Players'][0]['TotalDeaths']
        player_death_count.append(player_deaths)
        player_assist = info['Players'][0]['TotalAssists']
        player_assist_count.append(player_assist)
    gamertag = data['Results']
    print(gamertag[0]['Players'][0]['Player']['Gamertag'])
    player_kda = (sum(player_kills_count) + (1/3*(sum(player_assist_count))))/sum(player_death_count)
    print(round(player_kda,3))
    print(sum(player_kills_count))
    print(sum(player_death_count))
    print(sum(player_assist_count))
    print('-' * 30)

