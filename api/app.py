#!flask/bin/python
from flask import Flask, abort, request, jsonify, send_file
import os
import io
import zipfile
import time
import ast
import json
import tempfile
from urllib.request import urlretrieve
from os.path import basename

import mysql.connector

app = Flask(__name__)

def connectToMySQL():
    global connection
    mysqlUser = os.environ.get('MYSQL_USER') or 'user'
    mysqlPassword = os.environ.get('MYSQL_PASSWORD') or 'password123'

    config = {
        'user': mysqlUser,
        'password': mysqlPassword,
        'host': 'db',
        'port': '3306',
        'database': 'gears'
    }

    try:
        connection = mysql.connector.connect(**config)
    except Exception as e:
        time.sleep(3)
        connectToMySQL()

connectToMySQL()

@app.route('/')
def test():
    cursor = connection.cursor()
    cursor.execute('show databases;')
    databases = str(cursor.fetchall())
    cursor.close()
    return databases, 200, {'ContentType': 'text/plain'}

@app.route('/api/register', methods=['POST'])
def register():
    #Connect to db, add phone info with UUID(model, friendly name, etc)
    # POST json
    # {
    #   "uuid": "SomeKindOfUniqueIDHere",
    #   "model": "Nexus 5X",
    #   "codename": "bullhead",
    #   "friendlyname": "SomeKindOfNameSetByUser",
    # }
    if not request.json or not 'uuid' in request.json:
        abort(400)
    # Do the database transactions
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM users WHERE id='{}';".format(request.json['uuid']))
    if cursor.rowcount is 0:
        cursor.execute("INSERT INTO users VALUES ('{}', '{}', '{}', '{}');".format(request.json['uuid'], request.json['model'], request.json['codename'], request.json['friendlyname']))
        connection.commit()
        cursor.close()
        return "Success", 400
    else:
        cursor.close()
        return "User Already Exists", 500
    cursor.close()
    return "Error", 500

@app.route('/api/poll', methods=['GET'])
def poll():
    if not request.args or not 'uuid' in request.args:
        abort(400)
    # Get info on if device is registered
    # We're looking for GET arg UUID mostly
    # return if it's registered, if it has restore points, and if it has overlays selected
    ret = {
            "isRegistered": False,
            "device": {
                "uuid": None,
                "model": None,
                "codename": None,
                "friendlyname": None
            },
            "hasSettingsRestores": False,
            "hasOverlays": False
        }
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM users WHERE id='{}' LIMIT 1;".format(request.args['uuid']))
    ret['isRegistered'] = cursor.rowcount is not 0
    if ret['isRegistered']:
        dev = cursor.fetchone()
        ret['device']['uuid'] = dev[0]
        ret['device']['model'] = dev[1]
        ret['device']['codename'] = dev[2]
        ret['device']['friendlyname'] = dev[3]
    cursor.execute("SELECT * FROM settings WHERE userid='{}' LIMIT 1;".format(request.args['uuid']))
    ret['hasSettingsRestores'] = cursor.rowcount is not 0
    cursor.execute("SELECT * FROM selectedoverlays WHERE userid='{}' LIMIT 1;".format(request.args['uuid']))
    ret['hasOverlays'] = cursor.rowcount is not 0
    cursor.close()

    return jsonify(ret), 200, {'ContentType': 'application/json'}

def isUserRegistered(uuid):
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM users WHERE id='{}' LIMIT 1;".format(uuid))
    return cursor.rowcount is not 0

@app.route('/api/pull/settings', methods=['GET'])
def pullSettings():
    if not request.args or not 'uuid' in request.args:
        abort(400)
    if not isUserRegistered(request.args['uuid']):
        abort(400)
    # Grab settings from DB, looking for GET arg UUID
    settings = {
        "global": { },
        "system": { },
        "secure": { }
    }
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM settings WHERE userid='{}' LIMIT 1;".format(request.args['uuid']))
    dev = cursor.fetchone()
    if dev[1] is not None:
        jason = json.loads(dev[1])
        settings['global'] = jason
    if dev[2] is not None:
        jason = json.loads(dev[2])
        settings['system'] = realJson
    if dev[3] is not None:
        jason = json.loads(dev[3])
        settings['secure'] = realJson
    cursor.close()
    return jsonify(settings), 200, {'ContentType': 'application/json'}

@app.route('/api/pull/overlays', methods=['GET'])
def pullOverlays():
    if not request.args or not 'uuid' in request.args:
        abort(400)
    if not isUserRegistered(request.args['uuid']):
        abort(400)
    # Grab overlay data from DB, looking for GET arg UUID
    overlays = [ ]
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM selectedoverlays WHERE userid='{}' LIMIT 1;".format(request.args['uuid']))
    overlaydata = cursor.fetchone()
    if overlaydata[1] is not None:
        jason = json.loads(overlaydata[1])
        for id in jason:
            overlay = {}
            overlay['id'] = id
            cursor.execute("SELECT * FROM overlays WHERE id='{}' LIMIT 1;".format(id))
            overlayInfo = cursor.fetchone()
            overlay['author'] = overlayInfo[1]
            overlay['name'] = overlayInfo[2]
            overlay['description'] = overlayInfo[3]
            overlay['url'] = overlayInfo[4]
            overlays.append(overlay)

    cursor.close()
    return jsonify(overlays), 200, {'ContentType': 'application/json'}

@app.route('/api/listoverlays', methods=['GET'])
def listOverlays():
    # Pulls all possible overlays from storage and sends then, useful for web UI and mobile
    # Listens for args to specify if compatible or not, like treble=true, etc
    # Kind of like a "store"
    overlays = [ ]
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM overlays;")
    for overlayInfo in cursor.fetchall():
        overlay = {}
        overlay['id'] = overlayInfo[0]
        overlay['author'] = overlayInfo[1]
        overlay['name'] = overlayInfo[2]
        overlay['description'] = overlayInfo[3]
        overlay['url'] = overlayInfo[4]
        overlays.append(overlay)
    cursor.close()

    return jsonify(overlays), 200, {'ContentType': 'application/json'}

@app.route('/api/generateoverlayzip', methods=['GET'])
def generateOverlayZip():
    # Generates an addon zip to bundle overlays and such together
    # GET args should be specifying overlay IDs and such
    urls = []
    cursor = connection.cursor(buffered=True)
    for id in request.args.getlist('ids'):
        cursor.execute("SELECT url FROM overlays WHERE id='{}' LIMIT 1;".format(id))
        overlaydata = cursor.fetchone()
        urls.append(overlaydata[0])

    with tempfile.TemporaryDirectory() as zipPath:
        for url in urls:
            fileName = url[url.rfind("/")+1:]
            urlretrieve(url, "{}/{}".format(zipPath, fileName))
        data = io.BytesIO()
        with zipfile.ZipFile(data, mode='w') as zip:
            for fileName in os.listdir(zipPath):
                zip.write("{}/{}".format(zipPath, fileName), fileName)
        data.seek(0)
        return send_file(
            data,
            mimetype='application/zip',
            as_attachment=True,
            attachment_filename='overlays.zip'
        )

app.config.from_object(os.environ.get('API_SETTINGS') or 'config.Config')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
