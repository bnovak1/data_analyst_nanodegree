import xml.etree.ElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
Before you process the data and add it into MongoDB, you should
check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data model
and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with problematic characters.
Please complete the function 'key_type'.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    
    if element.tag == "tag":
        
        key = element.attrib['k']
        
        if lower.search(key) != None:
            keys['lower'] += 1
            lower_file.write(key + '\n')
        elif lower_colon.search(key) != None:
            keys['lower_colon'] += 1
            lower_colon_file.write(key + '\n')
        elif problemchars.search(key) != None:
            keys['problemchars'] += 1
            problemchars_file.write(key + '\n')
        else:
            keys['other'] += 1
            other_file.write(key + '\n')
            
    return keys


def process_map(filename):

    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}

    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


if __name__ == "__main__":

    lower_file = open('lower_tags.dat', 'w')
    lower_colon_file = open('lower_colon_tags.dat', 'w')
    problemchars_file = open('problemchars_tags.dat', 'w')
    other_file = open('other_tags.dat', 'w')

    keys = process_map('Baton_Rouge.osm')
    pprint.pprint(keys)
    
    print
    print str(keys['problemchars']) + ' tags were found with problematic characters'

    lower_file.close()
    lower_colon_file.close()
    problemchars_file.close()
    other_file.close()
