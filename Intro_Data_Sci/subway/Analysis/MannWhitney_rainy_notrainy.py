import numpy as np
import scipy
import scipy.stats
import pandas as pd


def read_csv_data(version):
    """
    Read in csv data to data frame
    """
    
    if version == 1:
        df = pd.read_csv('../data/turnstile_data_master_with_weather.csv')
    else:
        df = pd.read_csv('../data/turnstile_weather_v2.csv')
        
    return df


def mann_whitney_plus_means(version=1):
    '''
    This function will consume the turnstile_weather dataframe containing
    our final turnstile weather data. 
    
    You will want to take the means and run the Mann Whitney U-test on the 
    ENTRIESn_hourly column in the turnstile_weather dataframe.
    
    This function should return:
        1) the mean of entries with rain
        2) the mean of entries without rain
        3) the Mann-Whitney U-statistic and p-value comparing the number of entries
           with rain and the number of entries without rain
    
    You should feel free to use scipy's Mann-Whitney implementation, and you 
    might also find it useful to use numpy's mean function.
    
    Here are the functions' documentation:
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    
    You can look at the final turnstile weather data at the link below:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''
    
    turnstile_weather = read_csv_data(version)
    
    # entries per hour with and without rain
    entries_per_hour_rain = turnstile_weather.ENTRIESn_hourly[turnstile_weather.rain == 1]
    entries_per_hour_norain = turnstile_weather.ENTRIESn_hourly[turnstile_weather.rain == 0]
    
    # mean entries per hour with and without rain
    with_rain_mean = np.mean(entries_per_hour_rain)
    without_rain_mean = np.mean(entries_per_hour_norain)
    
    # Mann-Whitney test
    (U,p) = scipy.stats.mannwhitneyu(entries_per_hour_rain, entries_per_hour_norain)
    
    return with_rain_mean, without_rain_mean, U, p # leave this line for the grader
