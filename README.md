# ESIEA | OSINT Project

This project is an open source intelligence (OSINT) tool. From personal data (name, e-mail address...), it collects open informations (photos, texts...) from different web sources and writes them all in a JSON file and a PDF report.

This tool works on Linux, Windows and Mac.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Requirements

The main script uses Python 3.6
You must download the latest version of Python 3 (at least version 3.6). 

* https://www.python.org/downloads/source/

Some modules have requirements, the setup script download the requirements automatically during its execution. Python requirements are downloaded with the paquet manager "Pip".
Download pip with the following (Linux) command:
```
sudo apt install python3-pip
```

### Installing

Clone (or download and unzip) the project on your local machine.
```
git clone https://github.com/FlorentGuyon/esiea-osint
```

### Configuring

Run the setup script as follows:
```
sudo python3 setup.py
```

### Running

When the requirements are downloaded, you can see the help page of the main script as follows:
```
python3 scan.py -h
```

A scan usually takes up to 5 minutes.
However, for a target's first scan, huge Twitter accounts can take up to 20 minutes 

### Getting results

A new folder "results" will contain all the collected data.
When all the scans will be finished, the absolut path to the PDF report will be printed, the JSON file containing all the collected data will be at the same location.

### Getting results

A new folder "results" will contain all the collected data.
When all the scans will be finished, the absolut path to the PDF report will be printed, the JSON file containing all the collected data will be at the same location.

### To go further

The documentation of the project is available in the "docs" folder as HTML web site.

## Authors

* **Florent Guyon** - *5th-year Digital Sciences Student*.
* **Paul Innocenti** - *5th-year Digital Sciences Student*.

## Acknowledgments

*This tool is developed for educational purposes only.*