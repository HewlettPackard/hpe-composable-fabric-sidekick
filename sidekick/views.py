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

from flask import Blueprint, render_template, request, redirect, session, url_for, abort, flash
import os
from werkzeug import secure_filename
from mongoengine import Q
import datetime
from database.models import Database
from database.forms import DatabaseForm
from database.temp import Temp
from database.number import Number
from database.switches import Switches
from database.sidekick import Sidekick
import pygal
from pygal.style import LightGreenStyle

sidekick_app = Blueprint('sidekick_app', __name__)

@sidekick_app.route('/newentry', methods=('GET', 'POST'))
def newentry():
    '''
    Adds a new entry to the database
    Reads form variables, creates an entry and
    saves it to the mongo database..

    '''
    # Get user
    user = Sidekick.objects.first()
    user = user.user.encode('utf-8')

    # Get time date stamp
    now = datetime.datetime.now()
    now = now.isoformat()


    # Get next record number
    num = Number.objects.first()
    num = num.num
    more = [user,now,num]

    # rick.append('fail')
    error='none'
    form = DatabaseForm()
    if form.validate_on_submit():
        message=form.message.data
        concern=form.concern.data

        message = message.encode('utf-8')
        concern = concern.encode('utf-8')

        # Build record to write to mongo database

        entry = Database(user=user,message=message,concern=concern,now=now,num=num)
        #rick.append('faiul')

        # Save the record
        try:
            entry.save()
        except:
            "ERR002 - saving new event form to database"
            return render_template('sidekick/dberror.html',error=error)

        # Increment number for next use
        num = num + 1

        # Clear temp database for a new session
        Number.objects().delete()

        # write the new number
        update = Number(num=num)

        # Save the number record for the next use
        try:
            update.save()
        except:
            error = "ERR-003 - event number not increased"
            return render_template('sidekick/dberror.html', error=error)


        return render_template('sidekick/crud-goodsavedentry.html')
    return render_template('sidekick/crud-new.html', form=form, more=more)

@sidekick_app.route('/editentry', methods=('GET', 'POST'))
def editentry():
    '''
    Edit an existing entry from the database

    '''
    if request.method == 'POST':
        # Get desired project
        num = request.form['num']
        # PDelete the record from mongo database
        entry = Database.objects(num=num)

        # create list from database entry
        more = {
                "num" : entry[0].num,
                "now" : entry[0].now,
                "user" : entry[0].user,
                "message" : entry[0].message,
                "concern" : entry[0].concern
                }
        # rick.append('fail')
        #send form with info list
        return render_template('sidekick/crud-editentry.html', more=more)

    # Get user
    user = Sidekick.objects.first()
    user = user.user.encode('utf-8')


    entries = []
    for e in Database.objects():
        if e.user == user:
            entries.append(e.num)
    return render_template('sidekick/crud-editselect.html', entries=entries)

@sidekick_app.route('/upentry', methods=('GET', 'POST'))
def upentry():
    '''
    Saves the edited record

    '''
    # Get desired project
    num = request.form['num']
    now = request.form['now']
    user = request.form['user']
    message = request.form['message']
    concern = request.form['concern']

    now = now.encode('utf-8')
    user = user.encode('utf-8')
    message = message.encode('utf-8')
    concern = concern.encode('utf-8')
    num = int(num)

    # Save the number record for the next use

    try:
        Database.objects(num=num).update(message=message,concern=concern)
    except:
        error = "ERR005 - Failed to update edited log entry"
        return render_template('sidekick/dberror.html')

    #send delete success
    return render_template('sidekick/crud-goodeditentry.html')



@sidekick_app.route('/deleteentry', methods=('GET', 'POST'))
def deleteentry():
    '''
    Delete an existing entry from the database

    '''
    if request.method == 'POST':
        # Get desired project
        num = request.form['num']
        # PDelete the record from mongo database
        try:
            Database.objects(num=num).delete()
        except:
            eorror = "ERR-004 Failed to delete log entry"
            return render_template('sidekick/dberror.html', error=error)

        #send delete success
        return render_template('sidekick/crud-deleteentry.html')

    # Build list of projects in database and send to selector form

    # Get user
    user = Sidekick.objects.first()
    user = user.user.encode('utf-8')


    entries = []
    for e in Database.objects():
        if e.user == user:
            entries.append(e.num)
    return render_template('sidekick/crud-deleteselect.html', entries=entries)

@sidekick_app.route('/listentry', methods=('GET', 'POST'))
def listentry():
    '''
    List all entries from the database by SA

    '''
    # Get user
    user = Sidekick.objects.first()
    user = user.user.encode('utf-8')


    entries = []
    for e in Database.objects():
        if e.user == user:
            entries.append(e)
    return render_template('sidekick/crud-list.html', entries=entries)


@sidekick_app.route('/cloneentry', methods=('GET', 'POST'))
def cloneentry():
    '''
    Clone an existing entry from the database

    '''
    if request.method == 'POST':
        # Get desired project
        num = request.form['num']
        # PDelete the record from mongo database
        entry = Database.objects(num=num)

        # Get next record number
        num = Number.objects.first()
        num = num.num

        # Get time date stamp
        now = datetime.datetime.now()
        now = now.isoformat()


        # create list from database entry
        more = {
                "num" : num,
                "now" : now,
                "user" : entry[0].user,
                "message" : entry[0].message,
                "concern" : entry[0].concern
                }


        #send form with info list
        return render_template('sidekick/crud-cloneentry.html', more=more)
    # Get user
    user = Sidekick.objects.first()
    user = user.user.encode('utf-8')

    entries = []
    for e in Database.objects():
        if e.user == user:
            entries.append(e.num)
    return render_template('sidekick/crud-cloneselect.html', entries=entries)


@sidekick_app.route('/upclone', methods=('GET', 'POST'))
def upclone():
    '''
    Saves the cloned record

    '''
    # Get desired project
    num = request.form['num']
    now = request.form['now']
    user = request.form['user']
    message = request.form['message']
    concern = request.form['concern']

    now = now.encode('utf-8')
    user = user.encode('utf-8')
    message = message.encode('utf-8')
    concern = concern.encode('utf-8')
    num = int(num)
#
    # Build record to write to mongo database

    entry = Database(user=user,message=message,concern=concern,now=now,num=num)
    #rick.append('faiul')

    # Save the record
    try:
        entry.save()
    except:
        error = "Clone save issues"
        return render_template('sidekick/dberror.html',error=error)

    # Increment number for next use
    num = num + 1

    # Clear temp database for a new session
    Number.objects().delete()

    # write the new number
    update = Number(num=num)

    # Save the number record for the next use
    try:
        update.save()
    except:
        error = "ERR007 Proble saving updated page index from clone"
        return render_template('sidekick/dberror.html', error=error)

    return render_template('sidekick/crud-goodcloneentry.html')


@sidekick_app.route('/newterm', methods=('GET', 'POST'))
def newterm():
    '''
    Saves the cloned record

    '''
    os.system("mate-terminal")
    # Return Main menu
    # Get user informaation
    creds = Sidekick.objects.first()
    user = creds.user
    ipaddress= creds.ipaddress

    # Insert chart data

    try:
        from pygal.style import DarkSolarizedStyle
        g1 = pygal.StackedLine(fill=True, interpolate='cubic', style=DarkSolarizedStyle)
        g1.add('A', [1, 3,  5, 16, 13, 3,  7])
        g1.add('B', [5, 2,  3,  2,  5, 7, 17])
        g1.add('C', [6, 10, 9,  7,  3, 1,  0])
        g1.add('D', [2,  3, 5,  9, 12, 9,  5])
        g1.add('E', [7,  4, 2,  1,  2, 10, 0])
        g1_data = g1.render_data_uri()
    except Exception, e:
		return(str(e))

    try:
        line_chart = pygal.HorizontalBar()
        line_chart.title = 'Browser usage in February 2012 (in %)'
        line_chart.add('IE', 19.5)
        line_chart.add('Firefox', 36.6)
        line_chart.add('Chrome', 36.3)
        line_chart.add('Safari', 4.5)
        line_chart.add('Opera', 2.3)
        line_chart.render()
        g2_data = line_chart.render_data_uri()
    except Exception, e:
		return(str(e))

    # Get switch information switch database
    switch_array = []
    for s in Switches.objects():
        # assigne local variables
        health = s.health
        ip_address = s.ip_address
        mac_address = s.mac_address
        name = s.name
        sw_version = s.sw_version
        # Creat a list for the record entry
        out=[health, ip_address, mac_address, name, sw_version]
        # Make a list of Lists
        switch_array.append(out)

    return render_template('main/sidekick1.html', u=user, i=ipaddress, g1_data=g1_data, g2_data=g2_data, s = switch_array)

@sidekick_app.route('/newprod', methods=('GET', 'POST'))
def newprod():
    '''
    Saves the cloned record

    '''
    return render_template('sidekick/crud-prodlist.html')
