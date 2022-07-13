from datetime import datetime
import re
import json

author = "Aadi Ohja"

"""
Template file setup
"""

TEMPLATE_PATH = "../templates/template.cpp"

def get_header(problem_name):
    author_line = f" * Author:  {author}\n"
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    created_line = f" * Created: {dt_string}\n"
    problem_line = f" * Problem: {problem_name}\n"
    header = "/**\n" + author_line + created_line + problem_line + "**/\n"
    return header


def create_template(filename, problem_name):
    f = open(filename, "a")
    f.write(get_header(problem_name))
    with open(TEMPLATE_PATH, 'r') as sol:
        f.write(sol.read())
    return


"""
Getting the problem name (from ecnerwala)
"""
NAME_PATTERN = re.compile(r'^(?:Problem )?([A-Z][0-9]*)\b')

def get_prob_name(data):
    if 'USACO' in data['group']:
        if 'fileName' in data['input']:
            names = [data['input']['fileName'].rstrip('.in'), data['output']['fileName'].rstrip('.out')]
            if len(set(names)) == 1:
                return names[0]

    if 'url' in data and data['url'].startswith('https://www.codechef.com'):
        return data['url'].rstrip('/').rsplit('/')[-1]

    patternMatch = NAME_PATTERN.search(data['name'])
    if patternMatch is not None:
        return patternMatch.group(1)

    print(f"For data: {json.dumps(data, indent=2)}")
    return input("What name to give? ")