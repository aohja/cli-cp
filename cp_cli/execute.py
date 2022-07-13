import click
import subprocess
import sys
import time

COMPILE_CMD = "g++ -DLOCAL -std=c++2a -O2 -Wall -Wextra"

def build(problem):
    command = f"{COMPILE_CMD} {problem}.cpp -o {problem}"
    # click.echo(command)
    cp = subprocess.run(command, shell=True)
    if cp.returncode != 0:
        sys.exit(cp.stdout)
    click.echo(f"Compiled {problem}.cpp")
    return 0


def output(test_case, input_file, result, answer, runtime):
    verdict = (result.stdout == answer.stdout)
    outcome = ""
    if (verdict):
        outcome = "Passed"
    else:
        outcome = "Failed"
    print(f"Sample {test_case}: {outcome} ({runtime * 1000} ms)")
    if (not verdict):
        print("--------------------------------------------------------------------------------------------")
        print("Input")
        sample = subprocess.run(f"cat ./in/{input_file}", capture_output=True)
        print(sample.stdout.decode("utf-8"))
        print("Expected Output")
        print(answer.stdout.decode("utf-8"))
        print("User Output")
        print(result.stdout.decode("utf-8"))
        print("--------------------------------------------------------------------------------------------")
    return verdict


def run_one(problem, input_file, output_file, test_case):
    cmd = f"{problem}.exe < ./in/{input_file}"
    start = time.time()
    result = subprocess.run(cmd, shell=True, capture_output=True)
    runtime = time.time() - start
    cmd = f"cat ./out/{output_file}"
    answer = subprocess.run(cmd, shell=True, capture_output=True)
    return output(test_case, input_file, result, answer, runtime)


@click.command()
@click.argument("problem")
def run(problem):
    subprocess.run("clear", shell=True)
    build(problem)
    cp = subprocess.run(f"ls ./in | grep '{problem}_input'", shell=True, capture_output=True, text=True)
    test_inputs = [filename for filename in cp.stdout.split('\n') if filename]
    sorted(test_inputs)
    cp = subprocess.run(f"ls ./out | grep '{problem}_out'", shell=True, capture_output=True, text=True)
    test_outputs = [filename for filename in cp.stdout.split('\n') if filename]
    sorted(test_outputs)
    passed = 0
    for i in range(len(test_inputs)):
        passed += run_one(problem, test_inputs[i], test_outputs[i], i + 1)
    print(f"Passed: {passed} / {len(test_inputs)}")
    return 0
