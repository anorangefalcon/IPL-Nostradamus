import tkinter as tk
from tkinter import PhotoImage
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from tkinter import *
from tkinter.ttk import Combobox
from data_extraction import DataExtractor
from tkinter import messagebox
from PIL import ImageTk, Image
import importlib
from logos import Logos
from data_analysis_form import EDAfrm
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot

# from components import Components

class frmHome:
    def __init__(self):
        self.frame = tk.Tk()
        self.frame.title('IPL Nostradamus')

        # adds icon on the app window
        self.nostradamus_icon = PhotoImage(file='/Users/anorangefalcon/Desktop/SPIC ML/IPLmatchPrediction/logosData/logo/nostradamus_logo.png')
        self.frame.wm_iconphoto(True, self.nostradamus_icon)

        self.frame.geometry('1920x1080')
        # self.frame.config(bg = 'grey')
        self.venue = tk.StringVar()
        self.team1 = tk.StringVar()
        self.team2 = tk.StringVar()
        self.toss_winner = tk.StringVar()
        self.toss_decision = tk.StringVar()
        self.toss_decision.set('Bat')

        data_obj = DataExtractor()
        self.venueValues = data_obj.get_venue()
        self.teams = list(data_obj.get_unique_teams())

        self.teams.insert(0,'Select Team')

        self.tossTeams = []

        self.venueLbl = tk.Label(self.frame, text = 'Venue')
        self.venueLbl.place(x = 100, y=50)

        self.venueCmb = Combobox(self.frame, state = 'readonly', textvariable= self.venue)
        self.venueCmb.place(x=100, y=80)
        self.venueCmb['values'] = self.venueValues

        self.team1Lbl = tk.Label(self.frame, text = 'Team 1')
        self.team1Lbl.place(x = 100, y=130)

        self.team1Cmb = Combobox(self.frame, state = 'readonly', textvariable= self.team1)
        self.team1Cmb.place(x= 100, y=160)
        self.team1Cmb['values'] = self.teams
        self.team1Cmb.current(0)
        self.team1Cmb.bind("<<ComboboxSelected>>", self.team1_selection)

        self.team2Lbl = tk.Label(self.frame, text = 'Team 2')
        self.team2Lbl.place(x=100, y=210)
        
        self.team2Cmb = Combobox(self.frame, state ='readonly', textvariable= self.team2)
        self.team2Cmb.place(x=100, y=240)
        self.team2Cmb['values'] = self.teams
        self.team2Cmb.bind('<<ComboboxSelected>>', self.team2_selection)
        
        self.team2Cmb.current(0)

        self.tossWinnerLabel = tk.Label(self.frame, text = 'Toss Winner')
        self.tossWinnerLabel.place(x = 100, y= 290)

        self.tossWinnerCmb = Combobox(self.frame, state = 'readonly', textvariable=self.toss_winner)
        self.tossWinnerCmb.place(x = 100, y=320)

        self.decisionLbl = tk.Label(self.frame, text = 'Toss Decision')
        self.decisionLbl.place(x=100, y=370)

        self.batRbn = tk.Radiobutton(self.frame, text = 'Bat', variable= self.toss_decision, value = 'Bat')
        self.batRbn.place(x= 100, y=400)

        self.fieldRbn = tk.Radiobutton(self.frame, text ='Field', variable=self.toss_decision, value = 'Field')
        self.fieldRbn.place(x = 200, y=400)

        self.submitBtn = tk.Button(self.frame, text = 'Submit', command = self.submit_click)
        self.submitBtn.place(x= 165, y=460)

        # self.img1 = ImageTk.PhotoImage(Image.open('/Users/payal/SPIC/IPLmatchPrediction/logosData/logo/kings_xi_punjab.png'))
        self.logo1Lbl = tk.Label(self.frame, text = ' ')
        # self.logo1Lbl.config(font=('Charter', 30))
        self.logo1Lbl.place(x=500, y=50)

        self.logo2Lbl = tk.Label(self.frame, text = ' ')
        # self.logo2Lbl.config(font=('Charter', 30))
        self.logo2Lbl.place(x =1000 ,y=50)

        self.vsLbl = tk.Label(self.frame, text = ' ')
        self.vsLbl.place(x= 825, y=150)
        
        self.winnerLbl = tk.Label(self.frame, text = ' ')
        self.winnerLbl.config(font=('Rockwell', 30))
        self.winnerLbl.place(x=900, y=350, anchor = 'center')
        
        # self.img = ImageTk.PhotoImage(Image.open('/Users/payal/SPIC/IPLmatchPrediction/logosData/logo/vurses.png'))
        self.img = ImageTk.PhotoImage(Image.open('/Users/anorangefalcon/Desktop/SPIC ML/IPLmatchPrediction/logosData/logo/vurses.png'))
        self.vsLbl.configure(image = self.img)


        self.edaBtn = tk.Button(self.frame, text = 'Exploratory Data Analysis', command = self.eda_button_click)
        self.edaBtn.place(x= 100, y=500)

    def submit_click(self):
        # self.winnerLbl.config(text = 'The winner is')

        self.decision_data = {
            'venue': self.venue.get(),
            'team1' : self.team1.get(), 
            'team2' : self.team2.get(),
            'toss_winner' : self.toss_winner.get(),
            'toss_decision' : self.toss_decision.get()
        }

        # print(self.decision_data)

        extractor = DataExtractor()
        self.df = extractor.get_cleaned_data()
        # print(df.head(5))

        X = self.df[["venue","team1","team2","toss_winner","toss_decision"]]
        Y = self.df["winner"]  

        X = X.to_dict('records')

        vect = DictVectorizer()
        clf = LogisticRegression()

        X_transformed = vect.fit_transform(X)
        self.decision_data_transformed = vect.transform(self.decision_data)

        clf.fit(X_transformed, Y)

        print(self.decision_data_transformed)
        self.predicted_winner = clf.predict(self.decision_data_transformed)
        self.winnerLbl.config(text = self.predicted_winner[0].upper())
        # print(type(self.predicted_winner[0].upper()))
        self.pie_chart()

        count_winner = 0
        count_total_matches_played = 0
        for index, row in self.df.iterrows():
            if row['venue'] == self.decision_data['venue']:
                if row['team1'].lower().strip() == self.decision_data['team1'].lower().strip():
                    count_total_matches_played = 1 + count_total_matches_played
                    if row['winner'] == self.predicted_winner:
                            count_winner = 1 + count_winner
                elif row['team1'].lower().strip() == self.decision_data['team2'].lower().strip():
                    count_total_matches_played = 1 + count_total_matches_played
                    if row['winner'] == self.predicted_winner:
                            count_winner = 1 + count_winner

                if row['team2'].lower().strip() == self.decision_data['team1'].lower().strip():
                    count_total_matches_played = 1 + count_total_matches_played
                    if row['winner'] == self.predicted_winner:
                            count_winner = 1 + count_winner
                elif row['team2'].lower().strip() == self.decision_data['team2'].lower().strip():
                    count_total_matches_played = 1 + count_total_matches_played
                    if row['winner'] == self.predicted_winner:
                            count_winner = 1 + count_winner

        if count_winner < count_total_matches_played-count_winner:
            count_winner = count_total_matches_played - count_winner

        print("total: ", count_total_matches_played)
        print("winner count: ", count_winner)
        # x= [self.team1.get(), self.team2.get()]

        winner_percentage = round((count_winner/count_total_matches_played) * 100, 1)
        loser_percentage = 100 - winner_percentage

        if self.predicted_winner == self.team1.get():
            teams= [self.predicted_winner[0], self.team2.get()]
        else:
            teams = [self.predicted_winner[0], self.team1.get()]

        x = []

        for team in teams:
            team_name = ''
            words = team.split(' ')

            for word in words:
                team_name+=word[0].upper()

            x.append(team_name)
        y= [count_winner, count_total_matches_played - count_winner]


        print(x)
        colors = ['#99ff99', '#ff9999']
        fig1 = Figure(figsize = (4,4), dpi =100)
        plot1 = fig1.add_subplot(111)
        plot1.bar(x, y, color= colors)
        canvas1 = FigureCanvasTkAgg(fig1, master = self.frame)
        canvas1.draw()
        canvas1.get_tk_widget().place(x=550, y=450)

        fig2 = Figure(figsize = (4,4), dpi =100)
        plot2 = fig2.add_subplot(111)
        plot2.pie(y, labels = x,autopct='%0.2f%%',colors = colors)
        canvas2 = FigureCanvasTkAgg(fig2, master = self.frame)
        canvas2.draw()
        canvas2.get_tk_widget().place(x =975 , y =450)


        print(winner_percentage)
        print(loser_percentage)
        

    def eda_button_click(self):
        new_frame = EDAfrm()
        new_frame.show_dialog()

    
    def show_display(self):
        self.frame.mainloop( )

    def team1_selection(self, event):
        match_teams = []

        self.obj = Logos()
        self.logos = self.obj.get_logos()

        # print(self.logos)

        # logo_path = '/Users/payal/SPIC/IPLmatchPrediction/logosData/'
        logo_path = '/Users/anorangefalcon/Desktop/SPIC ML/IPLmatchPrediction/logosData/'
        Team1LogoFileName = ''
        Team2LogoFileName = ''

        if self.team2Cmb.current()>0:
            if self.team2Cmb.current()==self.team1Cmb.current():
                messagebox.showwarning('IPL Analysis','You cannot select same teams!')
                self.team1Cmb.current(0)
            else:
                match_teams.append(self.team1.get())
                match_teams.append(self.team2.get())

                for index, row in self.logos.iterrows():
                    if row[0].lower().strip() == self.team1.get().lower().strip():
                        Team1LogoFileName = row[1]
                    elif row[0].lower().strip()==self.team2.get().lower().strip():
                        Team2LogoFileName = row[1]

                self.img1 = ImageTk.PhotoImage(Image.open(logo_path+Team1LogoFileName))
                self.logo1Lbl.configure(image = self.img1)

                self.img2 = ImageTk.PhotoImage(Image.open(logo_path+Team2LogoFileName))
                self.logo2Lbl.configure(image = self.img2)
        else:
            match_teams = []
            match_teams.append(self.team1.get())

            for index, row in self.logos.iterrows():
                if row[0].lower().strip() == self.team1.get().lower().strip():
                    Team1LogoFileName = row[1]
                    break

            self.img1 = ImageTk.PhotoImage(Image.open(logo_path+Team1LogoFileName))
            self.logo1Lbl.configure(image = self.img1)


        self.tossWinnerCmb['values'] = match_teams


 

    def team2_selection(self, event):
        match_teams = []

        self.obj = Logos()
        self.logos = self.obj.get_logos()

        # self.logo_path ='/Users/payal/SPIC/IPLmatchPrediction/logosData/'
        self.logo_path ='/Users/anorangefalcon/Desktop/SPIC ML/IPLmatchPrediction/logosData/'
        Team1LogoFileName = ''
        Team2LogoFileName = ''


        if self.team1Cmb.current()>0:
            if self.team1Cmb.current()==self.team2Cmb.current():
                messagebox.showwarning('IPL Analysis','You cannot select same teams!')
                self.team2Cmb.current(0)
            else:
                match_teams.append(self.team1.get())
                match_teams.append(self.team2.get())

                for index, row in self.logos.iterrows():
                    if row[0].lower().strip() == self.team1.get().lower().strip():
                        Team1LogoFileName = row[1]
                    elif row[0].lower().strip()==self.team2.get().lower().strip():
                        Team2LogoFileName = row[1]

                self.img1 = ImageTk.PhotoImage(Image.open(self.logo_path+Team1LogoFileName))
                self.logo1Lbl.configure(image = self.img1)

                self.img2 = ImageTk.PhotoImage(Image.open(self.logo_path+Team2LogoFileName))
                self.logo2Lbl.configure(image = self.img2)
        else:
            match_teams.append(self.team2.get())

            for index, row in self.logos.iterrows():
                if row[0].lower().strip() == self.team2.get().lower().strip():
                    Team2LogoFileName = row[1]
                    break

            self.img1 = ImageTk.PhotoImage(Image.open(self.logo_path+Team1LogoFileName))
            self.logo2Lbl.configure(image = self.img1)

        self.tossWinnerCmb['values'] = match_teams
        self.winnerLbl.config(text = 'The Winner Is')

    def pie_chart(self):
        pass
        # count = 0
        # total = 0
        # for rows in self.df:
        #     print(rows[0])
        #     if rows['team1'] == self.team1.get() and rows['team2'] == self.team2.get() and rows['venue'] == self.venue.get():
        #         total = self.df['team1']
        #         if self.predicted_winner == self.df['winner']:
        #             count += 1
        # self.prob = (count /total)*100
        # print(self.prob)



obj = frmHome()
obj.show_display()
