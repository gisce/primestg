from flask import Flask
from flask import request
from flask import Response
from primestg.service import Service

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hola!"


@app.route("/cnc/dailyincremental/meters/")
def S02_all():
    return "Hola!"


@app.route("/cnc/dailyincremental/meters/<string:meter_id>/")
def S02(meter_id):
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    s = Service()
    rep = s.get_daily_incremental(meter_id, date_from, date_to)
    return Response(rep, mimetype="text/plain")

if __name__ == "__main__":
    app.run()
