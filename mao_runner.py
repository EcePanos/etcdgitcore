from ruamel.yaml import YAML
import subprocess
from contextlib import contextmanager
from crontab import CronTab
import os

cron = CronTab(user=True)
output = {}
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
        subprocess.run("{} {}/{}".format(data['Installer']['Command'], path, data['Installer']['Script']), shell=True)
    data['Path'] = path
    with open("local.yml", 'r') as stream:
        local = yaml.load(stream)
        local['Programs'].append(data)
    with open('local.yml', 'w') as stream:
        yaml.dump(local, stream)
    return data['Data']['Repo']['Remote']


def run_program(data):
    prog = 0
    com = 0
    with open("local.yml", 'r') as stream:
        local = yaml.load(stream)
    for n, program in enumerate(local['Programs']):
        if program['Name'] == data['name']:
            prog = n
            break
    for n, command in enumerate(local['Programs'][prog]['Commands']):
        if command['Name'] == data['command']:
            com = n
            break
    arguments = data['arguments']
    command_string = "{} {}/{}".format(local['Programs'][prog]['Commands'][com]['Command'],
                                       local['Programs'][prog]['Path'],
                                       local['Programs'][prog]['Commands'][com]['Script'])

    for argument in arguments:
        command_string += " {}".format(argument)
    with cd(local['Programs'][prog]['Path']):
        subprocess.run(command_string, shell=True)
    if data['cron']:
        job = cron.new(command="cd {} && {}".format(local['Programs'][prog]['Path'], command_string))
        if data['frequency'] == 'daily':
            job.minute.on(0)
            job.hour.on(0)
        elif data['frequency'] == 'weekly':
            job.minute.on(0)
            job.hour.on(0)
            job.dow.on(0)
        elif data['frequency'] == 'monthly':
            job.minute.on(0)
            job.hour.on(0)
            job.dom.on(1)
        for item in cron:
            print(item)
        cron.write()
        for item in cron:
            print(item)

    return [local['Programs'][prog]['Name'],
            local['Programs'][prog]['Data']['Local'],
            local['Programs'][prog]['Data']['Repo']['Name']]


if __name__ == '__main__':
    print("Welcome to MAO-Runner")
    while True:
        mode = str(input("Press 1 to install or 2 to run "))
        if mode == '1':
            install_program(str(input("Path to spec ")))
        else:
            break
