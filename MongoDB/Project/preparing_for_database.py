import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
"""
1. Fixes street types which are abbreviated

2. Transforms the shape of the data into:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

The transformed data is saved to a JSON file, so that mongoimport can be used later 
on to import the shaped data into MongoDB.

In particular the following things are done:
- Ony "node" and "way" top level tags are processed
- all attributes of "node" and "way" are turned into regular key/value pairs, except:
    - attributes in the CREATED array are added under a key "created"
    - attributes for latitude and longitude are added to a "pos" array,
      for use in geospacial indexing. 
- if second level tag "k" value contains problematic characters, it is ignored
- if second level tag "k" value starts with "addr:", it is added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", it is
  processed the same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag is ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  is turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

street_types_expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", 
                        "Square", "Lane", "Road", "Trail", "Parkway", "Commons", 
                        "Thruway", "Highway", "Circle"]

street_type_mapping = { "St": "Street",
                        "St.": "Street",
                        "Rd.": "Road",
                        "Rd": "Road",
                        "Ave": "Avenue",
                        "Ln": "Lane",
                        "Dr": "Drive",
                        "dr": "Drive",
                        "Blvd": "Boulevard",
                        "Hwy": "Highway"}

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
two_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def int_check(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


def update_street_type_name(name, street_types_expected, street_type_mapping):
    '''
    convert street type name abbreviations to full names
    '''
    
    street_type = street_type_re.search(name).group()
    
    if not int_check(street_type) and street_type not in street_types_expected:
        name = re.sub(r'\b\S+\.?$', street_type_mapping[street_type], name)
        print name

    return name
    
    
def shape_element(element):
    
    node = {}
    
    if element.tag == "node" or element.tag == "way":
        
        node['type'] = element.tag
        node['id'] = element.attrib['id']
        
        if 'visible' in element.attrib:
            node['visible'] = element.attrib['visible']
        
        node['created'] = {'version':element.attrib['version'], 
                           'changeset':element.attrib['changeset'], 
                           'timestamp':element.attrib['timestamp'],
                           'user':element.attrib['user'],
                           'uid':element.attrib['uid']}
        
        if node['type'] == 'node':
            node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]
        
        address = {}
        for tag in element.iter('tag'):
            
            key = tag.attrib['k']
            
            if problemchars.search(key) == None:
                
                key_split = key.split(':')
                key_split_len = len(key_split)
                
                if key_split_len > 1:
                    
                    if key_split[0] == 'addr':
                        
                        if key_split_len == 2:
                            
                            address_key = key_split[1]
                            address_value = tag.attrib['v']

                            # If street name, fix street type if abbreviated                            
                            if address_key == 'street':
                                address_value = update_street_type_name(address_value, 
                                                                        street_types_expected, 
                                                                        street_type_mapping)
                                
                            address[address_key] = address_value
                            
                    else:
                        
                        node[key] = tag.attrib['v']
                        
                else:
                    
                    node[key] = tag.attrib['v']
                
        if len(address) > 0:
            node['address'] = address
            
        if node['type'] == 'way':
            node_refs = []
            for nd in element.iter('nd'):
                node_refs = node_refs + [nd.attrib['ref']]
            node['node_refs'] = node_refs
            
        return node

    else:
    
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('../DATA/example.osm')
    #pprint.pprint(data)
    
    correct_first_elem = {
        "id": "261114295", 
        "visible": "true", 
        "type": "node", 
        "pos": [41.9730791, -87.6866303], 
        "created": {
            "changeset": "11129782", 
            "user": "bbmiller", 
            "version": "7", 
            "uid": "451048", 
            "timestamp": "2012-03-28T18:31:23Z"
        }
    }
    assert data[0] == correct_first_elem
    assert data[-1]["address"] == {
                                    "street": "West Lexington St.", 
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
                                    "2199822370", "2199822284", "2199822281"]

if __name__ == "__main__":
    process_map('Baton_Rouge.osm')