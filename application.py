
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


@application.route("/about")
def about():
    return render_template("about.html")

@application.route("/martime_education")
def martime_education():
    return render_template("maritime_education.html")

@application.route("/free_trade")
def free_trade():
    return render_template("free_trade.html")

@application.route("/grid")
def grid():
    return render_template("grid.html")

if __name__ == "__main__":
    application.debug=True
    application.run()
