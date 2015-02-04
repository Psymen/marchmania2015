#!/usr/bin/env python

# Import standard library
from os import environ, sep
from os.path import exists, basename, splitext
from glob import glob

# Import common modules
from pandas import read_csv, DataFrame
from numpy import sum, zeros, nan

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

# Main scriptgit
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

    # Add derived features
    feature_data['percent_season'] = feature_data['wins_season']/(feature_data['losses_season'] + feature_data['wins_season'])

    # Get data by individual year
    years = raw_data.seasons['season']
    for year in years:
        
        cYear = raw_data.regular_season_compact_results['season'] == year
        
        feature_data['wins_s_' + str(year)] = nan
        feature_data['losses_s_' + str(year)] = nan
        feature_data['percent_s_' + str(year)] = nan
        
        wins = zeros(len(feature_data.index.values))
        losses = zeros(len(feature_data.index.values))
        for i in range(len(feature_data.index.values)):
        
            _id = feature_data.index.values[i]
             
            c1 = raw_data.regular_season_compact_results['wteam'][cYear] == _id
            c2 = raw_data.regular_season_compact_results['lteam'][cYear] == _id
            wins[i] = sum(c1)
            losses[i] = sum(c2)
            
        feature_data['wins_s_' + str(year)] = wins
        feature_data['losses_s_' + str(year)] = losses
        feature_data['win_perc_s_' + str(year)] = wins/(wins+losses)

    feature_data.to_csv('features.csv')
    
