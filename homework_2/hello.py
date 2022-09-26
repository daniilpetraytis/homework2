import flask
import werkzeug.exceptions

app = flask.Flask(__name__)

app_dict = dict()


@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_exception(error):
    return flask.Response(status=405)


@app.get("/hello")
def hello():
    return "HSE OneLove!", 200, {'Content-Type': 'text/plain'}


@app.post("/set")
def set_value():
    response = flask.make_response()
    if ('Content-Type' not in flask.request.headers) or (flask.request.headers['Content-Type'] != 'application/json'):
        response.status_code = 415
    elif ('key' not in flask.request.json) or ('value' not in flask.request.json):
        response.status_code = 400
    else:
        app_dict[flask.request.json['key']] = flask.request.json['value']
        response.status_code = 200
    return response


@app.get("/get/<key>")
def get_value(key):
    if key not in app_dict.keys():
        response = flask.make_response()
        response.status_code = 404
        return response
    json_response = flask.json.dumps(
        {
            'key': key,
            'value': app_dict[key]
        }
    )
    return json_response, 200, {'Content-Type': 'application/json'}


@app.post("/divide")
def divide():
    if ('Content-Type' not in flask.request.headers) or (
            flask.request.headers['Content-Type'] != 'application/json'):
        response = flask.make_response()
        response.status_code = 415
        return response
    if ('dividend' not in flask.request.json) or ('divider' not in flask.request.json):
        response = flask.make_response()
        response.status_code = 400
        return response
    if flask.request.json['divider'] == 0:
        response = flask.make_response()
        response.status_code = 400
        return response
    return str(flask.request.json['dividend'] / flask.request.json['divider']), 200, {'Content-Type': 'text/plain'}
