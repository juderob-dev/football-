import wikipedia
import urllib3
import requests
from bs4 import BeautifulSoup,NavigableString, Tag
import json
# had to pip install xlml

def searchTeam(team):
    result = wikipedia.search(team+" football club first teams ")
    print(wikipedia.search("Arsenal Football team"))
    page= wikipedia.page(result[0])


    return (page.url)
    categories= page.categories
    content=page.content
    print(categories)
def getTable(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session = requests.Session()
    html = session.get(url, verify=False).content

    soup = BeautifulSoup(html, 'lxml')


    #table = soup.find('span', {'class': 'agent vcard'})
    table= soup.find('table', {'class':'wikitable football-squad nogrid'})
    table2 = soup.find('table', {'class': 'wikitable football-squad nogrid'}).find_next('table', {'class': 'wikitable football-squad nogrid'})

    #print(soup)
    #print(table2)

    content = {}

    #for table in soup.select('table class="wikitable football-squad nogrid" '):
    createTeamJson(table,content)
    createTeamJson(table2, content)
    return content



def createTeamJson(table, content):

    playerNamePL = 0
    playerNumberPL = 0
    nationPL = 0
    positionPL = 0

    for row in table.find_all('tr'):
        children = list(row.children)

        count = 0
        player = ""
        nation = ""
        pos = ""
        number = ""

        for item in children:

            if isinstance(item, NavigableString):
                continue
            elif isinstance(item, Tag):


                if item.name == 'th':
                    if item.get_text().strip() == 'Number':
                        playerNumberPL = count

                    elif item.get_text().strip() == 'Nation':
                        nationPL = count

                    elif item.get_text().strip() == 'Pos.':
                        positionPL = count

                    elif item.get_text().strip() == 'Player':
                        playerNamePL = count


                elif item.name == 'td':

                    if count == playerNumberPL:
                        number = item.get_text().strip()

                    elif count == nationPL:
                        nation = item.get_text().strip()
                    elif positionPL == count:
                        pos = item.get_text().strip()

                    elif count == playerNamePL:
                        player = item.get_text().strip()

                count = count + 1
        if number:

            section = {
                'NO.': number,
                # 'html': html,
                'pos.': pos,
                'Nation': nation,
                'Player': player
            }

            content[number] = section

        json.dumps(content, indent=2)

if __name__=="__main__":
    team = searchTeam("Arsenal")
    teamlist = getTable(team)
    print(teamlist)

