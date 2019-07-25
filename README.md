# Research Orbservatory Framework Launcher Manager And Orchestrator

Core software components of the MAO-MAO framework.

## Installation
 - Install etcd and join cluster (installer pending)
 - Install and configure git
 - Install requirements:
 ```
 pip install -r requirements.txt
 ```
 - Setup the config file with:
    - The path to import cloned data to
    - The host and port of etcd

## Usage

Run async_launcher.py to start the server. You can communicate with it with HTTP requests (CLI client pending). Detailed documentation of the REST API will be writen when the API itself is considered stable enough.
#### GETting information 

You can list the tools registered in the cluster, the tools installed in this node (if you installed any) and the datasets registered in the cluster.
#### Register tool

Using this endpoint will allow your tool to be discoverable by other members in the cluster. If it conforms to the MAO specification they will be able to clone, install and run it from this tool.

#### Install Tool

Assuming a tool is registered in the database and contains a MAO definition file. This can clone it from the listed repo, run the installer and then clone the dataset repository to the system.

#### Tool Help

This will output all the command information of a particular tool from the cached copy of its MAO definition. It will list the possible commands along with the arguments you can pass to them.
#### Run Tool

This endpoint is for executing tools. Assuming you have write permission on the tools data repository it will also push the generated data automatically (so make sure your tool adds data files instead of overwriting them). Besides the name of the tool you also need to supply the command and a list of arguments to be passed to the tool. By providing the cron parameter you can also turn the job into a daily, weekly or monthly cronjob, though automatic git pushing will be disabled.

#### Clone Data
If you want to gain access to a dataset generated from other members of the cluster without the associated tools, use this command. It will just clone the data repo.

## MAO Specification
Read the MAO.md file for information and guidelines for making your tool compatible with the launcher.
