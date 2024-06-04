import requests
import json 
import pandas as pd
from time import sleep
import datetime
import os


cwd = os.getcwd() 
print("Current directory is-", os.getcwd()) 

os.chdir(input("Which file directory do you want to save this under?"))
print("New directory is-", os.getcwd()) 

# Zoom League Names stored in a dictionary
competitors = {
        "1":"Premier-Zoom",
        "2": "Liga-Zoom",
        "3": "Bundes-Zoom",
        "4":"SerieA-Zoom",
        "5":"Ligue1-Zoom",
        "6":"Primeira-Zoom",
        "7": "Eredivisie-Zoom",
        "8":"Zoom Tornado League"
} 

# Function to retrieve response from the betting API server
def getSeasonResult(competitor, leagueName, season):
    url = "https://zoomapi.bet9ja.com/zoomexternalapi/SeasonResult/Results"
    params = {
        "clientId": "101",
        "competitionId": competitor,
        "previous": season
    }
    headers = {
        "Cookie": "_fbp=fb.1.1709989492898.1573887337; cif_=Y; _gcl_au=1.1.547721733.1709989501; _ga=GA1.1.1485785155.1709989495; _tgpc=b2c69978-e7bb-5bce-aa3c-4933cd2eb3c4; _tglksd=eyJzIjoiMzA3YjJmMzMtZWE4Yi01YjJlLTk2ODMtNjI4OTg2MzIzMzkwIiwic3QiOjE3MTAxNzcwNjI2OTksInNvZCI6Ind3dy5nb29nbGUuY29tIiwic29kdCI6MTcxMDE3NzA2MjY5OSwic29kcyI6ImMiLCJzb2RzdCI6MTcxMDE3NzA2NTY5MX0=; _sp_srt_id.55ca=e4c7e10f-31e6-4177-822c-3e48ad2c3a8e.1710177066.1.1710177067..fb7e2d5e-de16-4d66-b0d0-b5f6aa12179d....0; cto_bundle=TdO3FV8wVG54c3JuUnI2OE1qS3klMkJueWE3Sk91SUFodjRpZCUyQnR3QyUyQnNKc2M0OER1RU5yajBxZnhLSGlsU1prd2lwMEtuJTJGbVc2dUhrbjh5ZllUbGFlT2RVZTJWSDN6WHFpb3V6Snl2eCUyRkhpRjJJMnB3YmMwNkRmc3NHUkJ6Mkw5VCUyRlB4YWRJSDM2RjZnMGxLTE1rdTRxMFVINmclM0QlM0Q; _ga_YYQNLHMCQS=GS1.1.1710177070.2.1.1710177084.0.0.0; ak_bmsc=3A9048940CAEC6AEA4D0E69E1D1C3A89~000000000000000000000000000000~YAAQhYbdWKJmNTSOAQAA/yztOhc83lZINTscwEtUIeewEX6WWd2LgZi0qcmy06tI6OxMNrLc6TlM9w/zDJOpWnZWVz+HeUV+4CHGXulxYy4PDVetisFJN+eiDlhGfKPlBPqidNn8oSr5E7+feL+K089qmRI4htz2auPNEDAhg8F57fdckSluSrUQiDjvpj588loYHudU7xPpJVnfO8VCB1yiOvKYjpwFPJKRsfjhbHLTgHHzXI58wdh7jkp3exAbzBI8Uv18t2EFlpXzZUuD70NID7CO3GaY3lGFN2gsXrjrjm9h/Js3KnXvZABeDGP0seSYde2S/i/PVSBgEjkujHgiS/BLbAkFsS2bmPz52X4Qh123ZUCEq74WtPCMJk2qRH3LbsjerbTLeg==; bm_sv=F0063711DB699A234B798D07CC05561F~YAAQhYbdWPBmNTSOAQAATNHtOhefxSFzl3aoU0jaMOlOKTTKAvmYQ364LfgKT37ENII0/NZM382r5pN9c+odVlncrQGcXQmyHr7xvfcaHVzyUbkKp2GNhwVEGKlcVvM6hEp3xrgKc2mytPqdjhtBeCmXfg/jhYvE7mxmRyWX+3q6swN8it4aSDbZiaWLWVifF+8U5yVIr0u3aN5+9c515+7HRl+4FNmHuNJ6fErb9jOidbgwvMEXTd7RuXCJXCyy~1",
        "Sec-Ch-Ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "Clientid": "101",
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.65 Safari/537.36",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://zoomapi.bet9ja.com/zoom/results/premier-zoom?clientId=101&offset=3600000&matchId=2205748",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, params=params, headers=headers)
    textFile = json.loads(response.text)
    seasonResults = pd.DataFrame(textFile)


    # storing the season start date in a variable
    dd, mm, year = ((seasonResults['data']['rounds'][0]['time']).split(" ")[0]).split("-")
    time = (seasonResults['data']['rounds'][0]['time']).split(" ")[1].replace(":","_")
    print(time)
    seasonStartDate = f"{mm}-{dd}-{year}"
   
    # Custom season naming convention to keep track of time and season startdate
    seasonResults.to_json(f"{leagueName} {seasonStartDate} {time}.json")

    print(f"{leagueName} {seasonStartDate} Season data stored in json")

# Looping through all the leagues in Bet9ja Zoom to store their season results
for key,value in competitors.items():
    sleep(2)
    # Get previous season results
    try: 
        getSeasonResult(key,value, "1")
    except: 
        print(f"{competitors[key]} previous season data not stored in json")
    # Get current season results
    try: 
        getSeasonResult(key,value, "0")
    except: 
        #print error message 
        print(f"{competitors[key]} Season data not stored in json")
 
