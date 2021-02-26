import flask
import bid

#-----------------Initialization---------------------------------

app = flask.Flask(__name__)
app.secret_key = "YourBid:)"
app.config['TEMPLATES_AUTO_RELOAD'] = True
#---------------Page Registration-------------------------------

app.register_blueprint(bid.commonPages)
app.register_blueprint(bid.northPages, url_prefix="/north")
app.register_blueprint(bid.southPages, url_prefix="/south")

#-----------------Working Area----------------------------------

app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
