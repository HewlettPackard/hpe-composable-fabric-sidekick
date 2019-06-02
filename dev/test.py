# (C) Copyright 2019 Hewlett Packard Enterprise Development LP.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# __author__ = "@netwookie"
# __credits__ = ["Rick Kauffman"]
# __license__ = "Apache2.0"
# __version__ = "1.0.0"
# __maintainer__ = "Rick Kauffman"
# __email__ = "rick.a.kauffman@hpe.com"

import json
from pyhpecfm.auth import CFMClient
from pyhpecfm import fabric
from pyhpecfm import system
import pprint

# Authenticat to the controller
c=CFMClient('172.18.1.66', 'admin','plexxi')

try:
    cfm_fabrics = fabric.get_fabrics(c)
except:
    error = "ERR-LOGIN - Failed to log into CFM controller"
    print error

pp = pprint.PrettyPrinter(indent=4)

pp.pprint(cfm_fabrics)

'''
# Set some counters
c = 0
x = 0

# Set a blank list to store disctionaries
fabric_data = []

# Loop through cfm_fabrics and process IPZ
for i in cfm_fabrics:

    try:
        desc = cfm_fabrics[c]['description']
        if desc == '':
            desc = 'HPE Composable Fabric'

    except:
        desc = 'HPE Composable Fabric'

    try:
        fab_uuid = cfm_fabrics[c]['fabric_uuid']
    except:
        fab_uuid = '-unknown'

    try:
        name = cfm_fabrics[c]['name']
    except:
        name = '-unknown'

    try:
        mode = cfm_fabrics[c]['mode']
    except:
        mode = '-unknown'

    try:
        sub_address = cfm_fabrics[c]['subnet']['address']
    except:
        sub_address = '-unknown'

    try:
        sub_prefix = cfm_fabrics[c]['subnet']['address']
    except:
        sub_prefix = '-unknown'


    out ={
            'u_desc':desc,
            'u_stable':fab_uuid,
            'u_name':name,
            'u_mode':mode,
            'u_sub_address':sub_address,
            'u_sub_prefix':sub_prefix
          }
    fabric_data.append(out)

    #print(json.dumps(joe, sort_keys=True, indent=4))

    x = x + 1
    print out
    c = c + 1
print fabric_data
print (' {0} cfm_fabrics were discovered ' .format(str(x)))
print ('>{0}< this is desc' .format(desc))
'''
