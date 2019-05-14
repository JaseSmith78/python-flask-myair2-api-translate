#!/usr/bin/env python3

"""
    myair v2 control

    myaircontrol Copyright(C) 2019 Jason Smith
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions.
"""

__author__ = "Jason Smith"
__version__ = "0.0.4"
__license__ = "GPL-3.0-or-later"

import os
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import logzero
import markdown
from flask import Flask, jsonify
from flask_cors import CORS
from logzero import logger

def create_app(config=None):
    app = Flask(__name__)

    # See http://flask.pocoo.org/docs/latest/config/
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    # Setup cors headers to allow all domains
    # https://flask-cors.readthedocs.io/en/latest/
    CORS(app)

    # Definition of the routes. Put them into their own file. See also
    # Flask Blueprints: http://flask.pocoo.org/docs/latest/blueprints
    @app.route("/")
    def index():
        logger.info("/")
        #open README.md file
        with open(os.path.dirname(app.root_path) + '/myair/README.md', 'r') as readme_file:
            #read the file
            contents = readme_file.read()
            #convert to html from markdown
            return markdown.markdown(contents, extensions=['tables'])

    @app.route("/api/getSetTemp")
    def getSetTemp():
        logger.info("getSetTemp")
        tmp = myair_status("SetTemp")
        return tmp
    
    @app.route("/api/setTemp/<temp>")
    def setTemp(temp):
        logger.info("setTemp/%s", temp)
        tmp = myair_settemp(temp)
        return tmp    
    
    @app.route("/api/getActTemp")
    def getActTemp():
        logger.info("getActTemp")
        tmp = myair_status("ActTemp")
        return tmp
    
    @app.route("/api/getMode")
    def getMode():
        logger.info("getMode")
        tmp = myair_status("Mode")
        return tmp   
        
    @app.route("/api/getRunning")
    def getRunning():
        logger.info("getRunning")
        tmp = myair_status("Running")
        return tmp

    @app.route("/api/setRunning/<run>")
    def setRunning(run):
        logger.info("setRunning/%s", run)
        tmp = myair_setrun(run)
        return tmp
    
    @app.route("/api/getZone/<zone>")
    def getZone(zone):
        logger.info("getZone/%s", zone)
        (a,b,c) = myair_zonestatus()
        rettext = "name: {1} open: {2} Percent: {3}"
        rettext = rettext.replace("{1}", a[int(zone)])
        rettext = rettext.replace("{2}", b[int(zone)])
        rettext = rettext.replace("{3}", c[int(zone)])
        return rettext
        
    @app.route("/api/setZone/<zone>/<action>/<value>")
    def setZone(zone, action, value):
        logger.info("setZone/%s/%s/%s", zone, action, value)
        if action.upper() == "ONOFF":
            tmp = myair_setzone(zone=zone, onoff=value)
        elif action.upper() == "PERCENT":
            tmp = myair_setzone(zone=zone, percent=value)
        else: 
            tmp = "broken"
        return tmp
            
      

        
    return app

def myair_request(req):
    """ Set to IP or hostname of myair controler """
    myairaddress = "ac.home.internal"
    myairdic = {
            "login":"http://{1}/login?password=password",
            "status":"http://{1}/getSystemData",
            "power":"http://{1}/setSystemdata?airconOnOff={2}",
            "settemp":"http://{1}/setSystemData?centralDesiredTemp={2}",
            "getzone":"http://{1}/getZoneData?zone={2}",
            "setzone":"http://{1}/setZoneData?zone={2}",
            "setzoneonoff":"&zoneSetting={3}",
            "setzonepercent":"&userPercentSetting={4}"
            }
    for each in myairdic:
        myairdic[each] = myairdic[each].replace("{1}",myairaddress)
    return myairdic[req]
     
def myair_login():
    """myair login"""       
    logger.info("do myair login, url: %s", myair_request("login"))
    x = urllib.request.urlopen(myair_request("login"))
    httpreturn = x.read()
    logger.debug("returned: %s", httpreturn)
    
def myair_status(req):
    myair_login()
    logger.info("do myair status, type: %s, url: %s", req, myair_request("status"))
    urlhandle = urllib.request.urlopen(myair_request("status"))
    httpresult = urlhandle.read()
    logger.debug("returned: %s", httpresult)
    y = ET.fromstring(httpresult)
    
    Running = 0
    TempActual = 0.0
    TempSetpoint = 0.0
    Mode = "X"

    for z in y.findall('system'):
        for system in z.findall('unitcontrol'):
            Running = system.findtext('airconOnOff')
            TempActual = system.findtext('centralActualTemp')
            TempSetpoint = system.findtext('centralDesiredTemp')
            d = system.findtext('mode')
            if d == "1":
                Mode = "C"
            if d == "2":
                Mode = "H"
            if d == "3":
                Mode = "F"
    retval = ""        
    if req.upper() == "ACTTEMP":
        retval = str(TempActual)
    elif req.upper() == "SETTEMP":
        retval = str(TempSetpoint)
    elif req.upper() == "RUNNING":
        retval = str(Running)
    elif req.upper() == "MODE":
        retval = str(Mode)
    else:
        retval = "0"
    logger.info("returning status: %s", retval)
    return retval
    
def myair_zonestatus():
    """
    Returns name, open, percent
    as arrays
    """
    myair_login()
    logger.info("do myair zone status")
    zoneurl = myair_request("getzone")
    zoneurl = zoneurl.replace("{2}","all")
    logger.info(" url: %s", zoneurl)
    
    zname = ["","","","","","","","",""]
    zopen = [0,0,0,0,0,0,0,0,0]
    zpercent = [0,0,0,0,0,0,0,0,0]
    
    urlhandle = urllib.request.urlopen(zoneurl)
    httpresult = urlhandle.read()
    logger.debug("returned: %s", httpresult)
    x = ET.fromstring(httpresult)
    for ZoneNumber in range(1,9):
        for system in x.findall('zone'+str(ZoneNumber)):
            zopen[ZoneNumber] = system.findtext('setting')
            zpercent[ZoneNumber] = system.findtext('userPercentSetting')
            zname[ZoneNumber] = system.findtext('name')
    return (zname,zopen,zpercent)
    
def myair_setzone(zone, onoff=-1, percent=-1):
    """sets zone params"""
    myair_login()
    logger.info("do myair set zone onoff: %s, percent: %s", onoff, percent)
    url = myair_request("setzone").replace("{2}",str(zone))
    logger.info("url: %s", url)
    if int(onoff) > -1:
        logger.debug("onoff")
        url = url + myair_request("setzoneonoff").replace("{3}",str(onoff))
    if int(percent) > -1:
        logger.debug("percent")
        url = url + myair_request("setzonepercent").replace("{4}",str(percent))
    logger.info("url: %s", url)
    urlhandle = urllib.request.urlopen(url)
    http = urlhandle.read()
    logger.debug("returned: %s", http)
    return "ok"
    
def myair_setrun(run):
    """sets the AC on or off"""
    myair_login()
    logger.info("so myair set running: %s", run)
    runurl = myair_request("power").replace("{2}", run)
    logger.info("url: %s", runurl)
    urlhandle = liburlrequest.urlopen(runurl)
    httpresult = urlhandle.read()
    logger.debug("returned: %s", httpsresult)
    return "ok"
    
def myair_settemp(temp):
    """ sets desired temp"""
    myair_login()
    logger.info("do myair set temp: %s", temp)
    tempurl = myair_request("settemp").replace("{2}", temp)
    logger.info("url: %s", tempurl)
    urlhandle = urllib.request.urlopen(tempurl)
    httpresult = urlhandle.read()
    logger.debug("returned: %s", httpresult)
    return "ok"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", action="store", default="8000")
    logzero.logfile("/var/log/myaircontrol/myair.log",backupCount = 9, maxBytes = 1e6)
    args = parser.parse_args()
    port = int(args.port)
    app = create_app()
    app.run(host="0.0.0.0", port=port)
