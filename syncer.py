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
today = str(datetime.datetime.today().year) + "-" + str(datetime.datetime.today().month) + "-" + str(datetime.datetime.today().day)


def sync():
    # Push to github repo
    repo = git.Repo(workdir)
    hub = str(input("Which microservice repository?"))
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
        client.set(('/'+ hub + '/' + today + '/' + user), repo.remotes.origin.url)
        print(client.get('/'+ hub + '/' + today + '/' + user).value)
    except:
        print("Error updating etcd")
        return


def retrieve():
    dir = str(input("Which microservice repository?"))
    try:
        directory = client.get("/" + dir)
        # loop through directory children
        for result in directory.children:
            print(result.key)
    except:
        print("No such entry")
        return
    date = str(input("Which date?"))
    try:
        directory = client.get("/" + dir + "/" + date)
        # loop through directory children
        for result in directory.children:
            print(result.key)
    except:
        print("No such entry")
        return
    operator = str(input("Which operator?"))
    try:
        value = client.get("/" + dir + "/" + date + "/" + operator).value
    except:
        print("No such entry")
        return
    answer = str(input("Clone " + value + " to " + importdir + "?[y/n]"))
    if answer == 'y':
        try:
            git.Repo.clone_from(value, importdir)
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
