from flask import Flask, request, json, jsonify
import syncer
from ruamel.yaml import YAML


app = Flask(__name__)
yaml = YAML()
yaml.preserve_quotes = True


def downloadtool():
    print("Tools currently registered in the database:")
    syncer.list("tools")
    tool = str(input("Which tool do you need?"))
    repo = syncer.get("tools/" + tool)
    answer = str(input("Clone {} to importdir?[y/n]".format(repo)))
    if answer == 'y':
        syncer.clonetool(repo, tool)


@app.route('/regtools', methods=['GET'])
def regtools():
    return jsonify(syncer.list('tools'))


@app.route('/datasets', methods=['GET'])
def datasets():
    return jsonify(syncer.list('data'))


@app.route('/installed', methods=['GET'])
def installed():
    with open('local.yml', 'r') as local:
        data = yaml.load(local)
    result = []
    for program in data['Programs']:
        result.append(program['Name'])
    return jsonify(result)


@app.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    syncer.write("tools/{}".format(data['name']), data['url'])
    return jsonify(syncer.get("tools/{}".format(data['name'])))


@app.route('/install', methods=['POST'])
def install():
    data = json.loads(request.data)
    repo = syncer.get("tools/" + data['name'])
    syncer.clonetool(repo, data['name'])
    return installed()


@app.route('/help', methods=['POST'])
def help():
    query = json.loads(request.data)
    with open('local.yml', 'r') as local:
        data = yaml.load(local)
    for program in data['Programs']:
        if program['Name'] == (query['name']):
            return jsonify(program['Commands'])
    else:
        return jsonify("No such program")


@app.route('/retrieve', methods=['POST'])
def retrieve():
    data = json.loads(request.data)
    syncer.retrieve(data['name'])
    return jsonify("Done")


@app.route("/run", methods=['POST'])
def run():
    data = json.loads(request.data)
    syncer.sync(data)
    return jsonify("Done")


if __name__ == '__main__':
    app.run()
