import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import time
import random
import xlsxwriter

f = open('C:/Users/Public/Documents/key.txt', 'r')
key = f.read()

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': key,
}

params = urllib.parse.urlencode({
    # Request parameters
})

map_choice = ['Eden','Coliseum','Empire','Echelon','Fathom','Mercy','Molten','Overgrowth','Plaza','Regret','Riptide','Stasis','The Rig','Torque','Truth','Tyrant','Nyxium','Seclusion','Jade Harbour','Solasium','Pegasus','Orion','Furnace']
fix_wbook = xlsxwriter.Workbook('Fixtures.xlsx')
w_s = fix_wbook.add_worksheet()
bold = fix_wbook.add_format({'bold':True})
red = fix_wbook.add_format({'font_color':'red'})
blue = fix_wbook.add_format({'font_color':'blue'})
align = fix_wbook.add_format({'align':'center'})
merge_format = fix_wbook.add_format({
    'border': 5,
    'align':'center',
    'valign':'vcenter',
    'fg_color':'yellow'})
w_s.set_column('C:G', 15)
w_s.set_column('B:B', 10)

w_s.write(0, 0, 'Fixtures',bold)
w_s.write(0, 6, "Team's mean KD", bold)
w_s.write(1, 1 , 'Red Team:', red)
w_s.write(3, 1 , 'Blue Team:', blue)
w_s.write(5, 1, 'Red Team:', red)
w_s.write(7, 1, 'Blue Team:', blue)
w_s.write(9, 1, 'Red Team:', red)
w_s.write(11, 1, 'Blue Team:', blue)
w_s.write(13, 1, 'Red Team:', red)
w_s.write(15, 1, 'Blue Team:', blue)
w_s.write(18, 0, 'Maps',bold)

def map_selector():
    
    random.shuffle(map_choice)
    w_s.write(18, 1, 'The first map tonight is: ' + map_choice[0])
    w_s.write(19, 1, 'The second map for tonight : ' + map_choice[1])
    w_s.write(20, 1, 'The third map for tonight is: ' + map_choice[2])
    w_s.write(21, 1, 'The fourth map tonight is: '+ map_choice[3])
    w_s.write(22, 1, 'Free-for-all: ' + map_choice[4])

player_roster = []

def team_creator():
       
    while True:
        try:
            new_player = str(input('Add a player or enter "done" to close roster: '))
            player_roster.append(new_player)
        except:
            print('Please enter a name')
        else:
            if new_player.lower() == 'done':
                player_roster.pop()
                break

player_kills_count = []
player_death_count = []
player_assist_count = []
player_kda_count = []
player_gamertag_list = []

def data_collect(gamertag):

    
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

for name in player_roster:
    data_collect(name)

kd_dict = dict(zip(player_gamertag_list, player_kda_count))


def shuffler():

    random.shuffle(player_roster)
    half_list = len(player_roster)//2
    if len(player_roster) % 2 == 0 or len(player_roster) % 2 == 1:
        global team_one
        global team_two
        team_one = player_roster[0:half_list]
        team_two = player_roster[half_list:]
    global team_one_kd
    global team_two_kd
    global kd_one_list
    global kd_two_list
    team_one_kd = 0
    team_two_kd = 0
    kd_one_list = []
    kd_two_list = []

    for name in team_one:
        for key, value in kd_dict.items():
            if key == name:
                team_one_kd = team_one_kd + value
                kd_one_list.append(value)

    for name in team_two:
        for key, value in kd_dict.items():
            if key == name:
                team_two_kd = team_two_kd + value
                kd_two_list.append(value)

    global team_one_mean
    global team_two_mean

    team_one_mean = round(team_one_kd/len(team_one),2)
    team_two_mean = round(team_two_kd/len(team_two),2)

def teams():
    count = 0
    while count < 4:
        shuffler()
        if abs(team_one_mean - team_two_mean) <= 0.3:

            if count == 0:

                for player in range(len(team_one)):
                    n = len(team_one)
                    w_s.write(1, player+2, team_one[player])
                    w_s.write(2, len(team_one)+2, team_one_mean, align)
                    # w_s.write(2, 2, kd_one_list[0], align)
                    # w_s.write(2, 3, kd_one_list[1], align)
                    # w_s.write(2, 4, kd_one_list[2], align)
                    # w_s.write(2, 5, kd_one_list[3], align)

                for player in range(len(team_two)):
                    w_s.write(3, player+2, team_two[player])
                    w_s.write(4, len(team_two)+2, team_two_mean, align)
                    # w_s.write(4, 2, kd_two_list[0], align)
                    # w_s.write(4, 3, kd_two_list[1], align)
                    # w_s.write(4, 4, kd_two_list[2], align)
                    # w_s.write(4, 5, kd_two_list[3], align)

                count += 1

            elif count == 1:

                for player in range(len(team_one)):
                    w_s.write(5, player+2, team_one[player])
                    w_s.write(6, len(team_one)+2, team_one_mean, align)
                    # w_s.write(6, 2, kd_one_list[0], align)
                    # w_s.write(6, 3, kd_one_list[1], align)
                    # w_s.write(6, 4, kd_one_list[2], align)
                    # w_s.write(6, 5, kd_one_list[3], align)

                for player in range(len(team_two)):
                    w_s.write(7, player+2, team_two[player])
                    w_s.write(8, len(team_two)+2, team_two_mean, align)
                    # w_s.write(8, 2, kd_two_list[0], align)
                    # w_s.write(8, 3, kd_two_list[1], align)
                    # w_s.write(8, 4, kd_two_list[2], align)
                    # w_s.write(8, 5, kd_two_list[3], align)

                count += 1

            elif count == 2:

                for player in range(len(team_one)):
                    w_s.write(9, player+2, team_one[player])
                    w_s.write(10, len(team_one)+2, team_one_mean, align)
                    # w_s.write(10, 2, kd_one_list[0], align)
                    # w_s.write(10, 3, kd_one_list[1], align)
                    # w_s.write(10, 4, kd_one_list[2], align)
                    # w_s.write(10, 5, kd_one_list[3], align)

                for player in range(len(team_two)):
                    w_s.write(11, player+2, team_two[player])
                    w_s.write(12, len(team_two)+2, team_two_mean, align)
                    # w_s.write(12, 2, kd_two_list[0], align)
                    # w_s.write(12, 3, kd_two_list[1], align)
                    # w_s.write(12, 4, kd_two_list[2], align)
                    # w_s.write(12, 5, kd_two_list[3], align)
                count += 1

            elif count == 3:

                for player in range(len(team_one)):
                    w_s.write(13, player+2, team_one[player])
                    w_s.write(14, len(team_one)+2, team_one_mean, align)
                    # w_s.write(14, 2, kd_one_list[0], align)
                    # w_s.write(14, 3, kd_one_list[1], align)
                    # w_s.write(14, 4, kd_one_list[2], align)
                    # w_s.write(14, 5, kd_one_list[3], align)

                for player in range(len(team_two)):
                    w_s.write(15, player+2, team_two[player])
                    w_s.write(16, len(team_two)+2, team_two_mean, align)
                #     w_s.write(16, 2, kd_two_list[0], align)
                #     w_s.write(16, 3, kd_two_list[1], align)
                #     w_s.write(16, 4, kd_two_list[2], align)
                #     w_s.write(16, 5, kd_two_list[3], align)
                # count += 1
        else:
            shuffler()

def map_check():
    while True:
        if 'Seclusion' in map_choice[0:5] and len(player_roster) % 2 == 1:
            random.shuffle(map_choice)
            print('The first map tonight is: ' + map_choice[0] + '\n\nThe second map for tonight : ' + map_choice[1] + '\n\nThe third map for tonight is: ' + map_choice[2] + '\n\nThe fourth map tonight is: '+ map_choice[3] + '\n\nFree-for-all: ' + map_choice[4])
        
        else:
            break

def halo_mondays():
 
    team_creator()
    for name in player_roster:
        data_collect(name)
    map_selector()
    map_check() 
    teams()
    fix_wbook.close()
   
everyone = input('Is everyone playing? y or n ')

if everyone[0].lower() == 'y':
    player_roster = ['budbudhardy','flaresman','Dead1n5ide','RustlingSpore','sashwank','ManChivster','UBERmatto','Fro5tShark']
    for name in player_roster:
        data_collect(name)
    map_selector()
    map_check()
    teams()
    fix_wbook.close()

elif everyone[0].lower() == 'n':
    no_matt = input('Is Shit Matt playing? y or n ')
    if no_matt[0].lower() == 'n':
        player_roster = ['budbudhardy','flaresman','Dead1n5ide','RustlingSpore','sashwank','ManChivster','Fro5tShark']
        for name in player_roster:
            data_collect(name)
        map_selector()
        map_check()
        teams()
        fix_wbook.close()

    elif no_matt[0].lower() == 'y':
        halo_mondays()
