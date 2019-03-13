import etcd
import git
import datetime
#python-etcd
#GitPython


client = etcd.Client(host='127.0.0.1', port=2379)
now = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
print(now)

def sync(path):
    #Push to github repo
    repo = git.Repo(path)

    print(repo.git.status())
    print(repo.git.add('.'))
    repo.index.commit("sync " + now)
    print(repo.git.status())
    print(repo.remotes.origin.url)
    repo.remotes.origin.push()
    print(repo.git.status())

    #Write etcd entry
    client.set(('/aws/' + now + '/panos'), repo.remotes.origin.url)
    print(client.get('/aws/' + now + '/panos').value)


def retrieve():
    dir = str(input("Which microservice repository?"))
    directory = client.get("/" + dir)

    # loop through directory children
    for result in directory.children:
        print(result.key)
    #newdata('/home/panos/etcdgitdata')
    date = str(input("Which date?"))
    directory = client.get("/" + dir + "/" + date)

    # loop through directory children
    for result in directory.children:
        print(result.key)
    operator = str(input("Which operator?"))
    value = client.get("/" + dir + "/" + date + "/" + operator).value
    print(value)
retrieve()
