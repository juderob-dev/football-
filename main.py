import scrapeImages
import teamSheet


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    teamA="Arsenal"
    teamB="manchester United"


    teamAData = teamSheet.searchTeam("Arsenal")
    teamAList = teamSheet.getTable(teamA)
    for i in teamAList:
        print(i,"hey")




