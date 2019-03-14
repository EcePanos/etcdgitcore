import etcd
import git
import datetime
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
workdir = config['WORKING_ENVIRONMENT']['WORKDIR']
user = config['WORKING_ENVIRONMENT']['OPERATOR']
importdir = config['WORKING_ENVIRONMENT']['IMPORTDIR']
etcd_host = config['ETCD']['HOST']
etcd_port = int(config['ETCD']['PORT'])


client = etcd.Client(host=etcd_host, port=etcd_port)
now = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
print(now)


def sync(path, operator):
    # Push to github repo
    repo = git.Repo(path)
    hub = str(input("Which microservice repository?"))
    print(repo.git.status())
    print(repo.git.add('.'))
    repo.index.commit("sync " + now)
    print(repo.git.status())
    print(repo.remotes.origin.url)
    repo.remotes.origin.push()
    print(repo.git.status())
    # Write etcd entry
    client.set(('/'+ hub + '/' + now + '/' + operator), repo.remotes.origin.url)
    print(client.get('/'+ hub + '/' + now + '/' + operator).value)


def retrieve(path):
    dir = str(input("Which microservice repository?"))
    directory = client.get("/" + dir)
    # loop through directory children
    for result in directory.children:
        print(result.key)
    date = str(input("Which date?"))
    directory = client.get("/" + dir + "/" + date)
    # loop through directory children
    for result in directory.children:
        print(result.key)
    operator = str(input("Which operator?"))
    value = client.get("/" + dir + "/" + date + "/" + operator).value
    git.Repo.clone_from(value, path)


mode = str(input("Mode? (sync/retrieve)"))
if mode == 'sync':
    sync(workdir, user)
elif mode == 'retrieve':
    retrieve(importdir)
