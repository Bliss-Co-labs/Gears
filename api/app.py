#!flask/bin/python
from flask import Flask, abort, request, jsonify, send_file
import os
import io
import zipfile

app = Flask(__name__)

@app.route('/')
def test():
    return "Is this the Krusty Krab?\nNo, this is Patrick", 200, {'ContentType': 'text/plain'}

@app.route('/api/register', methods=['POST'])
def register():
    #Connect to db, add phone info with UUID(model, friendly name, etc)
    # POST json
    # "device": {
    #   "uuid": "SomeKindOfUniqueIDHere",
    #   "model": "Nexus 5X",
    #   "codename": "bullhead",
    #   "friendlyname": "SomeKindOfNameSetByUser",
    # }
    if not request.json or not 'device' in request.json:
        abort(400)
    #Do the database transactions
    # Return success if so
    return "Error", 500

@app.route('/api/poll', methods=['GET'])
def poll():
    # Get info on if device is registered
    # We're looking for GET arg UUID mostly
    # return if it's registered, if it has restore points, and if it has overlays selected
    return jsonify(request.args), 200, {'ContentType': 'application/json'}


@app.route('/api/pull/settings', methods=['GET'])
def pullSettings():
    # Grab settings from DB, looking for GET arg UUID
    settings = {
        "global":
            {
                "key_name": "value",
                "key_two": "value"
            },
        "system":
            {
                "key_name": "value",
                "key_two": "value"
            }
        }
    return jsonify(settings), 200, {'ContentType': 'application/json'}

@app.route('/api/pull/overlays', methods=['GET'])
def pullOverlays():
    # Grab overlay data from DB, looking for GET arg UUID
    overlays = [
            {
                "id": "overlayid Is An Int",
                "name": "friendlyname",
                "description": "value",
                "author": "value",
                "url": "https://linktooverlay.com/overlay.apk"
            }
        ]
    return jsonify(overlays), 200, {'ContentType': 'application/json'}


@app.route('/api/listoverlays', methods=['GET'])
def listOverlays():
    # Pulls all possible overlays from storage and sends then, useful for web UI and mobile
    # Listens for args to specify if compatible or not, like treble=true, etc
    # Kind of like a "store"
    overlays = [
            {
                "id": "overlayid Is An Int",
                "name": "friendlyname",
                "description": "value",
                "author": "value",
                "url": "https://linktooverlay.com/overlay.apk"
            }
        ]
    return jsonify(overlays), 200, {'ContentType': 'application/json'}

@app.route('/api/generateoverlayzip', methods=['GET'])
def generateOverlayZip():
    # Generates an addon zip to bundle overlays and such together
    # GET args should be specifying overlay IDs and such
    zipPath = "testzip/"
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as zip:
        for fileName in os.listdir(zipPath):
            zip.write(zipPath + fileName)
    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='overlays.zip'
    )

app.config.from_object(os.environ.get('API_SETTINGS') or 'config.Config')

if __name__ == '__main__':
    app.run()
