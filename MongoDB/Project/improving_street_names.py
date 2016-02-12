"""
- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
- the update_name function fixes the street name
    The function takes a string with street name as an argument and returns the fixed name
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "Baton_Rouge.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Thruway", "Highway", "Circle"]

mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Rd": "Road",
            "Ave": "Avenue",
            "Ln": "Lane",
            "Dr": "Drive",
            "dr": "Drive",
            "Blvd": "Boulevard",
            "Hwy": "Highway"
            }

def int_check(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected and int_check(street_type) == False:
            street_types[street_type].add(street_name)
              

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    
    nstreets = 0
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        
        if elem.tag == "node" or elem.tag == "way":
            
            for tag in elem.iter("tag"):
                
                if is_street_name(tag):
                    nstreets += 1
                    audit_street_type(street_types, tag.attrib['v'])
                    
    print 'There are ' + str(nstreets) + ' streets in the data set'
    print
                    
    return street_types


def update_name(name, mapping):
    
    street_type = street_type_re.search(name).group()
    name = re.sub(r'\b\S+\.?$', mapping[street_type], name)

    return name


if __name__ == '__main__':
    st_types = audit(OSMFILE)

    print 'Street names with abbreviated types:\n'
    nfixed = 0
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            nfixed += 1
    
    print
    print str(nfixed) + ' street name abbreviations were found'