"""This script is to run through gamertags and create a dictionary of the gamertags
and the kd ratio from the custom games"""
import requests
import bs4

#The function can take another argument of the final page, gives the user the option to alter how many results they need
def data_collect(gamertag):
    """finds the gamertags profile on the website and scrapes the kd ratio for the page range stated"""
    k_d = []
    for page in range(0,2):
        #Used an f string literal to apply the input argument and for loop to the weblink which can be used by
        #any gamertag and page number
        page_url = f'http://halotracker.com/h5/games/{gamertag}?page={page}&mode=custom'
        res = requests.get(page_url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        for value in soup.select('.game-stat-value'):
            k_d.append(float(value.text.strip()))
    k_d = k_d[1::2]
    return k_d
players_kd=[]
def mean_kd():
#Players are in a tuple, as lists are unhashable
    players = ('budbudhardy','flaresman','sashwank','Dead1n5ide','ManChivster','RustlingSpore','Fro5tShark','UBERmatto','r3dFlash')
    for person in players:
        players_kd.append(data_collect(person))
    #kd_dict = dict(zip(players,players_kd))
    #print(kd_dict)
    players_mean_kd = []
    for kd in players_kd:
        mean_kd = round(sum(kd)/len(players_kd[0]),2)
        players_mean_kd.append(mean_kd)
    final_kd = dict(zip(players,players_mean_kd))
    return(final_kd)
    print(final_kd)

mean_kd()
