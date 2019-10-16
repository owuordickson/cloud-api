import sys
import json
from algorithms.init_fuzz_x import *


def application(env, start_response):
    start_response("200 OK", [("Content-Type", "image/png")])
    try:
        request_body_size = int(env.get('CONTENT_LENGTH', 0))
        request_body = env['wsgi.input'].read(request_body_size)
        # data = json.loads(request_body)
        # message = json.dumps({"pattern":data["patternType"]})
        message = init_algorithm(request_body)
    except (ValueError):
        request_body_size = 0
        message = json.dumps({"success":"welcome to py-server API"})

    return str(message).encode("utf-8")
