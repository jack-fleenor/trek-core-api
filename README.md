Here is an example of a simple Flask API app:

Copy code
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
To run this app, you will need to have Flask installed. You can install Flask by running pip install Flask in your terminal.

Once you have Flask installed, you can run the app by using the following command:

Copy code
python app.py
This will start the Flask development server, which you can access by going to http://127.0.0.1:5000/ in your web browser.

You can also specify the host and port that the Flask development server should run on by using the --host and --port flags, respectively. For example, the following command will start the server on host 0.0.0.0 and port 8080:

Copy code
python app.py --host=0.0.0.0 --port=8080
Keep in mind that the Flask development server is not intended for production use. For deploying a Flask app to a production environment, you will need to use a more robust web server, such as Gunicorn or uWSGI.