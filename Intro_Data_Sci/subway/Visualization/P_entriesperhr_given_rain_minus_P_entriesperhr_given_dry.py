from pandas import *
import pandasql
from ggplot import *
import numpy as np
import matplotlib.pyplot as plt

def read_csv_data(version):
    """
    Read in csv data to data frame
    """
    
    if version == 1:
        df = read_csv('../data/turnstile_data_master_with_weather.csv')
    else:
        df = read_csv('../data/turnstile_weather_v2.csv')
        
    return df
    

def plot_weather_data(version=1,nbins=18):
    ''' 
    plot_weather_data is passed a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make another data visualization
    focused on the MTA and weather data we used in Project 3.
    
    Make a type of visualization different than what you did in the previous exercise.
    Try to use the data in a different way (e.g., if you made a lineplot concerning 
    ridership and time of day in exercise #1, maybe look at weather and try to make a 
    histogram in this exercise). Or try to use multiple encodings in your graph if 
    you didn't in the previous exercise.
    
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time-of-day or day-of-week
     * How ridership varies by subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/
     
    You can check out the link 
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    to see all the columns and data points included in the turnstile_weather 
    dataframe.
     
   However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''   
    
    turnstile_weather = read_csv_data(version)
    
    # bins
    entries_max = turnstile_weather.ENTRIESn_hourly.max()
    entries_min = turnstile_weather.ENTRIESn_hourly.min()
    bins = np.linspace(entries_min,entries_max,nbins)
    binwidth = bins[1] - bins[0]
    
    # probabilities for number of entries per hour on dry days
    dry = turnstile_weather.ENTRIESn_hourly[turnstile_weather.rain == 0]
    (hist_dry,bin_edges) = np.histogram(dry,bins)
    prob_dry = hist_dry/float(np.sum(hist_dry))
    
    # probabilities for number of entries per hour on rainy days
    rainy = turnstile_weather.ENTRIESn_hourly[turnstile_weather.rain == 1]
    (hist_rain,bin_edges) = np.histogram(rainy,bins)
    prob_rain = hist_rain/float(np.sum(hist_rain))
    
    # plot histograms on rainy and dry days
    plt.hist(np.array(dry),bins=bins,color='w',label='dry')
    plt.hist(np.array(rainy),bins=bins,label='rainy')
    
    plt.legend()
    plt.title('Histograms of number of entries per hour on rainy and dry days')
    plt.xlabel('Number of entries per hour')
    plt.xlim(0,20000)
    plt.ylabel('Count')
    plt.ylim(-1000,55000)
    plt.show()
    
    # probablities when rainy - probabilities when dry
    prob_diff = prob_rain - prob_dry
    
    # improvised bar plot
    # geom_bar with stat='identity' does not seem to work

    # data frame for ggplot
    df = DataFrame({'xmin' : bins[:-1], 'xmax' : bins[1:],
                    'ymin' : prob_diff*((prob_diff < 0).astype(float)),
                    'ymax' : prob_diff*((prob_diff > 0).astype(float)),
                    'sign' : np.sign(prob_diff)})
                    
    
    # plot difference in probabilities on rainy and dry days
    plot = ggplot(df,aes(xmin='xmin',xmax='xmax',ymin='ymin',ymax='ymax',fill='sign')) + \
    geom_rect() + \
    geom_hline(yintercept=0,color='black') + \
    ggtitle('Probabilty of entries/hr when rainy - probability of entries/hr when dry') + \
    xlab('E = Entries/hr') + \
    ylab('P(E | rainy) - P(E | dry)')
    
    return plot
