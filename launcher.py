import syncer
import analyser


def registertool():
    name = str(input("Name of tool?"))
    repo = str(input("Github link:"))
    syncer.write("tools/{}".format(name),repo)


def downloadtool():
    print("Tools currently registered in the database:")
    syncer.list("tools")
    tool = str(input("Which tool do you need?"))
    repo = syncer.get("tools/" + tool)
    answer = str(input("Clone {} to importdir?[y/n]".format(repo)))
    if answer == 'y':
        syncer.clonetool(repo, tool)

if __name__ == '__main__':
    print("Welcome to the MAO-MAO Launcher")
    print("Current Features:")
    print("[1]Update the database with a new tool")
    print("[2]Install an existing tool")
    print("[3]Run a tool and generate data")
    print("[4]Search and retrieve data from the cluster")
    print("[5] Compare cloned data snapshots")
    print("[0]Quit(not really a feature)")

    while True:
        mode = str(input("What would you like to do?"))
        if mode == '1':
            registertool()
        elif mode == '2':
            downloadtool()
        elif mode == '3':
            syncer.sync()
        elif mode == '4':
            syncer.retrieve()
        elif mode == '5':
            analyser.list()
            file1 = str(input("First file:"))
            file2 = str(input("Second file:"))
            analyser.compare(file1, file2)
        elif mode == '0':
            quit = str(input("Are you sure? [y/n]"))
            if quit == 'y':
                break
        else:
            print("Sorry, didn't catch that.")
