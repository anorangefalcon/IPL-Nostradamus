import pandas as pd
import numpy as np

class DataExtractor:

    def __init__(self):
        # self.df = pd.read_csv('IPL Matches 2008-2020.csv')
        self.df = pd.read_csv('/Users/anorangefalcon/Desktop/SPIC ML/IPLmatchPrediction/IPL Matches 2008-2020.csv')
        # self.df = pd.read_csv('/Users/payal/SPIC/IPLmatchPrediction/IPL Matches 2008-2020.csv')
        
        self.df.drop(columns=['id','city','date','player_of_match','neutral_venue','result','result_margin','eliminator','method','umpire1','umpire2'],inplace=True)
        self.df.dropna(axis=0, subset='winner', inplace=True)

        cleantext = lambda x: self.clean_text(x)

        self.df['venue'] = pd.DataFrame(self.df.venue.apply(cleantext))
        self.df['team1'] = pd.DataFrame(self.df.team1.apply(cleantext))
        self.df['team2'] = pd.DataFrame(self.df.team2.apply(cleantext))
        self.df['toss_winner'] = pd.DataFrame(self.df.toss_winner.apply(cleantext))
        self.df['toss_decision'] = pd.DataFrame(self.df.toss_decision.apply(cleantext))
        self.df['winner'] = pd.DataFrame(self.df.winner.apply(cleantext))

        self.df.team1 = self.df.team1.str.replace('delhi daredevils','delhi capitals')
        self.df.team2 = self.df.team2.str.replace('delhi daredevils','delhi capitals')
        self.df.winner = self.df.winner.str.replace('delhi daredevils','delhi capitals')

        self.df.team1 = self.df.team1.str.replace('deccan chargers','sunrisers hyderabad')
        self.df.team2 = self.df.team2.str.replace('deccan chargers','sunrisers hyderabad')
        self.df.winner = self.df.winner.str.replace('deccan chargers','sunrisers hyderabad')

        self.df.drop(self.df[self.df.team1 == 'kochi tuskers kerala'].index,inplace = True)
        self.df.drop(self.df[self.df.team1 == 'pune warriors'].index,inplace = True)
        self.df.drop(self.df[self.df.team1 == 'rising pune supergiants'].index,inplace = True)
        self.df.drop(self.df[self.df.team1 == 'gujarat lions'].index,inplace = True)
        self.df.drop(self.df[self.df.team1 == 'rising pune supergiant'].index,inplace = True)
        self.df.drop(self.df[self.df.team2 == 'kochi tuskers kerala'].index,inplace = True)
        self.df.drop(self.df[self.df.team2 == 'pune warriors'].index,inplace = True)
        self.df.drop(self.df[self.df.team2 == 'rising pune supergiants'].index,inplace = True)
        self.df.drop(self.df[self.df.team2 == 'gujarat lions'].index,inplace = True)
        self.df.drop(self.df[self.df.team2 == 'rising pune supergiant'].index,inplace = True)

        self.df = self.df.reset_index()


    def clean_text(self, text):
        text = text.lower()
        return text

    def get_cleaned_data(self):
        return self.df

    def get_venue(self):
        self.array = self.df['venue'].unique()

        self.venue_list = self.array.tolist()

        return self.venue_list

    def get_unique_teams(self):

        return self.df['team1'].unique()

