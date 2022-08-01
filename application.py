
from flask import Flask, render_template

application = Flask(__name__)

# application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
#         username='flask-movies',
#         password='complexpassword123',
#         host='localhost',
#         port='5432',
#         database='flask-movies',
#     )


@application.route("/")
def root():
    return render_template("index.html")


@application.route("/hello")
def index():
    return "Hello World from COE Team."

if __name__ == "__main__":
    application.debug=True
    application.run()
