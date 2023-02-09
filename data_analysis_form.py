import tkinter as tk
from tkinter.ttk import Combobox
# import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from data_extraction import DataExtractor
import matplotlib
matplotlib.use('TkAgg')

class EDAfrm:
    def __init__(self):
        self.frame = tk.Tk()
        self.frame.title('Exploratory Data Analysis')
        self.frame.geometry('1920x1080')
        self.date = tk.StringVar()
        obj = DataExtractor()
        self.df = obj.get_cleaned_data()

        # self.cmb = Combobox(self.frame, state = 'readonly', textvariable= self.date )
        # self.list = []
        # self.cmb.bind('<<ComboboxSelected>>', self.new)

        fig1 = Figure(figsize=(5,5), dpi=100)
        fig2 = Figure(figsize = (5, 5), dpi = 100)

        plot1 = fig1.add_subplot(111)
        plot2 = fig2.add_subplot(111)

        teams = list(self.df['winner'].unique())
        y = []
        x=[]
        team_name = ''

        for team in teams:
            y.append(self.df['winner'].value_counts()[team])
            team_name = ''
            words = team.split(' ')

            for word in words:
                team_name+=word[0].upper()

            x.append(team_name)

        width = .5
        plot1.bar(x,y)
        plot2.pie(self.df['winner'].value_counts(), labels = x,autopct='%0.2f%%',)


        canvas1 = FigureCanvasTkAgg(fig1, master = self.frame)
        canvas2 = FigureCanvasTkAgg(fig2, master = self.frame)

        canvas1.draw()
        canvas2.draw()
        canvas1.get_tk_widget().place(x=200, y=150)
        canvas2.get_tk_widget().place(x=850, y=150)

    def show_dialog(self):
        self.frame.mainloop()