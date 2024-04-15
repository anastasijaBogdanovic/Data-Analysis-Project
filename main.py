import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

urls_to_scrape = {
   "2022": "https://www.hockey-reference.com/leagues/NHL_2022_skaters.html",
   "2021": "https://www.hockey-reference.com/leagues/NHL_2021_skaters.html",
   "2020": "https://www.hockey-reference.com/leagues/NHL_2020_skaters.html"
}

def extract_data(url, season):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'stats'})
    df = pd.read_html(StringIO(str(table)))[0]
    df['Season'] = season
    return df

dfs = [extract_data(url, season) for season, url in urls_to_scrape.items()]

all_data = pd.concat(dfs, ignore_index=True)

#print("Column Names:", all_data.columns)
all_data.columns = [' '.join(col).strip() for col in all_data.columns.values]
all_data['Age'] = pd.to_numeric(all_data['Unnamed: 2_level_0 Age'], errors='coerce')

average_age_per_team_season = all_data.groupby(['Unnamed: 3_level_0 Tm', 'Season'], as_index=False)['Age'].mean()
average_max_age_per_season = all_data.groupby('Season', as_index=False)['Age'].agg(['mean', 'max']).reset_index()

#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

print("Average Age per Team and Season:")
print(average_age_per_team_season)

print("\nAverage and Maximum Age per Season only:")
print(average_max_age_per_season)
