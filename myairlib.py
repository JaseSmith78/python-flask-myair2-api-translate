#!/usr/bin/env python3

"""
    myair v2 control 

MIT License

Copyright (c) [2019] [Jason Smith]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

__author__ = "Jason Smith"
__version__ = "0.0.9"
__license__ = "MIT"

import os
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import logzero
from logzero import logger
from time import sleep,time
import json


class myair:
    def __init__(self, address):
        """ Setup class variables """
        self.controlUnit = address
        self.updateTime = (time.time() - 5 )
        self.refreshIntival = 5
        self.zoneOnOff = [0,0,0,0,0,0,0,0,0]
        self.zoneName = ["","","","","","","","",""]
        self.zonePercent = [0,0,0,0,0,0,0,0,0]
        self.mode = 'C'
        self.power = '0'
        self.tempActual = '21'
        self.tempSet = '21'
        """ Set to IP or hostname of myair controler """
        self.urldic = {
                "login":"http://{1}/login?password=password",
                "status":"http://{1}/getSystemData",
                "power":"http://{1}/setSystemData?airconOnOff={2}",
                "settemp":"http://{1}/setSystemData?centralDesiredTemp={2}",
                "getzone":"http://{1}/getZoneData?zone=all",
                "setzone":"http://{1}/setZoneData?zone={2}",
                "setzoneonoff":"&zoneSetting={3}",
                "setzonepercent":"&userPercentSetting={4}",
                "setmode":"http://{1}/setSystemData?mode={2}"
                }
        for each in self.urldic:
            self.urldic[each] = self.urldic[each].replace("{1}",self.controlUnit)

    def login():
        """myair login"""
        logger.info("do myair login, url: %s", self.urldic("login"))
        x = urllib.request.urlopen(self.urldic("login"))
        httpreturn = x.read()
        logger.debug("returned: %s", httpreturn)

    def updateData():
        if time.time() > self.updateTime + self.refreshInterval:
            login()
            """ start the get status process """
            logger.info("do myair status, url: %s",  self.urldic("status"))
            urlhandle = urllib.request.urlopen(self.urldic("status"))
            httpresult = urlhandle.read()
            logger.debug("returned: %s", httpresult)
            y = ET.fromstring(httpresult)
            for z in y.findall('system'):
                for system in z.findall('unitcontrol'):
                    self.power = system.findtext('airconOnOff')
                    self.tempActual = system.findtext('centralActualTemp')
                    self.tempSet = system.findtext('centralDesiredTemp')
                    d = system.findtext('mode')
                    if d == "1":
                        self.mode = "C"
                    if d == "2":
                        self.mode = "H"
                    if d == "3":
                        self.mode = "F"
            """ Update the zome status """
            logger.info("do myair zone status")
            logger.info(" url: %s", self.urldic("getzone"))
            urlhandle = urllib.request.urlopen(self.urldic("getzone"))
            httpresult = urlhandle.read()
            logger.debug("returned: %s", httpresult)
            x = ET.fromstring(httpresult)
            for ZoneNumber in range(1,9):
                for system in x.findall('zone'+str(ZoneNumber)):
                    self.zoneOnOff[ZoneNumber] = system.findtext('setting')
                    self.zonePercent[ZoneNumber] = system.findtext('userPercentSetting')
                    self.zoneName[ZoneNumber] = system.findtext('name')
    
    def getStatus(self):
        return sata

    def setStatus(self, mode):
        pass

    def setStatus(self, power):
        pass

    def getSetTemp(self):
        updateData()
        return self.tempSet
   
    def getActualTemp(self):
        updateData()
        return self.tempActual

    def getZone(zone):
        updateData()
        retval = json.JSONEncoder().encode({OnOff: self.zoneOnOff[zone], Percent: self.zonePercent[zone], Name: self.zoneName[zone]})
        return(retval)

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
        urlhandle = urllib.request.urlopen(runurl)
        httpresult = urlhandle.read()
        logger.debug("returned: %s", httpresult)
        return "ok"

    def myair_setmode(mode):
        """sets the AC mode, Cooling (1), Heating (2), or Fan (3)"""
        myair_login()
        logger.info("do set new mode")
        modesub = 3
        if mode == "C":
            modesub = 1
        if mode == "H":
            modesub = 2
        if mode == "F":
            modesub = 3
        runurl = myair_request("setmode").replace("{2}", str(modesub))
        logger.info("url: %s", runurl)
        urlhandle = urllib.request.urlopen(runurl)
        httpresult = urlhandle.read()
        logger.debug("returned: %s", httpresult)
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


#--------------------------------------------------------------------------------------------------------------

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

    @app.route("/status")
    def HBThermStatus():
        logger.info("/status")
        statmp ="{"
        if myair_status("Running") == "0":
            statmp = statmp + "\"currentHeatingCoolingState\":0, "
            statmp = statmp + "\"targetHeatingCoolingState\":0, "
        else:
            tmpmode = myair_status("Mode")
            if tmpmode == "H":
                statmp = statmp + "\"currentHeatingCoolingState\":1, "
                statmp = statmp + "\"targetHeatingCoolingState\":1, "
            if tmpmode == "C":
                statmp = statmp + "\"currentHeatingCoolingState\":2, "
                statmp = statmp + "\"targetHeatingCoolingState\":2, "
            if tmpmode == "F":
                statmp = statmp + "\"currentHeatingCoolingState\":2, "
                statmp = statmp + "\"targetHeatingCoolingState\":3, "
        tmptemp = myair_status("ActTemp")
        statmp = statmp + "\"currentTemperature\":" + tmptemp + ", "
        tmptemp = myair_status("SetTemp")
        statmp = statmp + "\"targetTemperature\":" + tmptemp + " }"
        logger.info("returning json: %s", statmp)
        return statmp

    @app.route("/targetHeatingCoolingState/<mode>")
    def HBThermSetMode(mode):
        logger.info("targetHeatingCoolingState/%s", mode)
        if int(mode) == 0:
            tmp = myair_setrun("0")
            return tmp
        else:
            tmp = myair_setrun("1")
            if int(mode) == 1:
                tmp = tmp + "\n" + myair_setmode("H")
            if int(mode) == 2:
                tmp = tmp + "\n" + myair_setmode("C") 
            if int(mode) == 3:
                tmp = tmp + "\n" + myair_setmode("F") 
            return tmp

    @app.route("/targetTemperature/<temp>")
    def HBThermSetTemp(temp):
        logger.info("/targetTemperature/%s", temp)
        tmp = myair_settemp(temp)
        return tmp


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

    @app.route("/api/getZoneOO/<zone>")
    def getZoneOO(zone):
        logger.info("getZoneOO/%s", zone)
        (a,b,c) = myair_zonestatus()
        rettext = b[int(zone)]
        return rettext
    
    @app.route("/getZones")
    def getZones():
        logger.info("getZones")
        (a,b,c) = myair_zonestatus()
        rettext = "| name | open | percent | \n"
        rettext = rettext + "| --- | :---: | :---: | \n"
        for i in range(1, len(a)):
            rettext = rettext + "| " + a[i] + " | " + str(b[i]) + " | " + str(c[i]) + " | \n"
        return markdown.markdown(rettext, extensions=['tables'])
    
    @app.route("/api/getZones")
    def getZonesAPI():
        logger.info("getZonesAPI")
        (a,b,c) = myair_zonestatus()
        rettext = "name | open | percent \n"
        for i in range(1, len(a)):
            rettext = rettext + a[i] + " | " + str(b[i]) + " | " + str(c[i]) + "\n"
        return rettext

    @app.route("/api/setMode/<mode>")
    def setMode(mode):
        logger.info("/api/setMode/%s", mode)
        tmp = myair_setmode(mode)
        return tmp

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


     

    

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", action="store", default="8000")
    logzero.logfile("/var/log/myaircontrol/myair.log",backupCount = 9, maxBytes = 1e6)
    args = parser.parse_args()
    port = int(args.port)
    app = create_app()
    app.run(host="0.0.0.0", port=port)
