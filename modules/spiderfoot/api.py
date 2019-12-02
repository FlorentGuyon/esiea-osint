# -*- coding: utf-8 -*-

import requests
import json
import time
import sys
import multiprocessing
import os

#Adresse de spiderfoot en Local
API_ENDPOINT = "http://127.0.0.1:5001/"

scanId = ""


#Resume d'un scan en ayant son id
def searchForASummaryScan(scanId):
    newUrl = API_ENDPOINT + "scansummary?id=" + scanId + "&by=type"
    result = requests.get(url = newUrl)
    data = result.json()
    print(data)

def launchScan(baseCriteria):

    #Check if server is online
    result = requests.get(url = API_ENDPOINT + "ping")
    s = result.json()
    #
    if(s[0] == "SUCCESS"):

        #Set scan parameters
        scanParam = {
            "scanname": baseCriteria,
            "scantarget": baseCriteria,
            "modulelist": "",
            "typelist": "",
            "usecase": "all",
            "cli": "1"
        }

        #Get results and save scan ID
        result = requests.post(url= API_ENDPOINT + "startscan", data= scanParam)
        s = result.json()
        scanId= s[1]
        status= ""

        #Waiting for scan to finish
        while status != "FINISHED":
            time.sleep(3)
            result = requests.get(url= API_ENDPOINT+ "scanopts?id=" + scanId)
            s = result.json()
            if(s['meta'][5] != status):
                status = s['meta'][5]
                print("  [" + status + "]\tScan of " + baseCriteria)
          
        #Put data into a pretty json
        exportParam={"ids": scanId}
        result = requests.post(url= API_ENDPOINT + "scanexportjsonmulti", data = exportParam)
        j = json.loads(result.text)
        out = json.dumps(j, indent=4, separators=(',', ': '))
        #
        with open(os.sep.join(["modules", "spiderfoot", "results", baseCriteria.replace("\"", "") + ".json"]), "w+") as json_file:
            json_file.write(out)
            print("\nResults of " + baseCriteria + " scan loaded into " + os.sep.join(["modules", "spiderfoot", "results", baseCriteria.replace("\"", "") + ".json"]) + "\n")
        return 0
    #
    else:
        print("The server in unreachable. Scan of " + baseCriteria + " cancelled.")
        return -1


#Launch automatic scan with arguments
if __name__ == '__main__':
    jobs = []
    if sys.argv[1]:
        emails = sys.argv[1].split(',')
        print("\nNumber of data to scan: " + str(len(emails)) + "\n")
        if len(emails) > 1:
            for index in xrange(0, len(emails)):
                p = multiprocessing.Process(target=launchScan, args=[emails[index]])
                jobs.append(p)
                p.start()
        else:
            launchScan(sys.argv[1])
    else: 
        print("No valid target name. Please enter a valid name")