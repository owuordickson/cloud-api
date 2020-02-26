import json
# import sys
# from algorithms.init_fuzz_x import *
from main_entry import init_request


def application(env, start_response):
    
    try:
        start_response("200 OK", [("Content-Type", "image/png")])
        request_body_size = int(env.get('CONTENT_LENGTH', 0))
        request_body = env['wsgi.input'].read(request_body_size)
        # message = init_algorithm(request_body)
        message = init_request(request_body)
    except Exception as error:
        start_response("204 OK", [("Content-Type", "application/json")])
        # request_body_size = 0
        message = json.dumps({"Failed" : str(error)})

    return str(message).encode("utf-8")
