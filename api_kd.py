import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import time
import random

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

player_gamertag_list = []
player_kda_count = []

player_roster = ['BudbudHardy','Flaresman','Dead1n5ide','RustlingSpore','Sashwank','ManChivster','UBERmatto','Fro5tShark','r3dFLash']

def data_collect(gamertag):

    player_kills_count = []
    player_death_count = []
    player_assist_count = []
    
    time.sleep(2)
    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", f"/stats/h5/players/{gamertag}/matches?modes=custom", "{body}", headers)
        response = conn.getresponse()
        my_bytes_value = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    my_json = my_bytes_value.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    for info in data['Results']:
        player_kills = info['Players'][0]['TotalKills']
        player_kills_count.append(player_kills)
        player_deaths = info['Players'][0]['TotalDeaths']
        player_death_count.append(player_deaths)
        player_assist = info['Players'][0]['TotalAssists']
        player_assist_count.append(player_assist)
    gtag = data['Results']
    gamertag_list = gtag[0]['Players'][0]['Player']['Gamertag']
    player_gamertag_list.append(gamertag_list)
    player_kda = round((sum(player_kills_count) + (1/3*(sum(player_assist_count))))/sum(player_death_count),3)
    player_kda_count.append(player_kda)
    # print(gamertag_list, sum(player_kills_count), sum(player_death_count), sum(player_assist_count))
    # print(player_kda)
    

def mean_kd():
	for name in player_roster:
	    data_collect(name)
	global kd_dict
	kd_dict = dict(zip(player_gamertag_list, player_kda_count))
	print('data collected')
	return(kd_dict)