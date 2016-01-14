from pandas import *
import pandasql
from ggplot import *


def read_csv_data(version):
    """
    Read in csv data to data frame
    """
    
    if version == 1:
        df = read_csv('../data/turnstile_data_master_with_weather.csv')
    else:
        df = read_csv('../data/turnstile_weather_v2.csv')
        
    return df


def rename_columns(version,df):
    """
    rename columns for SQL
    should generalize to just remove all capitalization and under scores
    """
    
    if version == 1:
        df = df.rename(columns={'Hour':'hour','ENTRIESn_hourly':'entriesperhr','DATEn':'daten'})
    else:
        df = df.rename(columns={'ENTRIESn_hourly':'entriesperhr','DATEn':'daten'})
        
    return df
    

def nentries_mean(df):
    """
    mean of the total number of entries per hour for all units for each hour
    """
    
    # sum of the number of entries per hour for all units
    q = """
    SELECT hour, daten, SUM(entriesperhr) AS totentriesperhr
    FROM df
    GROUP BY hour, daten;
    """
    df = pandasql.sqldf(q.lower(), locals())
    
    # mean of the total number of entries per hour for all units for each hour
    q = """
    SELECT hour, AVG(totentriesperhr) AS avgentriesperhr
    FROM df
    GROUP BY hour;
    """
    df = pandasql.sqldf(q.lower(), locals())
    
    return df
        

def plot_weather_data(version=1):
    '''
    You are passed in a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.  
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.  

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time of day or day of week
     * How ridership varies based on Subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/
     
    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
     
    To see all the columns and data points included in the turnstile_weather 
    dataframe. 
     
    However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''
    
    turnstile_weather = read_csv_data(version)
    
    # rename columns for SQL and keep only the necessary ones
    turnstile_weather = rename_columns(version,turnstile_weather)
    turnstile_weather = turnstile_weather[['hour','entriesperhr','daten']]

    # mean of the total number of entries per hour for all units for each hour
    turnstile_weather = nentries_mean(turnstile_weather)

    # plot
    # with 1/3 of data, numbers will be about 1/3 as large since data for 2/3 of units on average on a date are missing
    plot = ggplot(turnstile_weather, aes(x='hour',y='avgentriesperhr')) + \
    geom_point() + \
    geom_line() + \
    ggtitle('Total number of entries averaged over date for each hour') + \
    xlab('Hour of the day') + \
    ylab('Mean number of entries for all units')
    
    return plot, turnstile_weather.avgentriesperhr


#ggsave(plot,'nentries_per_hour_mean.png')
