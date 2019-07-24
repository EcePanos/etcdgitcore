import sys
from ruamel.yaml import YAML
import subprocess
from contextlib import contextmanager
import os


output={}
yaml = YAML()
yaml.preserve_quotes = True


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def install_program(path):
    print("installing from " + path)

    with open(path + "/mao.yml", 'r') as stream:
        data = yaml.load(stream)
    print(data['Name'])
    print(data['Description'])
    with cd(path):
        subprocess.run("{} {}/{}".format(data['Installer']['Command'],path,data['Installer']['Script']), shell=True)
    data['Path'] = path
    with open ("local.yml",'r') as stream:
        local = yaml.load(stream)
        local['Programs'].append(data)
    with open ('local.yml', 'w') as stream:
        yaml.dump(local, stream)
    return data['Data']['Repo']['Remote']


def run_program():
    print("Select program to run:\n")
    with open ("local.yml",'r') as stream:
        local = yaml.load(stream)
    for n,program in enumerate(local['Programs']):
        print("{}. {}: {}".format(n+1,program['Name'],program['Description']))
    prog = int(input("\nYour choice: ")) - 1
    for n,command in enumerate(local['Programs'][prog]['Commands']):
        print("{}. {}: {}".format(n+1,command['Name'],command['Description']))
    com = int(input("\nYour choice: ")) - 1
    arguments = []
    if 'Arguments' in local['Programs'][prog]['Commands'][com]:
        for argument in local['Programs'][prog]['Commands'][com]['Arguments']:
            arguments.append(str(input("{}: {}: ".format(argument['Name'], argument['Description']))))
    command_string = "{} {}/{}".format(local['Programs'][prog]['Commands'][com]['Command'],
                                       local['Programs'][prog]['Path'],
                                       local['Programs'][prog]['Commands'][com]['Script'])

    for argument in arguments:
        command_string += " {}".format(argument)
    with cd(local['Programs'][prog]['Path']):
        subprocess.run(command_string, shell=True)
    return [local['Programs'][prog]['Name'],
            local['Programs'][prog]['Data']['Local'],
            local['Programs'][prog]['Data']['Repo']['Name']]


if __name__ == '__main__':
    print("Welcome to MAO-Runner")
    while True:
        mode = str(input("Press 1 to install or 2 to run "))
        if mode == '1':
            install_program(str(input("Path to spec ")))
        elif mode == '2':
            run_program()
        else:
            break
