""" Script Accesses Halo API for players previous 25 custom matches and creates a dictionary combining gamertag and average kda of the last 25 matches"""
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import time
import random
#Read in subscription key for API
f = open('C:/Users/Public/Documents/key.txt', 'r')
key = f.read()
f.close()

#Assign subscription key to authentication
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': key,
}

params = urllib.parse.urlencode({
    # Request parameters
})

player_gamertag_list = []
player_kda_count = []
#List of players gamertags
player_roster = ['BudbudHardy','Flaresman','Dead1n5ide','RustlingSpore','Sashwank','ManChivster','UBERmatto','Fro5tShark','r3dFLash']
#Function defined to access the Halo API for each gamertag put in as an arguement.
def data_collect(gamertag):

    player_kills_count = []
    player_death_count = []
    player_assist_count = []
    #Sleep added to prevent over use of API requesting limits
    time.sleep(2)
    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", f"/stats/h5/players/{gamertag}/matches?modes=custom", "{body}", headers)
        response = conn.getresponse()
        my_bytes_value = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    #Converting the bytes into JSON format
    my_json = my_bytes_value.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    #Looping through the JSON data to extract relevant data(kills, deaths and assists) and add to lists
    for info in data['Results']:
        player_kills = info['Players'][0]['TotalKills']
        player_kills_count.append(player_kills)
        player_deaths = info['Players'][0]['TotalDeaths']
        player_death_count.append(player_deaths)
        player_assist = info['Players'][0]['TotalAssists']
        player_assist_count.append(player_assist)
    #Finding the players gamertag within the data and adding to a list outside of the function
    gtag = data['Results']
    gamertag_list = gtag[0]['Players'][0]['Player']['Gamertag']
    player_gamertag_list.append(gamertag_list)
    #Calculating the KDA for each player and adding to an external list. Assists are rated at 1/3 of a kill
    player_kda = round((sum(player_kills_count) + (1/3*(sum(player_assist_count))))/sum(player_death_count),3)
    player_kda_count.append(player_kda)  

#New function defined to apply the data_collection function to a list of players. Gathers and calculates KDA for each player in the list.
def mean_kd():
	for name in player_roster:
	    data_collect(name)
	#Global variation defined as it's used in another script
	global kd_dict
	#Combine together the list of gamertags and their calculated KDA value 
	kd_dict = dict(zip(player_gamertag_list, player_kda_count))
	#Print statement to show the script has worked and finished
	print('data collected')
	return(kd_dict)