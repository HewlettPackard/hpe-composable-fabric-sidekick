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
from pyhpecfm.auth import CFMClient
from pyhpecfm import fabric
from pyhpecfm import system
import pprint

# Authenticat to the controllerx
c=CFMClient('172.18.1.66', 'admin','plexxi')

try:
    cfm_audits = system.get_audit_logs(c)
except:
    error = "ERR-LOGIN - Failed to log into CFM controller"
    print error

# Set some counters
c = 0
x = 0

# Loop through cfm_audits and process ALARMS
for i in cfm_audits:

    try:
        typex = cfm_audits[c]['record_type']
    except:
        typex = '-'

    if typex == 'EVENT':
        print typex
        x = x + 1
    c = c + 1
print (' {0} events were discovered ' .format(str(x)))
