import flask
import json
from .dealer import *


southPages = flask.Blueprint('southPages', __name__, template_folder='../templates')


@southPages.route("/", methods=['POST', 'GET'])
def index():
    if flask.request.method == "GET":
        with open('./hands.json', 'r') as f:
            handlist = json.load(f)
        return flask.render_template("player.html", player='south', handlist=handlist)


@southPages.route("/deal", methods=['POST', 'GET'])
def deal():
    if flask.request.method == "GET":
        game = Game("None")
        with open('./hands/' + str(game.hash) + '.json', 'w') as f:
            json.dump(game.toJson(), f)
        hand = {"hash": game.hash, "status": "south"}
        with open('./hands.json', 'r') as f:
            handlist = json.load(f)
        handlist.append(hand)
        with open('./hands.json', 'w') as f:
            json.dump(handlist, f)
        return flask.redirect(flask.url_for('commonPages.bid', player='south', hash=game.hash))
