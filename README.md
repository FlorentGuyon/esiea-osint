# ESIEA | OSINT Project

This project is an OSINT tool based on open source python scripts (called "modules" in the following text).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Requirements

The main script uses Python 3 so, you must download the latest version of Python 3. Some modules still use Python 2 so, you must also download the latest version of Phython 2.

* https://www.python.org/downloads/source/

Some modules have requirements, the setup script download the requirements automatically during its execution. Python requirements are downloaded with the paquet manager "Pip".
Download pip with the following command:
```
sudo apt install python3-pip
```

### Installing

Clone or download the project in your local machine.
```
git clone https://github.com/FlorentGuyon/esiea-osint
```

### Configuring

Run the setup script as follows:
```
sudo python3 setup.py
```

Keep this window open during the scans to keep the servers up.

### Running

When the requirements are downloaded and the servers are up, you can run (on another shell) the main script as follows to see the help page:
```
python3 scan.py -h
```

## Authors

* **Florent Guyon** - *5th-year Digital Sciences Student*.
* **Paul Innocenti** - *5th-year Digital Sciences Student*.

## Acknowledgments

Today, this tool is developed for educational purposes only.