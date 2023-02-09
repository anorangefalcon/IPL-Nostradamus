import pandas as pd

class Logos:
    def __init__(self):
        self.logos = pd.read_csv("/Users/anorangefalcon/Desktop/SPIC ML/IPLmatchPrediction/logosData/IPLlogos.csv")
        # self.logos = pd.read_csv("/Users/payal/SPIC/IPLmatchPrediction/logosData/IPLlogos.csv")

    def get_logos(self):
        return self.logos

