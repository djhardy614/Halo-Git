import http.client
import urllib.request
import urllib.parse
import urllib.error
import json
import time
import xlsxwriter

with open('C:/Users/Public/Documents/key.txt', 'r') as f:
    key = f.read()

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': key,
}

params = urllib.parse.urlencode({
    # Request parameters
})
outWorkbook = xlsxwriter.Workbook('OOP MVP.xlsx')
cell_format = outWorkbook.add_format({'align': 'center', 'bold': True})

class Player():

    def __init__(self, gamertag):
        self.gamertag = gamertag
        self.match_ids = []
        self.kda_l = []
        self.m_kda_l = []
        self.kills = []
        self.assists = []
        self.deaths = []

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

        kda = round((sum(self.kills) + 1 / 3 *
                     sum(self.assists)) / sum(self.deaths), 2)
        self.kda_l.append(kda)
        matches_kda = round((sum(self.kills[0:5]) + 1 / 3 *
                             sum(self.assists[0:5])) / sum(self.deaths[0:5]), 2)
        self.m_kda_l.append(matches_kda)
        print(self.kda_l)
        print(self.m_kda_l)

        print(round(abs(matches_kda - kda), 2))

        # create new list for total values to add to output

    def get_match_data(self, match_id):

        outSheet = outWorkbook.add_worksheet()
        outSheet.set_column('A:A', 15)
        outSheet.set_column('B:E', 12)
        gamertag_list = []
        total_kills_list = []
        total_deaths_list = []
        total_assists_list = []
        weapon_damage_list = []
        total_headshot_list = []
        total_accuracy_list = []
        total_kda_list = []
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
            gamertag_list.append(name)
            totalkills = info['TotalKills']
            total_kills_list.append(totalkills)
            totalassists = info['TotalAssists']
            total_assists_list.append(totalassists)
            totaldeaths = info['TotalDeaths']
            total_deaths_list.append(totaldeaths)
            weapondamage = info['TotalWeaponDamage']
            weapon_damage_list.append(weapondamage)
            totalheadshot = info['TotalHeadshots']
            total_headshot_list.append(totalheadshot)
            accuracy = info['TotalShotsLanded'] / info['TotalShotsFired']
            total_accuracy_list.append(round(accuracy, 2))
            kda = (totalkills + (totalassists * 1 / 3)) / (totaldeaths)
            total_kda_list.append(round(kda, 2))
            # print(name, ':', 'K:', totalkills, 'A:', totalassists, 'D:', totaldeaths, 'Acc', round(
            # accuracy * 100, 2), '%', 'KDA:', round(kda, 2))
            for item in range(len(gamertag_list)):
                outSheet.write('A1', 'Names', cell_format)
                outSheet.write('B1', 'Match Kills', cell_format)
                outSheet.write('C1', 'Match Deaths', cell_format)
                outSheet.write('D1', 'Match Assist', cell_format)
                outSheet.write('E1', 'Match KDA', cell_format)
                outSheet.write(item + 1, 0, gamertag_list[item])
                outSheet.write(item + 1, 1, total_kills_list[item])
                outSheet.write(item + 1, 2, total_deaths_list[item])
                outSheet.write(item + 1, 3, total_assists_list[item])
                outSheet.write(item + 1, 4, total_kda_list[item])

    def create_report(self):
        dave.get_match_data(dave.match_ids[0])
        dave.get_match_data(dave.match_ids[1])
        dave.get_match_data(dave.match_ids[2])
        dave.get_match_data(dave.match_ids[3])
        dave.get_match_data(dave.match_ids[4])

    def total_sheet(self):
        outSheet = outWorkbook.add_worksheet()
        for name in names:
            name.data_collector()

        outSheet.write('A1', 'Name', cell_format)
        outSheet.write('B1', 'Match kills', cell_format)
        outSheet.write('C1', 'Match deaths', cell_format)
        outSheet.write('D1', 'Match assists', cell_format)
        outSheet.write('E1', "Match's KDA", cell_format)
        outSheet.write('F1', '25 match kills', cell_format)
        outSheet.write('G1', '25 match deaths', cell_format)
        outSheet.write('H1', '25 match assists', cell_format)
        outSheet.write('I1', '25 match KDA', cell_format)
        outSheet.write('J1', 'KDA diff', cell_format)
        outSheet.set_column('A:J', 15)
        outSheet.write('A3', 'Sashwank')
        outSheet.write('A4', 'ManChivster')
        outSheet.write('A5', 'BudbudHardy')
        outSheet.write('A6', 'Fro5tShark')
        outSheet.write('A7', 'Dead1n5ide')
        outSheet.write('A8', 'RustlingSpore')
        outSheet.write('A9', 'Flaresman')

        for index, name in enumerate(names):
            outSheet.write(index + 2, 1, sum(name.kills[0:5]))
            outSheet.write(index + 2, 2, sum(name.deaths[0:5]))
            outSheet.write(index + 2, 3, sum(name.assists[0:5]))
            outSheet.write(index + 2, 4, name.m_kda_l[0])
            outSheet.write(index + 2, 5, sum(name.kills))
            outSheet.write(index + 2, 6, sum(name.deaths))
            outSheet.write(index + 2, 7, sum(name.assists))
            outSheet.write(index + 2, 8, name.kda_l[0])
            outSheet.write(index + 2, 9, name.m_kda_l[0] - name.kda_l[0])


dave = Player('BudbudHardy')
rob = Player('Sashwank')
sam = Player('ManChivster')
paul = Player('Flaresman')
chris = Player('Dead1n5ide')
matt = Player('RustlingSpore')
alex = Player('Fro5tShark')
names = [rob, sam, dave, alex, chris, matt, paul]
dave.data_collector()
# rob.data_collector()
# sam.data_collector()


# print(dave.kills)

# dave.get_kda()


dave.create_report()
dave.total_sheet()

outWorkbook.close()
