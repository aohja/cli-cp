import click
import os
import http.server
from .utils import *

"""
Using competitive companion to get names (from ecnerwala)
"""

def listen_once(timeout=None):
    json_data = None
    class CompetitiveCompanionHandler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            nonlocal json_data
            json_data = json.load(self.rfile)

    with http.server.HTTPServer(('127.0.0.1', 10043), CompetitiveCompanionHandler) as server:
        server.timeout = 2000
        server.handle_request()

    if json_data is not None:
        print(f"Got data {json.dumps(json_data)}")
    else:
        print("Got no data")
    return json_data


def listen_many(*, num_items=None, num_batches=None, timeout=None):
    if num_items is not None:
        res = []
        for _ in range(num_items):
            cur = listen_once(timeout=None)
            res.append(cur)
        return res

    if num_batches is not None:
        res = []
        batches = {}
        while len(batches) < num_batches or any(need for need, tot in batches.values()):
            print(f"Waiting for {num_batches} batches:", batches)
            cur = listen_once(timeout=None)
            res.append(cur)
            cur_batch = cur['batch']
            batch_id = cur_batch['id']
            batch_cnt = cur_batch['size']
            if batch_id not in batches:
                batches[batch_id] = [batch_cnt, batch_cnt]
            assert batches[batch_id][0] > 0
            batches[batch_id][0] -= 1
        return res

    res = [listen_once(timeout=None)]
    while True:
        cnd = listen_once(timeout=timeout)
        if cnd is None:
            break
        res.append(cnd)
    return res


def save_samples(data):
    letter = get_prob_name(data)
    if not os.path.exists(f"./{letter}.cpp"):
        create_template(letter, data["name"])
    if not os.path.exists(f"./in"):
        os.mkdir(f"./in")
    if not os.path.exists(f"./out"):
        os.mkdir(f"./out")
    for i, t in enumerate(data['tests'], start=1):
        input_path = f"{letter}_input{i}.in"
        f = open(os.path.join("in", input_path), "w")
        f.write(t['input'])
        f.close()
        output_path = f"{letter}_out{i}.out"
        f = open(os.path.join("out", output_path), "w")
        f.write(t['output'])
        f.close()
    return


@click.command()
def listen():
    click.echo(f"Listening for input data, press q to exist")
    json_data = listen_many(num_batches=1)
    for data in json_data:
        save_samples(data)
