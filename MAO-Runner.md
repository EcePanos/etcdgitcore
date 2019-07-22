# MAO Runner Prototype

Prototype runner for MAO-MAO framework. The operating principle is to include
in every MAO-MAO tool:
- An install script
- A script that runs the tool with no interactive input besides command-line arguments
- A `mao.yaml` file with their paths and what arguments they need

With these constraints we can install and execute the program from the
MAO Runner. On its own this is not useful, but, when integrated with the
MAO-MAO etcd-git program, it will allow the tools to be
managed automatically as components of a single framework (eg for generating
cronjobs or event-driven execution of the tools as the framework evolves)

This means that now the MAO-MAO launcher program will be capable of setting up
and running a MAO-MAO network worker machine by:
- Installing and operating the tools on demand or scheduled
- Tracking and updating the datasets when a tool is executed

## TODO:
- Integration with the etcd-git tool to discover and clone the tools
- Generation of cronjobs
- Automatically adding generated data to datasets
