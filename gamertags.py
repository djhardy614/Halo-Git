
gamertags = {'dave':'budbudhardy','paul':'flaresman','rob':'sashwank','mills':'Dead1n5ide','sam':'ManChivster','g matt':'RustlingSpore','frost':'Fro5tShark','s matt':'UBERmatto','gary':'r3dFlash'}
player_roster = []
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
gamer_roster = []
for person in player_roster:
	if person in gamertags.keys():
		gtag = gamertags.get(gamertags.values())
		gamer_roster.append(gtag)

print(gamer_roster)

# r_gamertags = {v:k for k, v in gamertags.items()}
# print(r_gamertags)
# for person in player_roster:
# 	r_gamertags.get(item,item)
