Gears API Calls
======

The API here is written in flask and should be responsive and elegant enough to match almost all loads.

API Calls
------
#### `/api/register`

Registers a device to the server

HTTP Method: `POST`

Arguments:
  - None

POST Data:

    "device": {
      "uuid": "SomeKindOfUniqueIDHere",
      "model": "Nexus 5X",
      "codename": "bullhead",
      "friendlyname": "SomeKindOfNameSetByUser",
    }

Return Data:
  - HTTP 200 if success
  - HTTP 400 if JSON is invalid
  - HTTP 500 if there was a server error


#### `/api/poll`

Gets info on a registered device

HTTP Method: `GET`

Arguments:
  - `uuid` - The UUID of the device used when registered

POST Data: None

Return Data:

    {
      "isRegistered": true,
      "device": {
        "uuid": "SomeKindOfUniqueIDHere",
        "model": "Nexus 5X",
        "codename": "bullhead",
        "friendlyname": "SomeKindOfNameSetByUser",
      },
      "hasSettingsRestores": true,
      "hasOverlays": true
    }

#### `/api/pull/settings`

Gets the settings from the database

HTTP Method: `GET`

Arguments:
  - `uuid` - The UUID of the device used when registered

POST Data: None

Return Data:

    {
      "global": {
        "key_name": "value",
        "key_two": "value"
      },
      "system": {
        "key_name": "value",
        "key_two": "value"
      },
      "secure": {
        "key_name": "value",
        "key_two": "value"
      }
    }

#### `/api/pull/overlays`

Gets the overlays from the database

HTTP Method: `GET`

Arguments:
  - `uuid` - The UUID of the device used when registered

POST Data: None

Return Data:

    [
      {
        "id": 0,
        "name": "friendlyname",
        "description": "value",
        "author": "value",
        "url": "https://linktooverlay.com/overlay.apk"
      },
      {
        "id": 1,
        "name": "friendlyname",
        "description": "value",
        "author": "value",
        "url": "https://linktooverlay.com/overlay.apk"
      }
    ]

#### `/api/listoverlays`

Gets the list of all overlays from the database

HTTP Method: `GET`

Arguments:
  - TBD, Should be a way to narrow results, think like an overlays market

POST Data: None

Return Data:

    [
      {
        "id": 0,
        "name": "friendlyname",
        "description": "value",
        "author": "value",
        "url": "https://linktooverlay.com/overlay.apk"
      },
      {
        "id": 1,
        "name": "friendlyname",
        "description": "value",
        "author": "value",
        "url": "https://linktooverlay.com/overlay.apk"
      }
    ]

###### `/api/generateoverlayzip`

Gets a zip file of specified overlays

HTTP Method: `GET`

Arguments:
  - A list of overlay IDs to zip up `yourdomainname.com:5000/api/generateoverlayzip?ids=1&ids=4&ids=8` would select overlays 1, 4, and 8

POST Data: None

Return Data: A zip file with these overlays
