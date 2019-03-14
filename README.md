# etcdgitcore
Core software components of the etcd managed git environment.

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

Run the syncer program to either sync your data with the cluster or retrieve data from another operator in the cluster.

### Sync Mode

In sync mode the program will ask you which microservice hub your data is about, push it to your github remote and write an entry in etcd to help members of the cluster to find it.

### Retrieve Mode

In retrieve mode the program will ask you which hub you are interested in, then display available datasets by date updated, and ask to input a date, then show you which operators have data from that date. Finally, once you select an operator, it will clone their data to your import directory.
