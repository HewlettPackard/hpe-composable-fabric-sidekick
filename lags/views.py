# -*- coding: utf-8 -*-
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
#
#   a python module that handles the link-aggregation API call to the CFM controller
#
#---------------------------------------------------------------------------------------
from flask import Blueprint, render_template, request, redirect, session, url_for, abort
import os
from werkzeug import secure_filename
from mongoengine import Q
import pygal
import json

# Place to stach the user temporarily
from database.sidekick import Sidekick
from pyhpecfm.client import CFMClient
from pyhpecfm import fabric
from pyhpecfm import system

lag_app = Blueprint('lag_app', __name__)

@lag_app.route('/process_lags', methods=('GET', 'POST'))
def process_lags():

    # Get user informaation..
    creds = Sidekick.objects.first()
    username=creds.user
    username=username.encode('utf-8')
    ipaddress=creds.ipaddress
    ipaddress=ipaddress.encode('utf-8')
    password=creds.passwd
    password=password.encode('utf-8')
    #append.rick('fail')

    # Create client connection
    client = CFMClient(ipaddress, username, password)
    client.connect()

    # assignment of attributes
    count_only=False
    mac_attachments=True
    mac_learning=True
    ports=True
    port_type='access'
    tags=True
    type='provisioned'
    vlan_groups=True
    # Create an attribute dictionary
    params = {
                'count_only': count_only,
                'mac_attachments': mac_attachments,
                'mac_learning': mac_learning,
                'ports': ports,
                'port_type': port_type,
                'tags': tags,
                'type': type,
                'vlan_groups': vlan_groups
              }

   # Pull the CFM controller for all lags
    try:
        cfm_lags = fabric.get_lags(client, params)
    except:
        error = "ERR-LOGIN - Failed to log into CFM controller"
        return error

    # build properties and ports disctionaries
    # Create some empty lists
    port_props=[]
    port_detail=[]
    lag_group=[]
    for lag in cfm_lags:
        if len(lag['port_properties']) > 1:

            # Iterate through port_properties
            for item in lag['port_properties']:
                lag_mode=item['lacp']['mode']
                lag_speed=item['speed']['current']
                lag_partner_status=item['port_lacp_state'][0]['partner_state_lacp_status']
                lag_partner_system=item['port_lacp_state'][0]['partner_state_system_id']
                lag_partner_port_state=item['port_lacp_state'][0]['partner_state_port']
                actor_lacp_status=item['port_lacp_state'][0]['actor_state_lacp_status']
                # Define properties dictionary
                properties={
                     'mode':lag_mode,
                     'speed':lag_speed,
                     'partner_status':lag_partner_status,
                     'partner_system':lag_partner_system,
                     'partner_port_state':lag_partner_port_state,
                     'actor_status':actor_lacp_status
                    }

                # Extract port detail.
                for ports in item['ports']:
                    switch_name=ports['switch_name']
                    link_state=ports['link_state']
                    admin_state=ports['admin_state']
                    port_security_enabled=ports['port_security_enabled']
                    vlans=ports['vlans']
                    speed=ports['speed']
                    port_label=ports['port_label']
                    bridge_loop_detection=ports['bridge_loop_detection']
                # Define port dictionary
                port_information={
                    'switch_name': switch_name,
                    'link_state': link_state,
                    'admin_state': admin_state,
                    'port_security_enabled': port_security_enabled,
                    'vlans': vlans,
                    'speed': speed,
                    'port_label': port_label,
                    'bridge_loop_detection': bridge_loop_detection
                    }

                port_detail.append(port_information)
                #ports = {'ports':port_detail}
            #----add port detail to the dictionary items
            properties['ports'] = port_detail
            properties['name'] = lag['name']
            # Now make it a dictionary
            properties={'properties': properties}

            lag_group.append(properties)


        lag_data = []
        port_props = []
        port_detail=[]
    return render_template('lags/lags.html', l=lag_group)
