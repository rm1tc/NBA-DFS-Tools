import json
import csv
import math
import numpy as np

class NBA_Evolutionary_Lineup_Selector:
    config = None
    player_dict = {}
    roster_construction = ['PG', 'SG', 'SF', 'PF', 'C', 'F', 'G', 'UTIL']
    lineup_pool = {}
    tournament_results = {}

    def __init__(self):
        self.load_config()
        self.load_projections(self.config['projection_path'])
        self.load_boom_bust(self.config['boombust_path'])
        self.load_lineup_pool(self.config['output_path']) # Load lineups generated by our optimizer


    # Load config from file
    def load_config(self):
        with open('config.json') as json_file: 
            self.config = json.load(json_file)
         
    # Load projections from file
    def load_projections(self, path):
        # Read projections into a dictionary
        with open(path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                player_name = row['Name']
                self.player_dict[player_name] = {'Fpts': 0, 'Position': [], 'ID': 0, 'Salary': 0, 'StdDev': 0, 'Ownership': 0, 'In Lineup': False}
                self.player_dict[player_name]['Fpts'] = float(row['Fpts'])

                #some players have 2 positions - will be listed like 'PG/SF' or 'PF/C'
                self.player_dict[player_name]['Position'] = [pos for pos in row['Position'].split('/')]

                if 'PG' in self.player_dict[player_name]['Position'] or 'SG' in self.player_dict[player_name]['Position']:
                    self.player_dict[player_name]['Position'].append('G')

                if 'SF' in self.player_dict[player_name]['Position'] or 'PF' in self.player_dict[player_name]['Position']:
                    self.player_dict[player_name]['Position'].append('F')

                self.player_dict[player_name]['Position'].append('UTIL')


                self.player_dict[player_name]['Salary'] = int(row['Salary'].replace(',',''))
                # need to pre-emptively set ownership to 0 as some players will not have ownership
                # if a player does have ownership, it will be updated later on in load_ownership()
                self.player_dict[player_name]['Salary'] = int(row['Salary'].replace(',',''))

    # Load standard deviations
    def load_boom_bust(self, path):
        with open(path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                player_name = row['Name']
                if player_name in self.player_dict:
                    self.player_dict[player_name]['StdDev'] = float(row['Std Dev'])

    def load_lineup_pool(self, path):
        with open(path) as file:
            reader = csv.DictReader(file)
            i = 0
            for row in reader:
                self.lineup_pool[i] = [row['PG'], row['SG'], row['SF'], row['PF'], row['C'], row['G'], row['F'], row['UTIL']]
                i = i + 1

    def run_evolution(self):
        # From the pool of lineups, simulate a GPP
        # For each lineup in the pool, mark how often they win, finish top 1%, finish top 10%
        # Create some metric from the win%,1%,10%
        # Keep only the top 90% from each iteration
        # Repeat until you have a set of 150 lineups
        pass
        