import sys
import json


def application(env, start_response):
    start_response("200 OK", [("Content-Type", "application/json")])
    try:
        request_body_size = int(env.get('CONTENT_LENGTH', 0))
        request_body = env['wsgi.input'].read(request_body_size)
        data = json.loads(request_body)
        message = data
        # message = "Dickson PC"
    except (ValueError):
        request_body_size = 0
        message = json.dumps({"error":"error found"})
    # version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    # message = "Hello World from from Dickson PC"
    # message = env['QUERY_STRING']
    # input = sys.argv[1]
    # message = str("hello "+str(input))
    return str(message).encode("utf-8")
