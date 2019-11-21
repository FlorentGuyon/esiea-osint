# ESIEA | OSINT Project

This project is an OSINT tool based on open source python scripts (called "modules" in the following text).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Requirements

The main script uses Python 3 so, you must download the latest version of Python 3.

* https://www.python.org/downloads/source/

Some modules have requirements, the main script download the requirements automatically during its execution.
Python requirements are downloaded with the paquet manager "Pip".
Download pip with the following command:
```
sudo apt install python3-pip
```

### Installing

Clone or download the project in your local machine.
```
git clone https://github.com/FlorentGuyon/esiea-pfe-osint
```

### Configuring

The scripts in this project use the alias "python3" to run the version 3 of Python. This alias is automatically defined on some systems.
If, by running the command "python3" in a prompt, you got an error, define the alias as follows:

Windows(10):
```
doskey python3={ABSOLUTE PATH TO "python.exe" version 3}
```  

Go on the root directory of this project and run the setup script as follows:
```
python3 setup.py
```

The setup scipt will create a requirements file. Make sure to download or upgrade all the requirements.
You can download the requirements as follows:
```
sudo python3 -m pip install --upgrade -r requirements.txt
```

Open the "modules.json" file and change the arguments value as you need. The arguments description can help you.

### Running

When the requirements are downloaded, you can run the main script as follows:
```
python3 main.py
```

## Authors

* **Florent Guyon** - *5th-year Digital Sciences Student*.
* **Paul Innocenti** - *5th-year Digital Sciences Student*.

## Acknowledgments

Today, this tool is developed for educational purposes only.