Gears (maybe a temporary name)
======

Components in Docker
------
  - `api/` Flask API Endpoint
  - `database/` MySQL for Data
  - `webui/` Nginx for the Web UI

Adding to Components
------
For the frontend, edit files in `webui/content`. Let me know if you need a custom config or anything else for nginx.

We still need a database schema

For editing API calls, edit `api/app.py`

To see API details, see [`api/README.md`](api/README.md)


Running this project
------
You need [Docker](docker.com) installed and running

Set `MYSQL_USER`, `MYSQL_PASSWORD`, and `NGINX_HOST` in your environment first or things won't work

`docker-compose build` will build the services and create the docker instance and make it ready to run

`docker-compose up` will run it

##### To run one of the subprojects

`cd` into the directory and run `docker build -t project_name` and then run with `docker run project_name`

`api/` is run on port 5000

`webui/` is run on a port assigned by Docker, use `docker ps` to see it

`database/` is run on port 27017

TODO
------
 - Add overlays
 - Add a way to easily add overlays to the database
 - Create the web ui
 - Create the service app in the ROM
 - Run on a real server
 - Some kind of 2FA to pair phone with browser session
 - Add an API to tell server the settings and overlays used
 - Create a `vendor/gears` repo for easily adding to a rom
 - Anyone remember Suse Studio? That's a good inspiration
 - Anything else?

Contributing to the project
------
Send a pull request for now if you're not already in this repo
