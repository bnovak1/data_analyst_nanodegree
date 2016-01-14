from find_city_names import city_names
import xml.etree.cElementTree as ET

def get_county_ids_geonames(cities, geonames_file, state='Louisiana'):
    '''
    Use GeoNames data from http://download.geonames.org/export/zip/US.zip to create a dictionary 
    containing cities in the OSM data as keys and lists of county id numbers corresponding to the cities as values.
    '''
    
    # Read GeoNames file
    geo_file = open(geonames_file, 'r')    
    geonames_data = geo_file.readlines()

    # Initialize dictionary for county id numbers
    county_id_lists = {}
    
    for line in geonames_data:
        
        # Split line based on spaces
        line_data = line.split()
        
        # Check if the line is for the correct state
        if state in line_data:

            # Get the city name
            # The first two fields contain no spaces
            # The city name goes from the third element to just before the state name
            ind = line_data.index(state)
            city = ' '.join(line_data[2:ind])
            
            # Check if city is in list of cities from OSM data
            if city in cities:
                
                line_len = len(line_data)
                
                # county id number is the 3rd from the last field & the 3rd from the last element in line_data
                county_id = int(line_data[line_len-3])

                # Check if city is in county_id_lists. Add the city and county id number if not.
                if city not in county_id_lists:
                    county_id_lists[city] = [county_id]
                
                # Check if county id number is in list for city. Add the county id number if not.
                elif county_id not in county_id_lists[city]:
                    county_id_lists[city].append(county_id)
                    
    return county_id_lists


def get_county_ids_osm(osmfile):
    '''
    Use OSM data to create a dictionary containing cities in the data as keys and unique lists of 
    county id numbers for the cities as values.
    '''
    
    # Open OSM file
    osm_file = open(osmfile, "r")
    
    # Initialize dictionary for county id numbers
    county_id_lists = {}
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        
        # Initialize city and county id number
        city_name = ''
        county_id = -1
        
        # Check nodes and ways
        if elem.tag == "node" or elem.tag == "way":
            
            # Look at tags in nodes and ways
            for tag in elem.iter("tag"):
                
                # City name                
                if tag.attrib['k'] == "addr:city":
                    city_name = tag.attrib['v']
                
                # County/county id  
                if tag.attrib['k'] == "gnis:county_id":
                    county_id = int(tag.attrib['v'])
        
        # Check that both the city name and county id number have been assigned
        if city_name != '' and county_id > 0:

            # If the city name is not in county_id_lists, then add the city name and county id number.
            if city_name not in county_id_lists:
                county_id_lists[city_name] = [county_id]

            # If county id number is not in county_id_lists[city_name], then add the county id number.
            elif county_id not in county_id_lists[city_name]:
                county_id_lists[city_name].append(county_id)
                
    return county_id_lists


def check_county_ids(county_id_lists_geonames, county_id_lists_osm):
    '''
    Check OSM county id numbers against geonames data (http://download.geonames.org/export/zip/US.zip)
    '''
    
    # Initialize a dictionary for problem county id numbers
    problem_county_ids = {}
    
    # Loop over cities in OSM data
    for city_name in county_id_lists_osm:

        # Loop over county id numbers for each city in OSM data
        for county_id in county_id_lists_osm[city_name]:
            
            # County id numbers for the city from the GeoNames data
            county_ids_geonames = county_id_lists_geonames[city_name]
            
            # If the county id number is not in the GeoNames data for the city, there is a problem
            # Save city and county id number to problem_county_ids
            if county_id not in county_ids_geonames:
                if city_name not in problem_county_ids:
                    problem_county_ids[city_name] = [county_id]
                else:
                    problem_county_ids[city_name].append(county_id)

    return problem_county_ids


if __name__ == '__main__':

    # list of cities from OSM data
    cities = city_names('Baton_Rouge.osm')

    # county id numbers from geonames data
    county_id_lists_geonames = get_county_ids_geonames(cities, 'US_zip_codes.txt')

    # county id numbers from OSM data
    county_id_lists_osm = get_county_ids_osm('Baton_Rouge.osm')

    # check for consitency between cities and county id numbers in OSM data
    problem_county_ids = check_county_ids(county_id_lists_geonames, county_id_lists_osm)
    if len(problem_county_ids) > 0:
        print problem_county_ids
    else:
        print "No problems with county id numbers"    