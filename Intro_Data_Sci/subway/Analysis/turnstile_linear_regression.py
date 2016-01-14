import numpy as np
import pandas
import matplotlib.pyplot as plt
from ggplot import *

def normalize_features(array):
    """
    Normalize the features in the data set.
    """
   
    array_normalized = (array-array.mean())/array.std()
    mu = array.mean()
    sigma = array.std()

    return array_normalized, mu, sigma


def compute_cost(features, values, theta):
    """
    Compute the cost function given a set of features / values, 
    and the values for our thetas.
    """

    npoints = len(values)
    sum_of_square_errors = np.square(np.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*npoints)

    return cost


def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.
    """
    
    # number of points
    npoints = len(values)
    
    # intialize cost history
    cost_history = []
    
    # num_interations iterations
    for iiter in range(num_iterations):
        
        # compute and store cost
        cost = compute_cost(features, values, theta)
        cost_history.append(cost)
        
        # update values of theta
        values_predicted = np.dot(features, theta)
        theta = theta + (alpha/npoints)*(np.dot(values - values_predicted,features))
        
    return theta, pandas.Series(cost_history)


def predictions(dataframe):
    '''
    The NYC turnstile data is stored in a pandas dataframe called weather_turnstile.
    Using the information stored in the dataframe, let's predict the ridership of
    the NYC subway using linear regression with gradient descent.
    '''

    # Select Features (try different features!)
    features = dataframe[['rain', 'fog', 'precipi', 'Hour', 'meantempi', 'maxdewpti']]

    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    
    # Values
    values = dataframe['ENTRIESn_hourly']
    npoints = len(values)

    features, mu, sigma = normalize_features(features)
    features['ones'] = np.ones(npoints) # Add a column of 1s (y intercept)
    
    # Convert features and values to numpy arrays
    features_array = np.array(features)
    values_array = np.array(values)

    # Set values for alpha, number of iterations.
    alpha = 0.1 # please feel free to change this value
    num_iterations = 75 # please feel free to change this value

    # Initialize theta, perform gradient descent
    theta_gradient_descent = np.zeros(len(features.columns))
    theta_gradient_descent, cost_history = gradient_descent(features_array, 
                                                            values_array, 
                                                            theta_gradient_descent, 
                                                            alpha, 
                                                            num_iterations)

    print cost_history.tail()
    
    plot = plot_cost_history(alpha, cost_history)
    ggsave(plot,'cost_history.png')
    
    predictions = np.dot(features_array, theta_gradient_descent)
    
    return predictions, plot


def plot_cost_history(alpha, cost_history):
   """
   This function is for viewing the plot of your cost history.
   """
    
   cost_df = pandas.DataFrame({
      'Cost_History': cost_history,
      'Iteration': range(len(cost_history))
   })
    
   return ggplot(cost_df, aes('Iteration', 'Cost_History')) + geom_point() + ggtitle('Cost History for alpha = %.3f' % alpha )


dataframe = pandas.read_csv('turnstile_data_master_with_weather.csv')
predictions = predictions(dataframe)
