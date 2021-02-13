"""This script is to run through gamertags and create a dictionary of the gamertags
and the kd ratio from the custom games"""
import requests
import bs4
import statistics
import xlsxwriter

#Players are in a tuple, as lists are unhashable
players = ('budbudhardy','flaresman','sashwank','Dead1n5ide','ManChivster','RustlingSpore','Fro5tShark','UBERmatto', 'r3dFlash')
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

players_kd = [] 
total_kd = []
overall_kd = []
for person in players:
    players_kd.append(data_collect(person))
players_mean_kd = []
for kd in players_kd:
     mean_kd = round(statistics.mean(kd[0:6]),3)
     overall_kd_value = round(statistics.mean(kd),3)
     total_sum_kd = round(sum(kd),3)
     total_kd.append(total_sum_kd)
     players_mean_kd.append(mean_kd)
     overall_kd.append(overall_kd_value)
final_kd = dict(zip(players,players_mean_kd))

outWorkbook = xlsxwriter.Workbook('MVP.xlsx')
outSheet = outWorkbook.add_worksheet()

cell_format = outWorkbook.add_format({'align':'center', 'bold':True})

outSheet.write('A1', 'Names', cell_format)
outSheet.write('D1', 'Last night K/D ', cell_format)
outSheet.set_column('A:D', 15)
outSheet.set_column('C:C', 17)
outSheet.write('C1', '20 games total K/D', cell_format)
outSheet.write('B1', '20 games K/D ', cell_format)
outSheet.write('E1', 'Round 6', cell_format)
outSheet.write('F1', 'Round 5', cell_format)
outSheet.write('G1', 'Round 4', cell_format)
outSheet.write('H1', 'Round 3', cell_format)
outSheet.write('I1', 'Round 2', cell_format)
outSheet.write('J1', 'Round 1', cell_format)

for item in range(len(players)):
    outSheet.write(item+1, 0, players[item])
    outSheet.write(item+1, 1, players_mean_kd[item])
    outSheet.write(item+1, 2, total_kd[item])
    outSheet.write(item+1, 3, overall_kd[item])

for row_num, row_data in enumerate(players_kd):
    for col_num, col_data in enumerate(row_data[0:6]):
        outSheet.write(row_num+1, col_num+4, col_data)  

outWorkbook.close()
