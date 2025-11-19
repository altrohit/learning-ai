import sys
import modal

app = modal.App("hello-world")

@app.function()
def f(i):
    if i%2 == 0:
        print(f'hello {i}')
    else:
        print(f'world {i}', file=sys.stderr)
    
    return i*i

@app.local_entrypoint()
def main():
    i = 1000
    print(f.local(i)) # run locally

    print(f.remote(i)) # run remotely

    # run parallel and remotely on Modal
    total = 0
    for ret in f.map(range(200)):
        total += ret
    print(total)