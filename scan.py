#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SYSTEM CALLS
import sys

# OS CALLS
import os

# ARGUMENTS PARSING
import getopt

# PARALLELIZATION
import threading

# TIME MANIUPULATION
import time

# ASYCHRONOUS COMMUNICATION
import asyncio


#____FILE__________________CLASS_
from libs.Person 	import Person


#_____FILE_________________FUNCTIONS_
from libs.utils		import *



stop = False



def startStatsDisplay():

	threading.Thread(name = "display", target = printStats).start()


def stopStatsDisplay():

	global stop
	stop = True

	for thread in threading.enumerate():

		if thread.name == "display":
			thread.join() 
			break


def printStats():

	threadCount = 0
	previousThreadCount = -1

	while stop != True:
		
		threadCount = getCountOfScans()
		sys.stdout.flush()
		
		if threadCount != previousThreadCount:

			previousThreadCount = threadCount

			threadClasses = [thread.name for thread in threading.enumerate()]

			lines = [
				"",
				"  Analysing...",
				"",
			]

			lines += ["    ■ {}\t  {}\t| {}".format(threadType, threadClasses.count(threadType), "■" * threadClasses.count(threadType)) for threadType in getThreadTypes()]

			clear()
			print("\n".join(lines))
			time.sleep(0.1)


# Display an help message
def displayHelp():
	# Lines of the message
	lines = [
		"",
		"  ╔════════════════════╗",
		"  ║ DO YOU NEED HELP ? ║",
		"  ╠════════════════════╩═══════════════════════════════════════════════════════════════════════╗",
		"  ║ Enter your arguments as follows:                                                           ║",
		"  ║                                                                                            ║",
		"  ║   ■ -h                                  or --help                                          ║",
		'  ║   ■ -f "<firstname>"                    or --firstname="<firstname>"                       ║',
		'  ║   ■ -l "<lastname>"                     or --lastname="<lastname>"                         ║',
		'  ║   ■ -m "<middlename1>,<middlename2>..." or --middlename="<middlename1>,<middlename2>..."   ║',
		'  ║   ■ -u "<username1>,<username2>..."     or --username="<username1>,<username2>..."         ║',
		'  ║   ■ -e "<email1>,<email2>..."           or --email="<email1>,<email2>..."                  ║',
		'  ║   ■ -p "<phone1>,<phone2>..."           or --phone="<phone1>,<phone2>..."                  ║',
		"  ║                                                                                            ║",
		"  ╚════════════════════════════════════════════════════════════════════════════════════════════╝"
	]
	# Print the final message
	print("\n".join(lines))


# First function called
def parseArgs(argv):

	# Test if the arguments are valid
	try:
		# Extract the arguments following this options
		opts, args = getopt.getopt(argv, "hf:l:e:m:p:u:", ["help", "firstname=", "lastname=", "email=", "middlename=", "phone=", "username="])
	# If the arguments are invalid
	except:
		# Display an help message
		displayHelp()
		# Exit the script
		print("\"" + " ".join(argv) + "\" are not valid arguments.")

	# If the arguments are missing
	if len(opts) == 0:
		# Display an help message
		displayHelp()
		# Exit the script
		print("The arguments are missing.")

	data = {}

	# For all arguments
	for opt, arg in opts:
		
		# If the argument is about help
		if opt in ("-h", "--help"):
			displayHelp()
			quit()

		else:
			
			opt = opt.replace("-", "")

			key = None

			if len(opt) == 1:
				if opt == "f": key = "firstname"
				elif opt == "l": key = "lastname"
				elif opt == "m": key = "middlename"
				elif opt == "u": key = "username"
				elif opt == "e": key = "email"
				elif opt == "p": key = "phone"

			else:
				key = opt

			if (key not in ["firstname", "lastname", "middlename"]) & (arg.count(" ") > 0):
				print("Error: Unauthorized spaces, please use commas as separator for {} list.".format(key))
				quit()


			if key in ["firstname", "lastname"]:
				data[key] = arg.strip()

			else:
				arg = arg.split(",")
				for value in arg:
					if value != "":
						if key not in data.keys():
							data[key] = []
						data[key].append(value.strip())
					else:
						print("Warning: {} list is empty.".format(key))

	return data


if __name__ == "__main__":

	checkPythonVersion()

	# PARSE THE ARGUMENTS TO EXTRACT THE PERSONAL DATA
	data = parseArgs(sys.argv[1:])

	# EXTRACT RESULTS PATH AND NAME FROM DATA
	setResultsValues(data)

	# START THE THREAD THAT DISPLAYS STATS
	startStatsDisplay()

	# CREATE A PERSON OBJECT WITH THE PERSONAL DATA
	target = Person(**data)

	# WAIT THE END OF ALL THREADS
	waitEndOfScans()

	# STOP THE THREAD THAT DISPLAYS STATS
	stopStatsDisplay()

	# EXPORT THE RESULTS AS A PDF FILE
	target.pdfExport()

	# EXPORT THE RESULTS AS A JSON FILE
	target.jsonExport()