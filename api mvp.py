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

try:
    conn = http.client.HTTPSConnection('www.haloapi.com')
    conn.request("GET", f"/stats/h5/players/budbudhardy/matches?modes=custom", "{body}", headers)
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

for match_id in match_id_list[0:5]:

    sleep(2)

    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", f"/stats/h5/custom/matches/{match_id}", "{body}", headers) 
        response = conn.getresponse()
        my_bytes_value = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    my_json = my_bytes_value.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    for info in data['PlayerStats']:       #to select relevant info, add in dictionary key 
        name = info['Player']['Gamertag']
        totalkills = info['TotalKills']
        totalassists = info['TotalAssists']
        totaldeaths = info['TotalDeaths']
        weapondamage = info['TotalWeaponDamage']
        shoulderbash = info['TotalShoulderBashDamage']
        totalheadshot = info['TotalHeadshots']
        kda = (totalkills + (totalassists * 1/3))/(totaldeaths)
        efficency = weapondamage/totalkills
        print(name, totalkills, totalassists, totaldeaths, round(efficency,2), round(kda,2))
    print('-'*30)

