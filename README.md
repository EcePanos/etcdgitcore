# etcd-git-sync
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

#### Sync Mode

In sync mode the program will ask you which microservice hub your data is about, push it to your github remote and write an entry in etcd to help members of the cluster to find it.  
The commit message used during the github sync is generated as `sync <date>`

#### Retrieve Mode

In retrieve mode the program will ask you which hub you are interested in, then display available datasets by date updated, and ask to input a date, then show you which operators have data from that date. Finally, once you select an operator, it will clone their data to your import directory.

## Purpose

The purpose of this tool is to facilitate collaboration in a global decentralized effort, where all collaborators sharing a single git repo would quickly become too cumbersome, and simply advertising their data on a website would have too much management overhead compared to an automated and distributed solution. Most importantly, the goal is for there to be no 'owner' or central governing body for the initiative that would cause a management bottleneck and impede research.    
The tool's goal is to solve the problem with minimal overhead, and without forcing the users to share sensitive data about their resources (such as passwords and ssh keys) while at the same time being easy to integrate in a larger toolset/research workflow.
