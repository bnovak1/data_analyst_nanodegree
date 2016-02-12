from find_city_names import city_names
import xml.etree.cElementTree as ET


def get_zip_codes_geonames(cities, geonames_file, state='Louisiana'):
    '''
    Use geonames data from http://download.geonames.org/export/zip/US.zip to create a dictionary 
    containing cities in the OSM data as keys and lists of geonames zipcodes for the cities as values.
    '''
    
    geo_file = open(geonames_file, 'r')
    
    zip_code_lists = {}
    
    geonames_data = geo_file.readlines()
    
    for line in geonames_data:
        
        line_data = line.split()
        
        if state in line_data:
            ind = line_data.index(state)
            city = ' '.join(line_data[2:ind])
            
            if city in cities:
                
                zip_code = line_data[1]
                
                if city not in zip_code_lists:
                    zip_code_lists[city] = [int(zip_code)]
                elif zip_code not in zip_code_lists[city]:
                    zip_code_lists[city].append(int(zip_code))
                    
    return zip_code_lists


def get_zip_codes_osm(osmfile):
    '''
    Use OSM data to create a dictionary containing cities in the data as keys and unique lists of 
    zipcodes for the cities as values.
    '''
    
    osm_file = open(osmfile, "r")
    
    zip_code_lists = {}
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        
        city_name = ''
        zip_code = -1
        
        if elem.tag == "node" or elem.tag == "way":
            
            for tag in elem.iter("tag"):
                                
                if tag.attrib['k'] == "addr:city":
                    city_name = tag.attrib['v']
                    
                if tag.attrib['k'] == "addr:postcode":
                    zip_code = int(tag.attrib['v'])
        
        if city_name != '' and zip_code > 0:
            if city_name not in zip_code_lists:
                zip_code_lists[city_name] = [zip_code]
            elif zip_code not in zip_code_lists[city_name]:
                zip_code_lists[city_name].append(zip_code)
                
    return zip_code_lists


def check_zip_codes(zip_code_lists_geonames, zip_code_lists_osm):
    '''
    Check zip codes against geonames data (http://download.geonames.org/export/zip/US.zip)
    '''
    
    problem_zip_codes = {}
    
    for city_name in zip_code_lists_osm:
        for zip_code in zip_code_lists_osm[city_name]:
            
            zip_codes_geonames = zip_code_lists_geonames[city_name]
            
            # If the zip code is not in the GeoNames data for the city, there is a problem
            # Save city and zip code to problem_zip_codes           
            if zip_code not in zip_codes_geonames:
                if city_name not in problem_zip_codes:
                    problem_zip_codes[city_name] = [zip_code]
                else:
                    problem_zip_codes[city_name].append(zip_code)

    return problem_zip_codes
                
                    
if __name__ == '__main__':
    
    # list of cities from OSM data
    cities = city_names('Baton_Rouge.osm')
    
    # zip codes from geonames data
    zip_code_lists_geonames = get_zip_codes_geonames(cities, 'US_zip_codes.txt')
    
    # zip codes from OSM data
    zip_code_lists_osm = get_zip_codes_osm('Baton_Rouge.osm')

    # check zip codes
    problem_zip_codes = check_zip_codes(zip_code_lists_geonames, zip_code_lists_osm)
    if len(problem_zip_codes) > 0:
        print problem_zip_codes
    else:
        print "No problems with zip codes"
