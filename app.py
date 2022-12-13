from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/characters/<name>')
def get_characters(name):
    return 'Hello %s!' % name

if __name__ == '__main__':
    app.run()