#!/usr/bin/env python

# Import standard library
from os import environ, sep
from os.path import exists, basename, splitext
from glob import glob

# Import common modules
from pandas import read_csv, DataFrame
from numpy import sum, zeros

class DataLoader(object):
    
    def __init__(self, dirName=None):

        # Can take directory name from input        
        if dirName is None:
            dirName = raw_input('Input location of data directory - ')

        # Correct common linux approach
        if '~' in dirName:
            dirName = dirName.replace('~', environ['HOME'])
            
        # Make sure ending is correct
        if not dirName.endswith(sep):
            dirName = dirName + sep

        # Confirm file exists and get list of data files
        if exists(dirName):
            dataFiles = glob(dirName + '*.csv')
        else:
            print dirName + " doesn't exist"
            return

        # Load each file into a pandas DataFrame
        for fName in dataFiles:
            
            temp = basename(fName)
            name = splitext(temp)[0]
            self.__dict__[name] = read_csv(fName)

# Main script
if __name__ == '__main__':

    # Load Raw Data
    raw_data = DataLoader('~/Workspace/Kaggle/marchmania2015/data')
    
    # Process Data Features
    wins = zeros(len(raw_data.teams))
    loss = zeros(len(raw_data.teams))
    tWins = zeros(len(raw_data.teams))
    tLoss = zeros(len(raw_data.teams))
    ids = []
    names = []
    for i in range(len(raw_data.teams)):
        ids.append(raw_data.teams['team_id'][i])
        names.append(raw_data.teams['team_name'][i])
        
        # Regular Season basics
        wins[i] = sum(raw_data.regular_season_compact_results['wteam'] == ids[i])
        loss[i] = sum(raw_data.regular_season_compact_results['lteam'] == ids[i])

        # Tourney basics
        tWins[i] = sum(raw_data.tourney_compact_results['wteam'] == ids[i])
        tLoss[i] = sum(raw_data.tourney_compact_results['lteam'] == ids[i])

    # Create Features DataFrame
    feature_data = DataFrame(names, index=ids, columns=['name'])
    feature_data['wins_season'] = wins
    feature_data['losses_season'] = loss
    feature_data['wins_tourney'] = tWins
    feature_data['losses_tourney'] = tLoss

    # Add derived features
    feature_data['win_perc_season'] = feature_data['wins_season']/(feature_data['losses_season'] + feature_data['wins_season'])
    feature_data['win_perc_tourney'] = feature_data['wins_tourney']/(feature_data['losses_tourney'] + feature_data['wins_tourney'])
    print feature_data
