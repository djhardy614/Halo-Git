import requests
import bs4


gamertag = str(input('What is your gamertag? '))

page_url = f'http://halotracker.com/h5/weapons/{gamertag}'
res = requests.get(page_url)
soup = bs4.BeautifulSoup(res.text, 'lxml')
weapon_values = soup.select('.value')
weapon_details = soup.select('.name')
all_names = soup.find_all('h4')
name = soup.h4.text


weapons = []
weapon_list = []
weapon_titles = []
weapon_stats = []

for name in all_names:
	weapon_list.append(name.text)
n = 26

weapon_list.remove('Support the Site')
for item in weapon_list:
	stripped_name = item[:-n]
	weapons.append(stripped_name)

for title in weapon_details:
	weapon_titles.append(title.text)

for stats in weapon_values:
	weapon_stats.append(stats.text)

kills = dict(zip(weapons, weapon_stats[::6]))
headshots = dict(zip(weapons, weapon_stats[3::6]))
accuracy = dict(zip(weapons, weapon_stats[4::6]))

# print("The number of kills with each weapon", kills)
# print("The number of headshots with each weapon", headshots)
# print("Accuracy with each weapon", accuracy)

output = input('What do you want to see: kills, headshots, accuracy or exit?')


if output[0].lower() == 'k':
	print(kills)
elif output[0].lower() == 'h':
	print(headshots)
elif output[0].lower() == 'a':
	print(accuracy)
