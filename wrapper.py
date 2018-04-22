from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
import time as my_time
import psycopg2
import psycopg2.extras
import ConfigParser
import os

app = Flask(__name__)
CORS(app)

config_path = os.path.dirname(os.path.abspath(__file__)) + '/wrapper.ini'
conf = ConfigParser.RawConfigParser()
conf.readfp(open(config_path))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)


@app.route('/config')
def config():
    results = {
        'supports_search': conf.getboolean('wrapper', 'supports_search'),
        'supports_group_request': conf.getboolean('wrapper', 'supports_group_request'),
        'supported_resolutions': conf.get('wrapper', 'supported_resolutions').split(','),
        'supports_marks': conf.getboolean('wrapper', 'supports_marks'),
        'supports_time': conf.getboolean('wrapper', 'supports_time')
    }

    return jsonify(results)


@app.route('/symbols')
def symbols():
    ticker = request.args.get('symbol')

    query = get_data('SELECT * FROM symbols WHERE symbol ILIKE %s OR ticker ILIKE %s',
                    [ticker, ticker])

    if len(query.data) == 0:
        return jsonify({
            "errmsg": "Symbol not found"
        })

    data = query.data[0]

    results = {}

    results["name"] = data["symbol"]
    results["ticker"] = data["ticker"]
    results["description"] = data["description"]
    results["session"] = data["session_regular"]
    results["timezone"] = data["timezone"]
    results["minmov"] = data["minmov"]
    results["pricescale"] = data["pricescale"]
    results["minmove2"] = data["minmov2"]
    results["fractional"] = data["fractional"]
    results["has_intraday"] = data["has_intraday"]
    results["supported_resolutions"] = data["supported_resolutions"].split(',')
    results["has_seconds"] = data["has_seconds"]
    results["has_daily"] = data["has_daily"]
    results["has_weekly_and_monthly"] = data["has_weekly_and_monthly"]
    results["has_empty_bars"] = data["has_empty_bars"]
    results["force_session_rebuild"] = data["force_session_rebuild"]
    results["has_no_volume"] = data["has_no_volume"]
    results["volume_precision"] = data["volume_precision"]
    results["data_status"] = data["data_status"]
    results["expired"] = data["expired"]

    results["intraday_multipliers"] = data["intraday_multipliers"].split(',') if data["intraday_multipliers"] is not None else ""
    results["seconds_multipliers"] = data["seconds_multipliers"].split(',') if data["seconds_multipliers"] is not None else ""
    results["expiration_date"] = data["expiration_date"] if data["expiration_date"] is not None else ""
    results["sector"] = data["sector"] if data["sector"] is not None else ""
    results["industry"] = data["industry"] if data["industry"] is not None else ""
    results["exchange"] = data["exchange"] if data["exchange"] is not None else ""
    results["listed_exchange"] = data["listed_exchange"] if data["listed_exchange"] is not None else ""
    results["type"] = data["type"] if data["type"] is not None else ""

    return jsonify(results)


@app.route('/search')
def search():
    query = request.args.get('query')
    type = request.args.get('type')
    exchange = request.args.get('exchange')
    limit = request.args.get('limit')

    final = []

    query = get_data('SELECT * FROM symbols WHERE symbol ILIKE %s OR ticker ILIKE %s LIMIT %s',
                    [query + '%', query + '%', limit])

    for w in query.data:
        results = {}

        results["symbol"] = w["symbol"]
        results["full_name"] = w["symbol"]
        results["description"] = w["description"]
        results["exchange"] = w["exchange"] if w["exchange"] is not None else ""
        results["ticker"] = w["ticker"]
        results["type"] = w["type"] if w["type"] is not None else ""
        final.append(results)

    return jsonify(final)


@app.route('/history')
def history():
    symbol = request.args.get('symbol')
    left = request.args.get('from')
    right = request.args.get('to')
    resolution = request.args.get('resolution')

    results = {}

    t = []
    c = []
    o = []
    h = []
    l = []
    v = []

    query = get_data('SELECT * FROM history WHERE (ticker ILIKE %s OR symbol ILIKE %s) AND time BETWEEN %s AND %s ORDER BY time',
                    [symbol, symbol, left, right])

    status = query.status

    for w in query.data:
        t.append(w["time"])
        c.append(w["close"])
        o.append(w["open"] if w["open"] is not None else w["close"])
        h.append(w["high"] if w["high"] is not None else w["close"])
        l.append(w["low"] if w["low"] is not None else w["close"])
        v.append(w["volume"])

    results["s"] = status
    results["t"] = t
    results["c"] = c
    results["o"] = o
    results["h"] = h
    results["l"] = l
    results["v"] = v
    if status == "error":
        results["errmsg"] = conf.get('wrapper', 'error_message')

    return jsonify(results)


@app.route('/time')
def time():
    result = int(my_time.time())
    return jsonify(str(result))


def get_postgres_config():
    results = {
        'postgres_host': conf.get('postgresql', 'postgres_host'),
        'postgres_database': conf.get('postgresql', 'postgres_database'),
        'postgres_username': conf.get('postgresql', 'postgres_username'),
        'postgres_password': conf.get('postgresql', 'postgres_password')
    }
    return results


def get_data(query, data):
    postgres_config = get_postgres_config()

    con = psycopg2.connect(database=postgres_config['postgres_database'],
                           user=postgres_config['postgres_username'],
                           host=postgres_config['postgres_host'],
                           password=postgres_config['postgres_password'])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    result = QueryData()
    try:
        cur.execute(query, data)
        array = cur.fetchall()
        result.data = array
        result.status = "ok"
    except Exception:
        result.status = "error"
    finally:
        con.close()

    return result


class QueryData:
    def __init__(self):
        pass

    data = {}
    status = ""
