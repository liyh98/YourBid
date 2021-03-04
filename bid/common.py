import flask
import json
from .dealer import *

commonPages = flask.Blueprint('commonPages', __name__, template_folder='../templates')

@commonPages.route("/bid", methods=['POST', 'GET'])
def bid():
    if flask.request.method == 'GET':
        game = Game("None", "None")
        flask.session['hash'] = flask.request.args['hash']
        with open('./hands/' + str(flask.request.args['hash']) + '.json', 'r') as f:
            game.fromJson(json.load(f))
        player = flask.request.args['player']
        flask.session['player'] = player
        hand = None
        l = len(game.bids)
        if ((l > 1 and game.bids[0] != '-') or l > 2) and game.bids[l - 1] == "P":
            hand = game.pn.display() + game.ps.display() + ['Vul: ' + game.vul, 'Dealer: ' + game.dealer]
        elif player == 'south':
            hand = game.ps.display() + ['Vul: ' + game.vul, 'Dealer: ' + game.dealer]
        else:
            hand = game.pn.display() + ['Vul: ' + game.vul, 'Dealer: ' + game.dealer]
        return flask.render_template("bid.html", game=game, player=player, hand=hand, bids=game.bids)
    if flask.request.method == 'POST':
        hash = flask.session['hash']
        bid = flask.request.form.get('thisbid')
        player = flask.session['player']
        game = Game("None", "None")
        with open('./hands/' + str(hash) + '.json', 'r') as f:
            game.fromJson(json.load(f))
        with open('./hands.json', 'r') as f:
            handlist = json.load(f)
        for hand in handlist:
            print(hand['hash'], hash)
            if str(hand['hash']) == str(hash):
                print("found!!")
                if str(bid) == "P" and ((len(game.bids) > 1 and game.bids[0] != '-') or len(game.bids) > 2):
                    hand['status'] = "closed"
                elif player == "north":
                    hand['status'] = "south"
                else:
                    hand['status'] = "north"
        with open('./hands.json', 'w') as f:
            json.dump(handlist, f)
        game.bids.append(bid)
        with open('./hands/' + str(hash) + '.json', 'w') as f:
            json.dump(game.toJson(), f)
        if player == 'south':
            return flask.redirect(flask.url_for("southPages.index"))
        if player == 'north':
            return flask.redirect(flask.url_for("northPages.index"))
