import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_db(db_name):
    
    from pymongo import MongoClient    

    client = MongoClient('localhost:27017')
    
    db = client[db_name]
    
    return db


def get_sections(db, nsec_lat, nsec_long):
    '''
    Get the latitudes and longitudes at the edges of the sections.
    These sections will not have precisely the same area due to curvature, 
    but this is a reasonable approximation for small areas.
    '''

    # get position data
    cursor = db.Baton_Rouge_LA_US_area.find({}, {'_id':0, 'pos':1})

    # get min and max latitude and longitude in the data
    cnt = 0    
    for document in cursor:
        
        if 'pos' in document:
        
            latitude = document['pos'][0]
            longitude = document['pos'][1]
    
            if cnt == 0:
                latitude_min = latitude
                latitude_max = latitude
                longitude_min = longitude
                longitude_max = longitude
            else:
                latitude_min = min(latitude, latitude_min)
                latitude_max = max(latitude, latitude_max)
                longitude_min = min(longitude, longitude_min)
                longitude_max = max(longitude, longitude_max)
            
        cnt += 1
        
    # calculate widths of sections
    secwidth_lat = (latitude_max - latitude_min)/float(nsec_lat)
    secwidth_long = (longitude_max - longitude_min)/float(nsec_long)
        
    # calculate edges of the sections
    boundaries = np.empty((nsec_lat*nsec_long, 4))
    cnt = 0
    for isec_lat in range(nsec_lat):
        for isec_long in range(nsec_long):
            boundaries[cnt, 0] = latitude_min + isec_lat*secwidth_lat
            boundaries[cnt, 1] = boundaries[cnt, 0] + secwidth_lat
            boundaries[cnt, 2] = longitude_min + isec_long*secwidth_long
            boundaries[cnt, 3] = boundaries[cnt, 2] + secwidth_long
            cnt += 1
            
    return boundaries
    
    
def count_buildings(db, boundaries, building_type=None):
    '''
    Find number of buildings of type building_type in each section defined by
    boundaries. If building_type is not specified, find the total number of 
    buildings in each section defined by boundaries.
    '''
    
    nsections = boundaries.shape[1]
    
    building_count = np.zeros(nsections)
    
    if building_type:
        cursor_building = \
            db.Baton_Rouge_LA_US_area.find({'building': building_type},
                                           {'_id': 0, 'pos': 1, 'node_refs': 1})
    else:
        cursor_building = \
            db.Baton_Rouge_LA_US_area.find({'building': {'$regex': r'^.'}},
                                           {'_id': 0, 'building': 1, 'pos': 1, 
                                            'node_refs': 1})
        building_type_counts = {}
        
    for document_building in cursor_building:

        # Count of buildings of each type
        if 'building' in document_building:
            
            bt = document_building['building']
            
            if bt in building_type_counts:
                building_type_counts[bt] += 1
            else:
                building_type_counts[bt] = 1

        if 'pos' in document_building:
        
            latitude = document_building['pos'][0]
            longitude = document_building['pos'][1]
        
        else:

            latitude = 0.0
            longitude = 0.0
            
#            noderefs = list(set(document_building['node_refs']))
            noderef = list(set(document_building['node_refs']))[0]
            
#            cursor_node = db.Baton_Rouge_LA_US_area.find({'$and':\
#                                                [{'type': 'node'}, 
#                                                 {'id': {'$in': noderefs}}]})                
            cursor_node = db.Baton_Rouge_LA_US_area.find({'$and':\
                                                [{'type': 'node'}, 
                                                 {'id': noderef}]})
                
            nnodes = 0
            for document_node in cursor_node:
                latitude += document_node['pos'][0]
                longitude += document_node['pos'][1]
                nnodes += 1

            latitude /= float(nnodes)
            longitude /= float(nnodes)
            
        for isection in range(nsections):
                
            if latitude >= boundaries[isection, 0] and \
               latitude <= boundaries[isection, 1] and \
               longitude >= boundaries[isection, 2] and \
               longitude <= boundaries[isection, 3]:
                    building_count[isection] += 1
                    break

    if building_type:
        return building_count
    else:
        return (building_count, building_type_counts)
    

if __name__ == "__main__":

    # Database
    db = get_db('OSM')
    
    # Get quadrant boundaries
    boundaries = get_sections(db, 2, 2)
    
    # Count the total number of buildings
    (building_count, building_type_counts) = count_buildings(db, boundaries)
    
    # Save
    output = np.column_stack((boundaries, building_count))
    output = pd.DataFrame(output, columns=['latitude min', 'latitude max',
                                           'longitude min', 'longitude max',
                                           'count'])
    pd.DataFrame.to_csv(output, 'building_count.dat', sep=' ')
    
    output = pd.DataFrame.from_dict(building_type_counts, orient='index')
    pd.DataFrame.to_csv(output, 'building_type_counts.dat', sep=' ', 
                        header=False)
    
    n_building_types = len(building_type_counts)
    plt.bar(range(n_building_types), building_type_counts.values(), 
        align='center')
    plt.xticks(range(n_building_types), list(building_type_counts.keys()))
    plt.show()
    plt.close()
    