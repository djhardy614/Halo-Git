import http.client
import urllib.request
import urllib.parse
import urllib.error
import json
import time

with open('C:/Users/Public/Documents/key.txt', 'r') as f:
    key = f.read()

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': key,
}

params = urllib.parse.urlencode({
    # Request parameters
})


class Player():

    def __init__(self, gamertag):
        self.gamertag = gamertag
        self.gamertag_list = []
        self.kills = []
        self.assists = []
        self.deaths = []
        self.match_ids = []
        self.total_kills_list = []
        self.total_deaths_list = []
        self.total_assists_list = []
        self.weapon_damage_list = []
        self.total_headshot_list = []
        self.total_accuracy_list = []
        self.total_kda_list = []

    def data_collector(self):
        try:
            conn = http.client.HTTPSConnection('www.haloapi.com')
            conn.request(
                "GET", "/stats/h5/players/{}/matches?modes=custom".format(self.gamertag), "{body}", headers)
            response = conn.getresponse()
            my_bytes_value = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            # Converting the bytes into JSON format
        my_json = my_bytes_value.decode('utf8').replace("'", '"')

        data = json.loads(my_json)
        for info in data['Results']:
            player_kills = info['Players'][0]['TotalKills']
            player_deaths = info['Players'][0]['TotalDeaths']
            player_assist = info['Players'][0]['TotalAssists']
            self.kills.append(player_kills)
            self.deaths.append(player_deaths)
            self.assists.append(player_assist)
        for info in data['Results']:
            match_id = info['Id']['MatchId']
            self.match_ids.append(match_id)

    def get_kda(self):
        dave.data_collector()
        kda = (sum(dave.kills) + 1 / 3 * sum(dave.assists)) / sum(dave.deaths)
        matches_kda = (sum(dave.kills[0:5]) + 1 / 3 *
                       sum(dave.assists[0:5])) / sum(dave.deaths[0:5])
        print(abs(matches_kda - kda))

    def get_match_data(self, match_id):
        # for match_id in self.match_ids[0:5]:
        time.sleep(2)
        try:
            conn = http.client.HTTPSConnection('www.haloapi.com')
            conn.request(
                "GET", "/stats/h5/custom/matches/{}".format(match_id), "{body}", headers)
            response = conn.getresponse()
            my_bytes_value = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        my_json = my_bytes_value.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        # to select relevant info, add in dictionary key
        for info in data['PlayerStats']:
            name = info['Player']['Gamertag']
            self.gamertag_list.append(name)
            totalkills = info['TotalKills']
            self.total_kills_list.append(totalkills)
            totalassists = info['TotalAssists']
            self.total_assists_list.append(totalassists)
            totaldeaths = info['TotalDeaths']
            self.total_deaths_list.append(totaldeaths)
            weapondamage = info['TotalWeaponDamage']
            self.weapon_damage_list.append(weapondamage)
            totalheadshot = info['TotalHeadshots']
            self.total_headshot_list.append(totalheadshot)
            accuracy = info['TotalShotsLanded'] / info['TotalShotsFired']
            self.total_accuracy_list.append(round(accuracy, 2))
            kda = (totalkills + (totalassists * 1 / 3)) / (totaldeaths)
            self.total_kda_list.append(round(kda, 2))
            print(name, ':', 'K:', totalkills, 'A:', totalassists, 'D:', totaldeaths, 'Acc', round(
                accuracy * 100, 2), '%', 'KDA:', round(kda, 2))


dave = Player('BudbudHardy')
dave.data_collector()
print(dave.kills)

# dave.get_kda()
dave.get_match_data(dave.match_ids[0])
