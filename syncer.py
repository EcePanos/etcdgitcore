import etcd
import git
import datetime
import configparser
import mao_runner
from distutils.dir_util import copy_tree


config = configparser.ConfigParser()
config.read('config.ini')
importdir = config['WORKING_ENVIRONMENT']['IMPORTDIR']
etcd_host = config['ETCD']['HOST']
etcd_port = int(config['ETCD']['PORT'])
client = etcd.Client(host=etcd_host, port=etcd_port)
today = str(datetime.datetime.today().year) + "-" + str(datetime.datetime.today().month) + "-" + str(datetime.datetime.today().day)


def write(key,value):
    client.set(key, value)


def list(key):
    directory = client.get(key)
    qresult = []
    for result in directory.children:
        qresult.append(result.key)
    return qresult


def get(key):
    return client.get(key).value


def clonetool(repo, tool):
    try:
        git.Repo.clone_from(repo, importdir + "/" + tool)
        datarepo = mao_runner.install_program(importdir + "/" + tool)
        git.Repo.clone_from(datarepo, importdir + "/" + tool + "_data")
    except:
        print("Error cloning data")
        return


def sync(data):
    # Run tool
    info = mao_runner.run_program(data)
    copy_tree("{}/{}/{}".format(importdir, info[0], info[1]),
              "{}/{}".format(importdir, info[0] + "_data"))
    # Push to github repo
    repo = git.Repo("{}/{}".format(importdir, info[0] + "_data"))
    try:
        repo.git.add('.')
        repo.index.commit("sync " + today)
        print(repo.remotes.origin.url)
        repo.remotes.origin.push()
    except:
        print("Error during git sync")
        return
    # Write etcd entry
    try:
        client.set(('/data/' + info[2]), repo.remotes.origin.url)
        print(client.get('/data/' + info[2]).value)
    except:
        print("Error updating etcd")
        return


def retrieve(name):
    try:
        value = client.get("/data/" + name).value
    except:
        print("No such entry")
        return
    try:
        git.Repo.clone_from(value, importdir + "/" + name)
    except:
        print("Error cloning data")
        return


if __name__ == '__main__':
    print("Etcd-Git Sync:")
    print("A simple tool to share and track git repositories in an etcd cluster")
    print("Today it is " + today)
    while True:
        mode = str(input("Mode? (sync/retrieve/quit)"))
        if mode == 'sync':
            sync()
        elif mode == 'retrieve':
            retrieve()
        elif mode == 'quit':
            quit = str(input("Are you sure? [y/n]"))
            if quit == 'y':
                break
        else:
            print("Sorry, didn't catch that.")
