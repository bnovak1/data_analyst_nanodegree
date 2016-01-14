import numpy
import pandas

def compute_cost(features, values, theta):
    """
    Compute the cost of a list of parameters, theta, given a list of features 
    (input data points) and values (output data points).
    """
    npoints = len(values)
    sum_of_square_errors = numpy.square(numpy.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*npoints)

    return cost

def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.
    """

    # Write code here that performs num_iterations updates to the elements of theta.
    # times. Every time you compute the cost for a given list of thetas, append it 
    # to cost_history.
    # See the Instructor notes for hints.
    
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
        values_predicted = numpy.dot(features, theta)
        theta = theta + (alpha/npoints)*(numpy.dot(values - values_predicted,features))

    return theta, pandas.Series(cost_history) # leave this line for the grader
