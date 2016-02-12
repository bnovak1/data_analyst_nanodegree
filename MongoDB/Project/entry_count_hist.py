import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from tabulate import tabulate
   
def get_db(db_name):
    
    from pymongo import MongoClient    
    client = MongoClient('localhost:27017')
    
    db = client[db_name]
    
    return db


def make_pipeline():
    '''
    Create aggregation pipeline to group by users and count the number of entries for each user,
    then group by the number of entries for each user and count the number of users with each number of entries,
    then sort in ascending order.
    '''

    pipeline = [{'$group':{'_id':'$created.user', 'count':{'$sum':1}}},
                {'$group':{'_id':'$count', 'nusers':{'$sum':1}}},
                {'$sort':{'_id':1}}]

    return pipeline
    

def plot_hist(entry_hist):
    '''
    Plot the number of users for different numbers of entries. Ignore large numbers of entries where the
    number of users is only 1.
    '''
    
    num_entries = []
    num_users = []
    
    for n in entry_hist:
        num_entries.append(n['_id'])
        num_users.append(n['nusers'])
        
    num_entries = np.array(num_entries)
    num_users = np.array(num_users)
    percent_users_less = 100.0*np.cumsum(num_users)/np.sum(num_users)
    
    mpl.rcParams['font.size'] = 10
    
    ind = np.where(num_users > 1)[0][-1]
    plt.plot(num_entries[0:ind+1], percent_users_less[0:ind+1], '.-')
    
    plt.xlabel(r'Number of entries')
    plt.xlim(-5, 350)
    plt.axes().xaxis.set_major_locator(MultipleLocator(30))
    plt.axes().xaxis.set_minor_locator(MultipleLocator(10))    
    
    plt.ylabel(r'\% of users with $\le$ number of entries')
    plt.ylim(10, 85)
    plt.axes().yaxis.set_minor_locator(MultipleLocator(5))
    
    plt.title('Percentage of users with a given number of entries or fewer.\n\
    Numbers of entries are only shown for the largest number\n\
    of entries associated with 2 or more users.')
    
    plt.show()
    
    print tabulate(np.column_stack((num_entries[0:21], num_users[0:21], percent_users_less[0:21])), 
                   headers=['# Entries', '# Users', '% Users with # Entries or Fewer'])
    

if __name__ == "__main__":

    db = get_db('OSM')
    pipeline = make_pipeline()
    entry_hist = db.Baton_Rouge_LA_US_area.aggregate(pipeline)
    plot_hist(entry_hist)
