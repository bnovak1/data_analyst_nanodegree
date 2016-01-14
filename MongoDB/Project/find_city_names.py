import xml.etree.cElementTree as ET


def city_names(osmfile):
    
    osm_file = open(osmfile, "r")
    
    cities = []
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        
        if elem.tag == "node" or elem.tag == "way":
            
            for tag in elem.iter("tag"):
                
                if tag.attrib['k'] == "addr:city":
                    city_name = tag.attrib['v']
                    if city_name not in cities:
                        cities.append(city_name)
                        
    return cities
                    
if __name__ == '__main__':
    
    cities = city_names('Baton_Rouge.osm')
    
    print 'Cities included in the data:\n'
    for city in cities:
        print city