# ESIEA | OSINT Project

This project is an open source intelligence (OSINT) tool. Using personal data (name, e-mail address...), it collects open informations (photos, texts...) from different web sources and writes them all in a JSON file and a PDF report.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Requirements

The main script uses Python 3. You must download the latest version of Python 3. 

* https://www.python.org/downloads/source/

Some modules have requirements, the setup script download the requirements automatically during its execution. Python requirements are downloaded with the paquet manager "Pip".
Download pip with the following (Linux) command:
```
sudo apt install python3-pip
```

### Installing

Clone or download the project on your local machine.
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

## Authors

* **Florent Guyon** - *5th-year Digital Sciences Student*.
* **Paul Innocenti** - *5th-year Digital Sciences Student*.

## Acknowledgments

*This tool is developed for educational purposes only.*