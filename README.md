# ESIEA | Projet de fin d'études - OSINT

This project is an OSINT tool based on open source python scripts (called "modules" in the following text).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Requirements

You can run the main script with either Python 2 or 3, but some modules need one specific version of Python. 
So, download Python 2 and Python 3.

* https://www.python.org/downloads/source/

Some modules have requirements, the main script download the requirements automatically during its execution.
Python requirements are downloaded with the paquet manager "Pip".
Download pip with the following command:
```
python get-pip.py
```

### Installing

Clone or download the project in your local machine.

### Configuring

Open the file modules.json and setup the "args value" according to your needs.
The "args description" can help you.

### Running

Example:
```
python main.py www.myWebSite.com
```

* "python" is an alias defined in the PATH environment variable of your local machine.
* "main.py" is the name of the main script (.py means it's a Python script). If you're not located on the root directory of this project, you must write the exact relatif or absolut path to this file. 
Exemple on a Windows environment:
```
D:\\myFolder\\mySubFolder\\main.py
```
Or, if you are already located on "D:\\myfolder":
```
.\\mySubFolder\\main.py
```

## Authors

* **Florent Guyon** - *5th-year Digital Sciences Student*.
* **Paul Innocenti** - *5th-year Digital Sciences Student*.

## Acknowledgments

Today, this tool is developed for educational purposes only.