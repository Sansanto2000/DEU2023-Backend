from flask import Flask

app = Flask(__name__)

def get_hit_count():
    retries = 5
    return True

@app.route('/')
def hello():
    count = 2
    return 'Hello World! I have been seen {} times.\n'.format(count)