
import pandas as pd
import numpy as np

charts = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRRPejhjYGUYtLWTfBRZLmzBgvEGAYHm4DdGb8thCfBXJJlL1RzjHSKd7pF_aX_7AqO0cYo6KzJ4knU/pub?output=csv')
print('charts')
scores = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSSJwU9zaPLWEweKlhJzYuHy-B5v3U4JP8UIzkMBe0SpZ07hzSFZC-zINPgJYH_yGUOkO7u1YpW47nv/pub?output=csv')
scores.fillna(0, inplace = True)
scores[scores.columns[1:]].astype(int)
print('scores')
equivs = scores
print('equivs')



charts.reindex(['Charts', 'Tier', 'Max Score'])

print(scores)

def addChart(name, tier, maxscore):
  scores[name] = [0 for i in scores.index]
  equivs[name] = [0 for i in scores.index]
  charts[name] = [tier, maxscore]

def addPlayer(player):
  if len(scores[scores["Player"] == player].index) > 0:
    print('gofy')
  else:
    list = [player]
    list[1:] = ([0 for gonk in range(1,len(scores.columns))])
    scores.loc[len(scores.index)] = list
    equivs.loc[len(equivs.index)] = list

def equiv(score, maxscore, tier):
  C = int(tier)
  a = -C + 33
  b = C / ( np.exp(a) - 1)
  x = score / maxscore
  f = (C + b) * np.exp(-a * (1-x)) - b
  return(5 * f)
  
def addScore(player, chart, score):
  if score > charts[chart]['Max Score'] or score < 0:
    print('stupid')
  elif score < scores[chart][scores.index[scores['Player'] == player].tolist()[0]] and score != 0:
    print('gonk')
  else:    scores.at[scores.index[scores['Player'] == player].tolist()[0], chart] = score

def playerStats(player):
  print('Data for ' + player + "\n", pd.DataFrame({
    'Charts': equivs.columns,
    'Equiv': equivs.iloc[equivs.index[equivs['Player'] == player].tolist()[0]], 
    'Score': scores.iloc[scores.index[scores['Player'] == player].tolist()[0]]}).drop(index = 'Player').sort_values(by = 'Equiv', ascending = False).head(2 *counts))

def chartStats(chart):
  print('Data for '  + chart + '\n', pd.DataFrame({
    'Player': scores['Player'],
    'Score': scores[chart],
    'Equiv': equivs[chart]
  }).sort_values(by = 'Score', ascending = False))

def weightedAverage(list, count):
  mean = 100 / count
  weights = [
    2*mean - ( (2 * mean) / (count + 1) ) * i for i in range(1, count + 1)
  ]
  print(weights)
  return(sum([list[i] * (weights[i] / 100) for i in range (0, count)]))

def updateEquiv():
  for chart in charts:
    tier = charts[chart].values[0]
    maxscore = charts[chart].values[1]
    data = scores[chart].values
    for i in range(0, len(data)):
      equivs.at[i, chart] = equiv(scores[chart][i], maxscore, tier)

counts = 10

def leaderboard():
  leaderboards = pd.DataFrame({
    'Player': [0 for i in range(0, len(scores.index))], 'Rank': [0 for i in range(0,len(scores.index))]
  }, index = [i for i in range(0,len(scores.index))])
  for index, row in equivs.iterrows():
    leaderboards.iloc[index] = [row['Player'], round(weightedAverage(sorted(row.tolist()[1:], reverse = True), counts), 2)]
  print(leaderboards.sort_values(by = 'Rank', ascending = False).head(20))



updateEquiv()
leaderboard()

playerStats('jif')
playerStats('snaphap')