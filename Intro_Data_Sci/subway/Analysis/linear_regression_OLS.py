import numpy as np
import scipy
import statsmodels.api as sm
import datetime
import pandas as pd
import pandasql
import matplotlib.pyplot as plt
import sys
import imp


def read_csv_data():
    """
    Read in csv data to data frame
    """
    
    df = pd.read_csv('../data/turnstile_data_master_with_weather.csv')
    #~df = pd.read_csv('../data/turnstile_weather_v2.csv')
        
    return df


def compute_r_squared(data, predictions):
    """
    Coefficient of determination, R^2
    """

    data_mean = np.mean(data)
    r_squared = 1.0 - np.sum(np.square(data - predictions))/np.sum(np.square(data - data_mean))

    return r_squared


def normalize_features(array):
   """
   Normalize the features in the data set.
   """
   
   array_normalized = (array-array.mean())/array.std()
   mu = array.mean()
   sigma = array.std()

   return array_normalized, mu, sigma
   

def polynomial_features(df,col,max_order):
    """
    Calculate polynomial features.
    df: data frame
    col: name of column of data frame to use to create polynomial features
    max_order: highest order of polynomial
    Polynomial feature column names will have the form col^order.
    """
    
    for iorder in range(2,max_order+1):        
        newcol = col + '^' + str(iorder)
        df[newcol] = df[col]**iorder
        
        
    return df


def rename_columns(df):
    """
    rename columns for SQL
    should generalize to just remove all capitalization and under scores
    """
    
    df = df.rename(columns={'Hour':'hour','ENTRIESn_hourly':'entriesperhr','DATEn':'daten'})
    #~df = df.rename(columns={'ENTRIESn_hourly':'entriesperhr','DATEn':'daten'})
        
    return df
    

def nentries_mean(df,col_name):
    """
    mean of the total number of entries for all units for each hour or day
    """    

    # sum of the number of entries per hour for all units
    q = 'SELECT ' + col_name + ', daten, SUM(entriesperhr) AS totentries FROM df GROUP BY ' + col_name + ', daten;'
    df = pandasql.sqldf(q.lower(), locals())
    
    #mean of the total number of entries for all unit
    q = 'SELECT ' + col_name + ', AVG(totentries) AS avgentries FROM df GROUP BY ' + col_name + ';'
    df = pandasql.sqldf(q.lower(), locals())
    
    return df
    

def predictions():
    """
    Linear regression.
    """

    weather_turnstile = read_csv_data()

    # number of records
    npoints = len(weather_turnstile['DATEn'])

    # Day of the week (0=Monday,6=Sunday) and weekday (1 or 0) added to data frame
    dw = np.zeros(npoints)
    wd = np.zeros(npoints)
    dte = np.array(weather_turnstile['DATEn'])
        
    for ipoint in range(npoints):
        day = datetime.datetime.strptime(dte[ipoint],'%Y-%m-%d').date().weekday()
        dw[ipoint] = day
        if day < 5: wd[ipoint] = 1

    pd.set_option('chained_assignment', None)
    weather_turnstile['dayofweek'] = dw.astype(int)
    weather_turnstile['weekday'] = wd.astype(int)
        
    # Polynomial terms for dayofweek
    #~weather_turnstile = polynomial_features(weather_turnstile,'dayofweek',4)

    #~# Create version of dayofweek transformed such that 0 is the day with the lowest average number of entries for all units, 
    #~# 1 is the day with the second lowest average number of entries for all units, etc. The number of entries per hour will then be an 
    #~# increasing function of the transformed day.
    #~
    #~# total number of entries for all units averaged over date for each day of the week
    #~df = weather_turnstile
    #~df = rename_columns(df)
    #~df = df[['dayofweek','entriesperhr','daten']]
    #~df = nentries_mean(df,'dayofweek')
    #~
    #~# map for sorting days
    #~day_sort_map = np.argsort(np.array(np.argsort(df.avgentries)))
    #~df['dayofweeksorted'] = day_sort_map
    #~df.to_csv('../data/avgentriesperday.csv')
    #~
    #~# sort dayofweek and save to new column
    #~d = np.array(weather_turnstile.dayofweek)
    #~ds = np.zeros((npoints)).astype(int)
    #~for i in range(npoints):
        #~ds[i] = day_sort_map[d[i]]
        #~
    #~weather_turnstile['dayofweek_sorted'] = ds
        
    #~# Polynomial terms for dayofweek_sorted
    #~weather_turnstile = polynomial_features(weather_turnstile,'dayofweek_sorted',3)
    
    #~# Polynomial terms for Hour
    #~weather_turnstile = polynomial_features(weather_turnstile,'Hour',7)
    
    #~# Create version of Hour transformed such that 0 is the hour with the lowest average number of entries for all units, 
    #~# 1 is the hour with the second lowest average number of entries for all units, etc. The number of entries per hour will then be an 
    #~# increasing function of the transformed Hour instead of an oscillatory function of Hour and a polynomial can be fit using the transformed Hour.
    #~
    #~# total number of entries for all units averaged over date for each hour
    #~df = weather_turnstile
    #~df = rename_columns(df)
    #~df = df[['hour','entriesperhr','daten']]
    #~df = nentries_mean(df,'hour')
    #~
    #~# map for sorting hours
    #~hour_sort_map = np.argsort(np.array(np.argsort(df.avgentries)))
    #~df['hoursorted'] = hour_sort_map
    #~df.to_csv('../data/hour_sorted.csv')
    #~
    #~# sort hour and save to new column
    #~h = np.array(weather_turnstile.Hour)
    #~hs = np.zeros((npoints)).astype(int)
    #~for i in range(npoints):
        #~hs[i] = hour_sort_map[h[i]]
        #~
    #~weather_turnstile['Hour_sorted'] = hs
    
    #~# Polynomial terms for Hour_sorted
    #~weather_turnstile = polynomial_features(weather_turnstile,'Hour_sorted',7)
    
    # Hour of week
    weather_turnstile['hourofweek'] = weather_turnstile.Hour + 24*weather_turnstile.dayofweek
    
    # Create version of hourofweek transformed such that 0 is the hour with the lowest average number of entries for all units, 
    # 1 is the hour with the second lowest average number of entries for all units, etc. The number of entries per hour will then be an 
    # increasing function of the transformed hourofweek instead of an oscillatory function of hourofweek and a polynomial can be fit using the 
    # transformed hourofweek.
    
    # total number of entries for all units averaged over date for each hour
    df = weather_turnstile
    df = rename_columns(df)
    df = df[['hourofweek','entriesperhr','daten']]
    df = nentries_mean(df,'hourofweek')
    
    # map for sorting hours
    hourofweek_sort_map = np.argsort(np.array(np.argsort(df.avgentries)))
    df['hourofweek_sorted'] = hourofweek_sort_map
    df.to_csv('../data/hourofweek_sorted.csv')
    
    # sort hour and save to new column
    h = np.array(weather_turnstile.hourofweek)
    hs = np.zeros((npoints)).astype(int)
    for i in range(npoints):
        hs[i] = hourofweek_sort_map[h[i]]
        
    weather_turnstile['hourofweek_sorted'] = hs
    
    # Polynomial terms for hourofweek_sorted
    weather_turnstile = polynomial_features(weather_turnstile,'hourofweek_sorted',3)
    
    # Polynomial terms for precipi
    #~weather_turnstile = polynomial_features(weather_turnstile,'precipi',3)
    
    # Polynomial terms for meantempi
    weather_turnstile = polynomial_features(weather_turnstile,'meantempi',4)
            
    features = weather_turnstile[['hourofweek_sorted','hourofweek_sorted^2','hourofweek_sorted^3','meantempi','meantempi^2','meantempi^3','meantempi^4']]

    # Add UNIT to features using dummy variables
    dummy_units = pd.get_dummies(weather_turnstile['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    
    # Normalize features
    features_norm, mu, sigma = normalize_features(features)

    # Values
    values = weather_turnstile['ENTRIESn_hourly']
    
    # Convert features and values to numpy arrays
    features_array = np.array(features_norm)
    values_array = np.array(values)

    # Add a column of 1s to features (intercept)
    features_array = sm.add_constant(features_array)

    # Fitting
    model = sm.OLS(values_array,features_array)
    results = model.fit()
    
    # Coefficients
    coeff = results.params

    # Prediction
    prediction = results.fittedvalues
    
    # Residuals
    residuals = values_array - prediction

    # Coefficient of determination, R^2
    r_squared = compute_r_squared(values_array, prediction)
    
    return prediction, coeff, residuals, r_squared, weather_turnstile
