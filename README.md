# Research Orbservatory Framework Launcher Manager And Orchestrator

Core software components of the MAO-MAO framework.

## Installation
 - Install and configure etcd **(real etcd cluster not tested yet)**
 - Install and configure git
 - Create a github directory to store data files you create
 - Install requirements:
 ```
 pip install -r requirements.txt
 ```
 - Setup the config file with:
    - The path to your local Git Repository
    - The name you want written in etcd as your operator name
    - The path to import cloned data to
    - The host and port of etcd

## Usage

Launch launcher.py to access the interactive command line application. It currently has the following functionalities:

#### Register tool

This allows you to register a tool you have developed in the database. It creates an entry with the name of your tool and its github repository.

#### Install tool

This allows you to clone tools that have been registered in the database. It will give you a list of available tools to choose from.  
It will install the cloned tool in your import directory.

#### Run tool

This will allow you to run the installed tools in your system. You will be prompted to select the tool and then to select from available commands and finally any arguments the command requires. After the data has been generated by the tool, the program will ask you which microservice hub your data is about, push it to the tool's github data remote and write an entry in etcd to help members of the cluster to find it.  
The commit message used during the github sync is generated as `sync <date>`

#### Retrieve Mode

In retrieve mode the program will ask you which hub you are interested in, then display available datasets by date updated, and ask to input a date, then show you which operators have data from that date. Finally, once you select an operator, it will clone their data to your import directory.

#### Compare data

This mode allows you to choose from files in your workdir and compare them, to see the changes between two snapshots of a data stream. So far it only supports files in .csv format and does not search the directory recursively.

## Roadmap

- **Self-setup**: Discover and join the etcd cluster from within the Launcher.
- **Interface**: The interface will be redesigned to run as a server/daemon and to support running cronjobs or event-driven execution of experiments.
