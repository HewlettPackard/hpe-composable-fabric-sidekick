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
from flask import Blueprint, render_template, request, redirect, session, url_for, abort
import os
from werkzeug import secure_filename
from mongoengine import Q
import pygal
import json

# Place to stach the user temporarily
from database.sidekick import Sidekick
from pyhpecfm.auth import CFMClient
from pyhpecfm import fabric
from pyhpecfm import system

alarm_app = Blueprint('alarm_app', __name__)

@alarm_app.route('/view_alarms', methods=('GET', 'POST'))
def view_alarms():

    # Get user informaation.
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

    try:
        cfm_audits = system.get_audit_logs(client)
    except:
        error = "ERR-LOGIN - Failed to log into CFM controller"
        return error

    # Create a empty list for alarms
    alarm_data = []

    # Set some counters
    c = 0
    x = 0

    # Loop through cfm_audits and process ALARMS

    for i in cfm_audits:

        try:
            typex = cfm_audits[c]['record_type']
        except:
            typex = '-'

        if typex == 'ALARM':

            try:
                eventType = cfm_audits[c]['data']['event_type']
            except:
                eventType = '-'

            try:
                sev = cfm_audits[c]['severity']
            except:
                sev = '-'

            try:
                desc = cfm_audits[c]['description']
            except:
                desc = '-'

            # Build dictionary to add to list
            out = [eventType,typex,sev,desc]
            alarm_data.append(out)

        c = c + 1

    return render_template('alarms/alarms.html', a = alarm_data)
