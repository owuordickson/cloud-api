import sys
import json
from algorithms.init_procedure import *


def application(env, start_response):
    try:
        start_response("200 OK", [("Content-Type", "image/png")])
        request_body_size = int(env.get('CONTENT_LENGTH', 0))
        request_body = env['wsgi.input'].read(request_body_size)
        message = init_request(request_body)
    except (ValueError):
        start_response("200 OK", [("Content-Type", "application/json")])
        request_body_size = 0
        message = json.dumps({"success":"welcome to py-server API"})

    return str(message).encode("utf-8")
